from django.contrib import admin
from .models import (
    Restaurant, TableType, PricingTier, MenuItem,
    ReservationStatus, Reservation, ReservationGuest,
)


class ReservationGuestInline(admin.TabularInline):
    model = ReservationGuest
    extra = 1
    fields = ('full_name', 'email', 'phone', 'dietary_notes', 'is_primary')
    readonly_fields = ('created', 'modified')


class PricingTierInline(admin.TabularInline):
    model = PricingTier
    extra = 1
    fields = ('name', 'price_per_seat', 'priority', 'valid_from', 'valid_until', 'is_active')


class TableTypeInline(admin.TabularInline):
    model = TableType
    extra = 1
    fields = ('name', 'seats', 'quantity', 'price_per_seat', 'is_active')


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'course', 'price', 'is_available')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'phone', 'opening_time', 'closing_time', 'is_active')
    search_fields = ('name', 'slug', 'address')
    list_filter = ('is_active', 'timezone')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'modified')
    inlines = [TableTypeInline, MenuItemInline]


@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'seats', 'quantity', 'price_per_seat', 'is_active')
    list_filter = ('restaurant', 'is_active')
    search_fields = ('name', 'restaurant__name')
    readonly_fields = ('created', 'modified')
    inlines = [PricingTierInline]


@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'table_type', 'price_per_seat', 'priority', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('table_type__restaurant', 'is_active')
    search_fields = ('name', 'table_type__name')
    readonly_fields = ('created', 'modified')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'course', 'price', 'is_available')
    list_filter = ('restaurant', 'course', 'is_available')
    search_fields = ('name', 'description')
    readonly_fields = ('created', 'modified')

@admin.register(ReservationStatus)
class ReservationStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')
    search_fields = ('name',)
    readonly_fields = ('created', 'modified')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'reservation_date', 'reservation_time', 'restaurant', 'table_type', 'status', 'party_size')
    list_filter = ('restaurant', 'status', 'reservation_date', 'table_type')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created', 'modified')
    inlines = [ReservationGuestInline]
    ordering = ('-reservation_date', '-reservation_time')


@admin.register(ReservationGuest)
class ReservationGuestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'reservation', 'email', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('full_name', 'email')
    readonly_fields = ('created', 'modified')
