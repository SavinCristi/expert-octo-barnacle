from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_PENDING   = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING,   'În Așteptare'),
        (STATUS_CONFIRMED, 'Confirmat'),
        (STATUS_CANCELLED, 'Anulat'),
    ]

    name   = models.CharField(max_length=200)
    phone  = models.CharField(max_length=20)
    email  = models.EmailField()
    date   = models.DateField()
    time   = models.TimeField()
    guests = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    def __str__(self):
        return f'{self.name} — {self.date} {self.time}'


class EventInquiry(models.Model):
    TYPE_WEDDING   = 'wedding'
    TYPE_CORPORATE = 'corporate'
    TYPE_PARTY     = 'party'
    TYPE_OTHER     = 'other'
    TYPE_CHOICES = [
        (TYPE_WEDDING,   'Nuntă'),
        (TYPE_CORPORATE, 'Corporate'),
        (TYPE_PARTY,     'Petrecere Privată'),
        (TYPE_OTHER,     'Altceva'),
    ]

    STATUS_NEW       = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_CLOSED    = 'closed'
    STATUS_CHOICES = [
        (STATUS_NEW,       'Nou'),
        (STATUS_CONTACTED, 'Contactat'),
        (STATUS_CLOSED,    'Închis'),
    ]

    name             = models.CharField(max_length=200)
    phone            = models.CharField(max_length=20)
    email            = models.EmailField()
    desired_date     = models.DateField()
    event_type       = models.CharField(max_length=20, choices=TYPE_CHOICES)
    estimated_guests = models.PositiveSmallIntegerField()
    message          = models.TextField(blank=True)
    status           = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering        = ['-created_at']
        verbose_name    = 'Event Inquiry'
        verbose_name_plural = 'Event Inquiries'

    def __str__(self):
        return f'{self.name} — {self.get_event_type_display()} · {self.desired_date}'
