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
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name} — {self.date} {self.time}'
