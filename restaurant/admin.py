from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import EventInquiry, MenuItem, Reservation


@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display       = ('sort_order', 'name', 'name_en', 'category', 'price', 'weight', 'allergens')
    list_display_links = ('name',)
    list_filter        = ('category',)
    search_fields      = ('name', 'name_en')
    ordering           = ('sort_order',)
    fieldsets = (
        (None, {'fields': ('category', 'price', 'weight', 'calories', 'allergens', 'image')}),
        ('Romanian', {'fields': ('name', 'description')}),
        ('English', {'fields': ('name_en', 'description_en')}),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'date', 'time', 'guests', 'status')
    list_filter   = ('status', 'date')
    search_fields = ('name', 'phone', 'email')
    list_editable = ('status',)


@admin.register(EventInquiry)
class EventInquiryAdmin(admin.ModelAdmin):
    list_display   = ('name', 'event_type', 'desired_date', 'estimated_guests', 'status', 'created_at')
    list_filter    = ('status', 'event_type')
    search_fields  = ('name', 'phone', 'email')
    list_editable  = ('status',)
    readonly_fields = ('created_at',)
