from django.contrib import admin

from .models import MenuItem, Reservation


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'guests')
    list_filter = ('date',)
    search_fields = ('name', 'phone')
