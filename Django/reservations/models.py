# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    course = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    allergens = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_available = models.BooleanField(blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    available_until = models.DateField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'menu_item'


class PricingTier(models.Model):
    id = models.UUIDField(primary_key=True)
    table_type = models.ForeignKey('TableType', models.DO_NOTHING)
    name = models.CharField(max_length=120)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.IntegerField(blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'pricing_tier'


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING)
    table_type = models.ForeignKey('TableType', models.DO_NOTHING)
    status = models.ForeignKey('ReservationStatus', models.DO_NOTHING)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.IntegerField()
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=254, blank=True, null=True)
    customer_phone = models.CharField(max_length=30, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'reservation'


class ReservationGuest(models.Model):
    id = models.UUIDField(primary_key=True)
    reservation = models.ForeignKey(Reservation, models.DO_NOTHING)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    dietary_notes = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'reservation_guest'


class ReservationStatus(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=20)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'reservation_status'


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)
    timezone = models.CharField(max_length=63, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'restaurant'


class TableType(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, models.DO_NOTHING)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    seats = models.IntegerField()
    quantity = models.IntegerField(blank=True, null=True)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'table_type'
