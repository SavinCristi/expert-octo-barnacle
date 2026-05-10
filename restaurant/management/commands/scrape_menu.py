import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from restaurant.models import MenuItem

URL = "https://restaurant-vanatorul.ro/meniu/"

CATEGORY_LABELS = {
    "antreuri": "Antreuri",
    "ciorbe": "Ciorbe",
    "feluri": "Feluri principale",
    "garnituri": "Garnituri",
    "salate": "Salate",
    "deserturi": "Deserturi",
    "bauturi": "Răcoritoare",
    "energizante": "Energizante",
    "cafea": "Cafea & Ceai",
    "bere": "Bere",
    "alcool": "Alcool",
    "vinspumant": "Vin spumant",
    "vinroze": "Vinuri roze",
    "vinurialbe": "Vinuri albe",
    "vinurirosii": "Vinuri roșii",
}


def fetch_soup():
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_items(soup):
    """
    Walk top-level Elementor sections in document order.
    When a section contains a .elementor-menu-anchor, update the current category.
    When a section contains h3 item titles + a weight/price inner row, record the item.
    """
    items = []
    current_category = None

    for section in soup.find_all("section", class_="elementor-top-section"):
        # Check if this section sets a new category
        anchor = section.find("div", class_="elementor-menu-anchor")
        if anchor and anchor.get("id") in CATEGORY_LABELS:
            current_category = CATEGORY_LABELS[anchor["id"]]
            continue

        if current_category is None:
            continue

        # Each item lives in an elementor-col-100 column containing an h3 + inner section
        for col in section.find_all("div", class_="elementor-col-100"):
            h3 = col.find("h3", class_="elementor-heading-title")
            if not h3:
                continue

            name = h3.get_text(strip=True)
            # Strip leading "©" or similar decorative chars
            name = re.sub(r"^[©®™\s]+", "", name).strip()

            # Inner section holds [weight_col, price_col]
            inner = col.find("section", class_="elementor-inner-section")
            weight = ""
            price = None

            if inner:
                ps = inner.find_all("p", class_="elementor-heading-title")
                if len(ps) >= 2:
                    weight = ps[0].get_text(strip=True)
                    price_text = ps[1].get_text(strip=True)
                    m = re.search(r"[\d,.]+", price_text)
                    if m:
                        price = float(m.group().replace(",", "."))
                elif len(ps) == 1:
                    # Some items only have a price with no weight
                    price_text = ps[0].get_text(strip=True)
                    if "lei" in price_text.lower():
                        m = re.search(r"[\d,.]+", price_text)
                        if m:
                            price = float(m.group().replace(",", "."))
                    else:
                        weight = ps[0].get_text(strip=True)

            if name and price is not None:
                items.append(
                    {
                        "name": name,
                        "category": current_category,
                        "weight": weight,
                        "price": price,
                    }
                )

    return items


class Command(BaseCommand):
    help = "Scrape the live menu from restaurant-vanatorul.ro and save items to the database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching menu page...")
        soup = fetch_soup()

        self.stdout.write("Parsing items...")
        items = parse_items(soup)
        self.stdout.write(f"  Found {len(items)} items")

        created = updated = 0
        for item in items:
            obj, is_new = MenuItem.objects.update_or_create(
                name=item["name"],
                defaults={
                    "category": item["category"],
                    "weight": item["weight"],
                    "price": item["price"],
                },
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done — {created} created, {updated} updated ({created + updated} total)"
            )
        )
