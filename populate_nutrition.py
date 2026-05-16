"""
Populate calories and allergens for all MenuItem objects.

Allergens declared per EU Regulation 1169/2011 (14 mandated allergens):
  Gluten, Crustacee, Ouă, Pește, Arahide, Soia, Lapte,
  Fructe cu coajă lemnoasă, Țelină, Muștar, Susan,
  Dioxid de sulf/Sulfiți, Lupin, Moluște

Notes:
  - Distilled spirits (whisky, vodka, pălincă, brandy) are exempt from gluten/sulfiți
    labeling under EU law even when derived from cereals/wine — only beer requires Gluten.
  - Wines always carry Sulfiți (naturally present + added SO2).
  - Empty allergens string = no declarable EU allergens for that item.
"""

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from restaurant.models import MenuItem

# (calories_str, allergens_str)  — empty string means no declarable allergen
data = {
    # ── ANTREURI ──────────────────────────────────────────────────────────────
    # Creste de slănină prăjită pe pâine cu ceapă verde și roșii (200g)
    # Toasted pork-fat crisps on bread with spring onion & tomato
    1:  ("380 kcal", "Gluten"),

    # Bunătățuri din Poiana Brașov (200g)
    # Assorted smoked cold-cuts + cheese platter from Poiana Brașov
    2:  ("420 kcal", "Gluten, Lapte, Sulfiți"),

    # Carpaccio de cerb (180g)
    # Thinly sliced raw/cured venison, typically finished with Parmesan & mustard dressing
    3:  ("220 kcal", "Lapte, Muștar, Sulfiți"),

    # Platou de mizilicuri vânătoresc (400g)
    # Large hunter's snack board: smoked meats, brânză, pickles, bread
    4:  ("680 kcal", "Gluten, Lapte, Sulfiți"),

    # ── CIORBE ────────────────────────────────────────────────────────────────
    # Ciorbă de fasole (250g) — soured with borș (fermented wheat bran water) + celery base
    5:  ("180 kcal", "Gluten, Țelină, Sulfiți"),

    # Ciorba zilei (300g) — variable; allergens cover most Romanian soup bases
    6:  ("200 kcal", "Gluten, Lapte, Ouă, Țelină"),

    # Smântână (50g) — sour cream accompaniment
    7:  ("85 kcal", "Lapte"),

    # Pâine cu cartofi și ardei iute — bread, potato & chili side
    8:  ("150 kcal", "Gluten"),

    # ── FELURI PRINCIPALE ─────────────────────────────────────────────────────
    # Bulz Vânătoresc (300g)
    # Grilled polenta ball stuffed with brânză de burduf (sheep cheese) and bacon
    9:  ("480 kcal", "Lapte, Sulfiți"),

    # Tagliatelle vânătorești (150g pasta / 150g game ragù)
    # Egg pasta with game-meat ragù finished with cream and wine
    10: ("520 kcal", "Gluten, Ouă, Lapte, Sulfiți"),

    # Gulaș de mistreț (250g)
    # Wild-boar goulash thickened with flour; paprika base, celery, wine
    11: ("380 kcal", "Gluten, Țelină, Sulfiți"),

    # Piept de rață gătit sous vide cu sos de cireșe (150g / 15g sauce)
    # Sous-vide duck breast; cherry sauce with butter and wine
    12: ("320 kcal", "Lapte, Sulfiți"),

    # Mușchiuleț de mistreț pe grătar cu sos de ciuperci de pădure (150g / 15g)
    # Charcoal-grilled wild-boar tenderloin; wild-mushroom sauce with butter & wine
    13: ("340 kcal", "Lapte, Sulfiți, Țelină"),

    # Combinată vânătorească de mistreț și căprioară (150g / 15g / 150g)
    # Hunter's combo: boar + venison + sauce + side (polenta)
    14: ("560 kcal", "Lapte, Sulfiți, Țelină"),

    # Medalion de căprioară alături de sos de fructe de pădure (150g / 15g)
    # Venison medallion; forest-berry sauce with butter and wine reduction
    15: ("290 kcal", "Lapte, Sulfiți"),

    # Flambaj vânătoresc "du chef" servit cu sos vânătoresc (150g / 30g / 150g)
    # Flambéed game dish; hunter's sauce (flour-thickened, wine, butter) + side
    16: ("620 kcal", "Gluten, Lapte, Sulfiți, Țelină"),

    # Friptură de urs la tavă cu sos brun și garnitură (150g / 15g / 150g)
    # Roast bear; brown sauce (roux + stock + wine) + side
    17: ("550 kcal", "Gluten, Lapte, Sulfiți, Țelină"),

    # Pastramă de oaie trasă la tigaie cu mămăliguță (150g / 15g / 150g)
    # Pan-fried sheep pastrami (cured with SO2) + polenta with butter
    18: ("480 kcal", "Lapte, Sulfiți"),

    # Pastramă de oaie la grătar cu mămăliguță (150g / 15g / 150g)
    # Grilled sheep pastrami + polenta with butter
    19: ("460 kcal", "Lapte, Sulfiți"),

    # Mușchi de berbecuț cu sos de vin (150g / 15g)
    # Lamb loin; red-wine & butter sauce
    20: ("310 kcal", "Lapte, Sulfiți"),

    # Burgerul (200g patty / 150g bun + toppings)
    # Classic beef burger: sesame bun, cheese, egg-mayo, mustard
    21: ("680 kcal", "Gluten, Ouă, Lapte, Muștar, Susan"),

    # Mușchi de vită servit cu "untul zeilor" (150g / 15g)
    # Beef tenderloin with compound herb butter
    22: ("380 kcal", "Lapte, Sulfiți"),

    # Cârnați de pleșcoi la grătar (150g)
    # Grilled Pleșcoi spicy lamb-beef sausages (cured, SO2)
    23: ("380 kcal", "Sulfiți"),

    # Meat-"itei" — mici/mititei, 4 pieces (150g)
    # Grilled minced-meat rolls bound with breadcrumbs/bicarbonate; SO2 spice mix
    24: ("420 kcal", "Gluten, Sulfiți"),

    # Ceafă de porc pe grătar cu cărbuni (150g) — plain charcoal pork neck
    25: ("380 kcal", ""),

    # Coaste de porc pe grătar cu cărbuni, ceapă roșie și sos barbeque (300g / 15g / 15g)
    # Charcoal pork ribs; BBQ sauce contains gluten, mustard, sulfiți
    26: ("680 kcal", "Gluten, Muștar, Sulfiți"),

    # Platoul "Berarului" pentru 2 persoane (300g / 30g / 300g)
    # Beer-man's mixed grill platter for 2: sausages, ribs, burger, sides
    27: ("1200 kcal (2 pers.)", "Gluten, Ouă, Lapte, Muștar, Sulfiți, Susan"),

    # Aripioare de pui la grătar cu sos de smântână și usturoi (150g)
    # Grilled chicken wings; garlic sour-cream dip
    28: ("420 kcal", "Lapte"),

    # Piept de pui la grătar (150g) — plain grilled chicken breast
    29: ("220 kcal", ""),

    # Burger de pui (200g / 150g) — chicken burger with standard toppings
    30: ("580 kcal", "Gluten, Ouă, Lapte, Muștar, Susan"),

    # File de doradă cu sos butterlemon (150g / 15g)
    # Sea-bream fillet; butter-lemon sauce
    31: ("280 kcal", "Pește, Lapte"),

    # Tocăniță de ciuperci cu mămăliguță (150g)
    # Mushroom stew + polenta (butter in polenta and stew)
    32: ("220 kcal", "Lapte"),

    # Snițel de pui parizian (200g)
    # Parisian-style breaded chicken schnitzel (flour-egg-breadcrumb coating)
    33: ("480 kcal", "Gluten, Ouă, Lapte"),

    # Paste cu sos de roșii (150g) — egg pasta with tomato sauce
    34: ("340 kcal", "Gluten, Ouă"),

    # ── GARNITURI ─────────────────────────────────────────────────────────────
    # Mămăliguță (150g) — polenta finished with butter
    35: ("150 kcal", "Lapte"),

    # Cartofi trași la tigaie cu pătrunjel și usturoi (150g) — pan potatoes, no dairy
    36: ("200 kcal", ""),

    # Legume proaspete la tigaie (150g) — stir-fried seasonal vegetables
    37: ("100 kcal", ""),

    # Cartofi prăjiți cu parmezan (150g)
    38: ("280 kcal", "Lapte"),

    # Chips de cartofi dulci (150g) — sweet-potato chips, no allergens
    39: ("240 kcal", ""),

    # ── SALATE ────────────────────────────────────────────────────────────────
    40: ("60 kcal",  ""),   # Salată de varză albă cu roșie
    41: ("40 kcal",  ""),   # Salată verde, roșii, castraveți
    42: ("30 kcal",  ""),   # Murături asortate
    43: ("70 kcal",  ""),   # Salată de ardei copți de casă
    44: ("80 kcal",  ""),   # Salată de ciuperci pleurotus
    45: ("130 kcal", "Lapte"),   # Salată de rucola, roșii, parmezan

    # ── DESERTURI ─────────────────────────────────────────────────────────────
    # Papanaș cu dulceată de afine și smântână (120/30g)
    # Fried cheese doughnut: cottage cheese, eggs, flour; topped with sour cream
    46: ("380 kcal", "Gluten, Ouă, Lapte"),

    # Clătite cu dulceață de afine și sos de ciocolată (150g)
    # Crêpes (flour + eggs + milk) with blueberry jam and chocolate sauce
    47: ("420 kcal", "Gluten, Ouă, Lapte"),

    # Înghețată artizanală (100g) — artisan ice cream (milk + eggs base)
    48: ("220 kcal", "Lapte, Ouă"),

    # Tira Mi Su (150g) — tiramisu: savoiardi (gluten), eggs, mascarpone, Marsala (sulfiți)
    49: ("380 kcal", "Gluten, Ouă, Lapte, Sulfiți"),

    # Moelleux au chocolat (150g) — chocolate lava cake: flour, eggs, butter, cream
    50: ("420 kcal", "Gluten, Ouă, Lapte"),

    # Crêpes Suzette (120g) — crêpes flambéed with Grand Marnier (sulfiți in liqueur)
    51: ("380 kcal", "Gluten, Ouă, Lapte, Sulfiți"),

    # ── RĂCORITOARE ───────────────────────────────────────────────────────────
    52: ("105 kcal", ""),   # Coca Cola / Cola Zero (250ml)
    53: ("105 kcal", ""),   # Fanta / Sprite / Schweppes (250ml)
    54: ("120 kcal", ""),   # Cappy Nectar (250ml)
    55: ("75 kcal",  ""),   # Fuze Tea (250ml)
    56: ("0 kcal",   ""),   # Apă minerală / Apă plată (330ml)
    57: ("135 kcal", ""),   # Suc de mere Naturali (300ml)
    58: ("135 kcal", ""),   # Suc natural de portocale (300ml)
    59: ("105 kcal", ""),   # Suc natural de grapefruit (300ml)
    60: ("120 kcal", ""),   # Limonadă proaspătă (500ml)

    # ── ENERGIZANTE ───────────────────────────────────────────────────────────
    61: ("113 kcal", ""),   # Red Bull (250ml)

    # ── CAFEA & CEAI ──────────────────────────────────────────────────────────
    62: ("5 kcal",   ""),         # Ristretto Nespresso (15ml)
    63: ("5 kcal",   ""),         # Espresso Nespresso (25ml)
    64: ("10 kcal",  ""),         # Americano Nespresso (110ml)
    65: ("80 kcal",  "Lapte"),    # Cappuccino (110ml)
    66: ("120 kcal", "Lapte"),    # Café Latte (200ml)
    67: ("10 kcal",  ""),         # Espresso dublu Nespresso (40ml)
    68: ("230 kcal", "Lapte"),    # Ciocolată caldă (200ml)
    69: ("150 kcal", "Lapte"),    # Café frapé (300ml) — made with milk
    70: ("5 kcal",   ""),         # Ceai Taylors of Harrogate (200ml)

    # ── BERE ──────────────────────────────────────────────────────────────────
    # All beers contain Gluten (barley malt — not distilled, allergen intact)
    71: ("138 kcal", "Gluten"),   # Ursus premium draft (300ml)
    72: ("150 kcal", "Gluten"),   # Ursus Black (330ml)
    73: ("148 kcal", "Gluten"),   # Peroni Nastro Azzurro (330ml)
    74: ("260 kcal", "Gluten"),   # Bere Artizanală Dănilă nefiltrată (500ml)
    75: ("83 kcal",  "Gluten"),   # Ursus fără alcool (330ml)
    76: ("100 kcal", "Gluten"),   # Ursus Cooler fără alcool (330ml)

    # ── ALCOOL / COCKTAILS ────────────────────────────────────────────────────
    # Note: distilled spirits exempt from cereal-gluten labeling under EU 1169/2011
    77: ("56 kcal",  "Sulfiți"),                    # Martini Alb/Roșu (40ml) — vermouth, SO2
    78: ("95 kcal",  ""),                            # Afinată Bran (40ml) — blueberry liqueur
    79: ("165 kcal", ""),                            # Campari Orange (300ml)
    80: ("185 kcal", ""),                            # Cuba Libre (300ml)
    81: ("170 kcal", ""),                            # Gin Tonic (300ml)
    82: ("155 kcal", "Sulfiți"),                     # Aperol Spritz (300ml) — prosecco
    83: ("180 kcal", "Sulfiți"),                     # Hugo (300ml) — prosecco + elderflower
    84: ("105 kcal", ""),                            # Averna (40ml)
    85: ("103 kcal", ""),                            # Jägermeister (40ml)
    86: ("116 kcal", "Fructe cu coajă lemnoasă"),    # Disaronno (40ml) — bitter almond oil
    87: ("100 kcal", ""),                            # Fernet Branca (40ml)
    88: ("95 kcal",  ""),                            # Tanqueray gin (40ml)
    89: ("95 kcal",  ""),                            # Finlandia vodka (40ml)
    90: ("95 kcal",  ""),                            # Grey Goose vodka (40ml) — distilled, exempt
    91: ("108 kcal", ""),                            # Pălincă Casa Pălincii (40ml)
    92: ("110 kcal", ""),                            # Pălincă fiartă Casa Pălincii (40ml)
    93: ("108 kcal", ""),                            # Pălincă Zetea (40ml)
    94: ("131 kcal", "Lapte"),                       # Bailey's (40ml) — Irish cream
    95: ("97 kcal",  ""),                            # Jack Daniel's (40ml)
    96: ("95 kcal",  ""),                            # Johnnie Walker Black (40ml)
    97: ("95 kcal",  ""),                            # Glenfiddich 12y (40ml)
    98: ("92 kcal",  "Sulfiți"),                     # Jidvei VSOP brandy (40ml) — wine-based
    99: ("98 kcal",  "Sulfiți"),                     # Metaxa 7* (40ml) — wine-based

    # ── VIN SPUMANT ───────────────────────────────────────────────────────────
    100: ("164 kcal", "Sulfiți"),   # Le Contesse Brut (200ml)

    # ── VINURI ROZE (≈150ml glass unless stated) ──────────────────────────────
    101: ("133 kcal", "Sulfiți"),   # Corcova Rosé (187ml)
    102: ("120 kcal", "Sulfiți"),   # Organic Rosé — Domeniul Bogdan
    103: ("120 kcal", "Sulfiți"),   # Issa Rosé — La Salina
    104: ("125 kcal", "Sulfiți"),   # C'est Soir Busuioacă de Bohotin (demi-sec version higher)
    105: ("120 kcal", "Sulfiți"),   # Negru de Drăgășani — Bauer
    106: ("120 kcal", "Sulfiți"),   # Sole Rosé — Recaș

    # ── VINURI ALBE (≈150ml glass unless stated) ──────────────────────────────
    107: ("150 kcal", "Sulfiți"),   # Corcova Chardonnay (187ml)
    108: ("123 kcal", "Sulfiți"),   # Sauvignon Blanc — Domeniile la Migdali
    109: ("123 kcal", "Sulfiți"),   # Implicit Pinot Grigio — Recaș
    110: ("123 kcal", "Sulfiți"),   # Colțul Pietrei Sauvignon Blanc — Viile Metamorfosis
    111: ("123 kcal", "Sulfiți"),   # Crâmpoșie — Cepari
    112: ("123 kcal", "Sulfiți"),   # White Artisan — Aurelia Vișinescu
    113: ("123 kcal", "Sulfiți"),   # Terra Romana Sauvignon Blanc & Fetească Regală
    114: ("123 kcal", "Sulfiți"),   # Solo Quinta — Recaș
    115: ("150 kcal", "Sulfiți"),   # Tămâioasă Românească dulce — Stirbey

    # ── VINURI ROȘII (≈150ml glass unless stated) ─────────────────────────────
    116: ("154 kcal", "Sulfiți"),   # Corcova cupaj (187ml)
    117: ("127 kcal", "Sulfiți"),   # Organic Fetească Neagră — Domeniul Bogdan
    118: ("127 kcal", "Sulfiți"),   # Implicit Merlot — Recaș
    119: ("127 kcal", "Sulfiți"),   # Terra Romana Fetească Neagră — S.E.R.V.E.
    120: ("127 kcal", "Sulfiți"),   # Arezan Merlot — M1 Murfatlar
    121: ("127 kcal", "Sulfiți"),   # Liliac Cuvée Red — Lechința
    122: ("127 kcal", "Sulfiți"),   # Trois Amis — Domeniile la Migdali
    123: ("127 kcal", "Sulfiți"),   # Cabernet Sauvignon — Bauer
    124: ("127 kcal", "Sulfiți"),   # Prince Matei Rezerva — Domeniile Matei
    125: ("127 kcal", "Sulfiți"),   # Cuvée Uberland — Recaș
    126: ("127 kcal", "Sulfiți"),   # Lupi — Gitana Moldova
    127: ("180 kcal", "Sulfiți"),   # Vin fiert (200ml) — mulled wine + spices + sugar
}

updated = 0
skipped = []

for item_id, (calories, allergens) in data.items():
    try:
        item = MenuItem.objects.get(id=item_id)
        item.calories = calories
        item.allergens = allergens if allergens else None
        item.save(update_fields=["calories", "allergens"])
        allergen_display = allergens if allergens else "—"
        print(f"  ✓ [{item_id:3d}] {item.name[:50]:<50}  {calories:<22} {allergen_display}")
        updated += 1
    except MenuItem.DoesNotExist:
        skipped.append(item_id)
        print(f"  ✗ [{item_id:3d}] NOT FOUND in database")

# Flag any items we didn't map
unhandled = MenuItem.objects.exclude(id__in=data.keys())
for item in unhandled:
    print(f"  ⚠ [{item.id:3d}] UNHANDLED — {item.name}")

print(f"\n{'─'*70}")
print(f"  Updated : {updated}")
print(f"  Not found: {len(skipped)} (IDs: {skipped})")
print(f"  Unhandled: {unhandled.count()}")
