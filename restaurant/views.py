from collections import defaultdict

from django.shortcuts import render

from .models import MenuItem

CATEGORY_ORDER = [
    "Antreuri",
    "Ciorbe",
    "Feluri principale",
    "Garnituri",
    "Salate",
    "Deserturi",
    "Răcoritoare",
    "Energizante",
    "Cafea & Ceai",
    "Bere",
    "Alcool",
    "Vin spumant",
    "Vinuri roze",
    "Vinuri albe",
    "Vinuri roșii",
]


def home(request):
    grouped = defaultdict(list)
    for item in MenuItem.objects.all().order_by("category", "name"):
        grouped[item.category].append(item)

    menu_sections = [
        (cat, grouped[cat])
        for cat in CATEGORY_ORDER
        if cat in grouped
    ]
    # Append any unexpected categories not in the ordered list
    for cat, items in grouped.items():
        if cat not in CATEGORY_ORDER:
            menu_sections.append((cat, items))

    return render(request, "home.html", {"menu_sections": menu_sections})
