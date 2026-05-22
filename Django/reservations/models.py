import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField  # Necesario para el campo TEXT[] de allergens

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    address = models.CharField(max_length=500, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(max_length=254, blank=True, default='')
    website = models.URLField(max_length=500, blank=True, default='')
    opening_time = models.TimeField(default='08:00:00')
    closing_time = models.TimeField(default='23:00:00')
    timezone = models.CharField(max_length=63, default='UTC')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."restaurant"'
    
    def __str__(self):
        return self.name

class TableType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='table_types')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default='')
    seats = models.IntegerField()
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."table_type"'

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    course = models.CharField(max_length=60, default='Main')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ArrayField nativo de Postgres mapeado a TEXT[] en tu DDL
    allergens = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."menu_item"'

    def __str__(self):
        return self.name

class PricingTier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name='pricing_tiers')
    name = models.CharField(max_length=120)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.IntegerField(default=0)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."pricing_tier"'

    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.IntegerField()
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=254, blank=True, default='')
    customer_phone = models.CharField(max_length=30, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."reservation"'

    def __str__(self):
        return f"Reserva de {self.customer_name} ({self.reservation_date})"

class ReservationGuest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    dietary_notes = models.TextField(blank=True, default='')
    is_primary = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"content"."reservation_guest"'

    def __str__(self):
        return self.full_name