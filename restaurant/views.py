import datetime
from collections import defaultdict

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import EventInquiry, MenuItem, Reservation

FOOD_CATEGORIES = [
    "Antreuri",
    "Ciorbe",
    "Feluri principale",
    "Garnituri",
    "Salate",
    "Deserturi",
]

DRINK_CATEGORIES = [
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

CATEGORY_ORDER = FOOD_CATEGORIES + DRINK_CATEGORIES

CATEGORY_SLUG = {
    "Antreuri":          "antreuri",
    "Ciorbe":            "ciorbe",
    "Feluri principale": "feluri-principale",
    "Garnituri":         "garnituri",
    "Salate":            "salate",
    "Deserturi":         "deserturi",
    "Răcoritoare":       "racoritoare",
    "Energizante":       "energizante",
    "Cafea & Ceai":      "cafea-ceai",
    "Bere":              "bere",
    "Alcool":            "alcool",
    "Vin spumant":       "vin-spumant",
    "Vinuri roze":       "vinuri-roze",
    "Vinuri albe":       "vinuri-albe",
    "Vinuri roșii":      "vinuri-rosii",
}

EVENT_TYPE_LABELS = {
    EventInquiry.TYPE_WEDDING:   'Nuntă',
    EventInquiry.TYPE_CORPORATE: 'Corporate',
    EventInquiry.TYPE_PARTY:     'Petrecere Privată',
    EventInquiry.TYPE_OTHER:     'Altceva',
}


def home(request):
    grouped = defaultdict(list)
    for item in MenuItem.objects.all().order_by("category", "name"):
        grouped[item.category].append(item)

    menu_sections = []
    for cat in CATEGORY_ORDER:
        if cat in grouped:
            main_cat = "mancare" if cat in FOOD_CATEGORIES else "bautura"
            menu_sections.append((cat, grouped[cat], main_cat, CATEGORY_SLUG[cat]))

    for cat, items in grouped.items():
        if cat not in CATEGORY_ORDER:
            menu_sections.append((cat, items, "mancare", cat.lower().replace(" ", "-")))

    return render(request, "home.html", {"menu_sections": menu_sections})


@require_POST
def reserve(request):
    name   = request.POST.get('name',   '').strip()
    phone  = request.POST.get('phone',  '').strip()
    email  = request.POST.get('email',  '').strip()
    date_s = request.POST.get('date',   '').strip()
    time_s = request.POST.get('time',   '').strip()
    guests = request.POST.get('guests', '').strip()

    if not all([name, phone, email, date_s, time_s, guests]):
        return JsonResponse(
            {'ok': False, 'error': 'Toate câmpurile sunt obligatorii.'},
            status=400,
        )

    try:
        parsed_date = datetime.date.fromisoformat(date_s)
        for fmt in ('%H:%M', '%H:%M:%S'):
            try:
                parsed_time = datetime.datetime.strptime(time_s, fmt).time()
                break
            except ValueError:
                pass
        else:
            raise ValueError(f'unrecognised time: {time_s!r}')
        guests_int  = int(guests)
    except (ValueError, TypeError):
        return JsonResponse(
            {'ok': False, 'error': 'Format dată, oră sau număr de persoane invalid.'},
            status=400,
        )

    reservation = Reservation.objects.create(
        name=name, phone=phone, email=email,
        date=parsed_date, time=parsed_time, guests=guests_int,
    )

    send_mail(
        subject=f'[Vânătorul] Rezervare nouă — {name} · {date_s} {time_s}',
        message=(
            f'O nouă cerere de rezervare a fost primită pe site:\n\n'
            f'  Nume:     {name}\n'
            f'  Telefon:  {phone}\n'
            f'  Email:    {email}\n'
            f'  Data:     {date_s}\n'
            f'  Ora:      {time_s}\n'
            f'  Persoane: {guests_int}\n\n'
            f'  Status:       În Așteptare\n'
            f'  ID rezervare: #{reservation.id}\n\n'
            f'Confirmați sau anulați rezervarea din panoul de administrare:\n'
            f'{settings.SITE_URL}/admin/restaurant/reservation/{reservation.id}/change/'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['Office@restaurant-vanatorul.ro'],
        fail_silently=True,
    )

    return JsonResponse({'ok': True})


@require_POST
def event_inquiry(request):
    name       = request.POST.get('name',             '').strip()
    phone      = request.POST.get('phone',            '').strip()
    email      = request.POST.get('email',            '').strip()
    date_s     = request.POST.get('desired_date',     '').strip()
    event_type = request.POST.get('event_type',       '').strip()
    guests_s   = request.POST.get('estimated_guests', '').strip()
    message    = request.POST.get('message',          '').strip()

    if not all([name, phone, email, date_s, event_type, guests_s]):
        return JsonResponse(
            {'ok': False, 'error': 'Toate câmpurile obligatorii trebuie completate.'},
            status=400,
        )

    valid_types = {c[0] for c in EventInquiry.TYPE_CHOICES}
    if event_type not in valid_types:
        return JsonResponse(
            {'ok': False, 'error': 'Tip de eveniment invalid.'},
            status=400,
        )

    try:
        parsed_date = datetime.date.fromisoformat(date_s)
        guests_int  = int(guests_s)
        if guests_int < 1:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse(
            {'ok': False, 'error': 'Format dată sau număr de persoane invalid.'},
            status=400,
        )

    inquiry = EventInquiry.objects.create(
        name=name,
        phone=phone,
        email=email,
        desired_date=parsed_date,
        event_type=event_type,
        estimated_guests=guests_int,
        message=message,
    )

    event_label = EVENT_TYPE_LABELS.get(event_type, event_type)

    send_mail(
        subject=f'NOUA CERERE EVENIMENT: {name}',
        message=(
            f'O nouă cerere de eveniment a fost primită pe site:\n\n'
            f'  Nume:           {name}\n'
            f'  Telefon:        {phone}\n'
            f'  Email:          {email}\n'
            f'  Data dorită:    {date_s}\n'
            f'  Tip eveniment:  {event_label}\n'
            f'  Nr. persoane:   {guests_int}\n'
            f'  Detalii:        {message or "—"}\n\n'
            f'  Status:    Nou\n'
            f'  ID cerere: #{inquiry.id}\n\n'
            f'Vizualizați cererea în panoul de administrare:\n'
            f'{settings.SITE_URL}/admin/restaurant/eventinquiry/{inquiry.id}/change/'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['Office@restaurant-vanatorul.ro'],
        fail_silently=True,
    )

    return JsonResponse({'ok': True})
