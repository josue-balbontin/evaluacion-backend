
import random
import uuid
from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from reservations.models import (
    Restaurant, TableType, PricingTier, MenuItem,
    ReservationStatus, Reservation, ReservationGuest,
)


class Command(BaseCommand):
    help = 'Seed database with 300+ reservations and 500+ guests'

    def handle(self, *args, **options):

        if Reservation.objects.exists():
            self.stdout.write(self.style.WARNING('Data already seeded. Skipping.'))
            return

        self.stdout.write('Seeding data...')

        status_names = ['pending', 'confirmed', 'seated', 'completed', 'cancelled', 'no_show']
        statuses = {}
        for name in status_names:
            status, _ = ReservationStatus.objects.get_or_create(name=name)
            statuses[name] = status

 
        restaurants = []
        restaurant_data = [
            ('The Golden Fork', 'the-golden-fork', 'Fine dining experience', '123 Main St', '+1-555-0101', 'America/New_York'),
            ('Sakura Garden', 'sakura-garden', 'Authentic Japanese cuisine', '456 Oak Ave', '+1-555-0102', 'America/Los_Angeles'),
            ('La Trattoria', 'la-trattoria', 'Italian comfort food', '789 Pine Rd', '+1-555-0103', 'Europe/Rome'),
            ('Spice Route', 'spice-route', 'Indian fusion restaurant', '321 Elm St', '+1-555-0104', 'Asia/Kolkata'),
            ('Le Petit Bistro', 'le-petit-bistro', 'French bistro classics', '654 Maple Dr', '+1-555-0105', 'Europe/Paris'),
        ]
        for name, slug, desc, addr, phone, tz in restaurant_data:
            r = Restaurant.objects.create(
                name=name, slug=slug, description=desc,
                address=addr, phone=phone, timezone=tz,
                opening_time=time(8, 0), closing_time=time(23, 0),
            )
            restaurants.append(r)


        table_type_templates = [
            ('Bar Stool', 'Seating at the bar counter', 1, 8, Decimal('10.00')),
            ('Standard 2-Seat', 'Cozy table for two', 2, 15, Decimal('15.00')),
            ('Standard 4-Seat', 'Classic four-person table', 4, 10, Decimal('12.50')),
            ('Family 6-Seat', 'Large family table', 6, 6, Decimal('11.00')),
            ('VIP Booth', 'Private booth for special occasions', 4, 3, Decimal('35.00')),
            ('Patio 4-Seat', 'Outdoor seating', 4, 8, Decimal('14.00')),
        ]
        all_table_types = []
        for restaurant in restaurants:
            for name, desc, seats, qty, price in table_type_templates:
                tt = TableType.objects.create(
                    restaurant=restaurant, name=name, description=desc,
                    seats=seats, quantity=qty, price_per_seat=price,
                )
                all_table_types.append(tt)


        tier_names = ['Happy Hour', 'Weekend Premium', 'Holiday Special', 'Early Bird']
        for tt in all_table_types[:10]:
            for i, tier_name in enumerate(random.sample(tier_names, k=random.randint(1, 2))):
                PricingTier.objects.create(
                    table_type=tt,
                    name=tier_name,
                    price_per_seat=tt.price_per_seat * Decimal(str(random.uniform(0.7, 1.5))),
                    priority=i,
                    valid_from=None,
                    valid_until=None,
                )


        courses = ['Appetizer', 'Main', 'Dessert', 'Drink', 'Side']
        dish_names = {
            'Appetizer': ['Bruschetta', 'Spring Rolls', 'Soup of the Day', 'Caesar Salad', 'Garlic Bread'],
            'Main': ['Grilled Salmon', 'Beef Tenderloin', 'Pasta Carbonara', 'Chicken Tikka', 'Ratatouille'],
            'Dessert': ['Tiramisu', 'Creme Brulee', 'Chocolate Mousse', 'Cheesecake', 'Mochi Ice Cream'],
            'Drink': ['House Wine', 'Craft Beer', 'Fresh Lemonade', 'Espresso', 'Green Tea'],
            'Side': ['French Fries', 'Steamed Rice', 'Mixed Salad', 'Mashed Potatoes', 'Grilled Vegetables'],
        }
        allergen_options = ['gluten', 'dairy', 'nuts', 'shellfish', 'soy', 'eggs']

        for restaurant in restaurants:
            for course in courses:
                for dish in dish_names[course]:
                    MenuItem.objects.create(
                        restaurant=restaurant,
                        name=dish,
                        description=f'Our signature {dish.lower()}',
                        course=course,
                        price=Decimal(str(round(random.uniform(5.0, 45.0), 2))),
                        allergens=random.sample(allergen_options, k=random.randint(0, 2)),
                        is_available=random.random() > 0.1,
                    )


        first_names = ['James', 'Maria', 'John', 'Ana', 'Robert', 'Sofia', 'David', 'Emma',
                       'Carlos', 'Olivia', 'Miguel', 'Liam', 'Chen', 'Yuki', 'Ahmed', 'Fatima',
                       'Pierre', 'Ingrid', 'Hans', 'Lucia']
        last_names = ['Smith', 'Garcia', 'Johnson', 'Martinez', 'Brown', 'Lopez', 'Wilson',
                      'Lee', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'White', 'Harris']

        active_statuses = [statuses['pending'], statuses['confirmed'], statuses['seated'], statuses['completed']]
        all_statuses = list(statuses.values())

        today = date.today()
        reservations = []
        for i in range(300):
            restaurant = random.choice(restaurants)
            restaurant_tables = [tt for tt in all_table_types if tt.restaurant_id == restaurant.id]
            table_type = random.choice(restaurant_tables)

            first = random.choice(first_names)
            last = random.choice(last_names)
            customer_name = f'{first} {last}'

 
            delta = random.randint(-30, 30)
            res_date = today + timedelta(days=delta)


            hour = random.randint(11, 21)
            minute = random.choice([0, 15, 30, 45])

            status = random.choice(active_statuses) if delta >= 0 else random.choice(all_statuses)

            reservation = Reservation(
                restaurant=restaurant,
                table_type=table_type,
                status=status,
                reservation_date=res_date,
                reservation_time=time(hour, minute),
                party_size=random.randint(1, table_type.seats),
                customer_name=customer_name,
                customer_email=f'{first.lower()}.{last.lower()}@example.com',
                customer_phone=f'+1-555-{random.randint(1000,9999)}',
                notes=random.choice(['', '', '', 'Birthday celebration', 'Anniversary', 'Window seat preferred', 'Allergies - check notes']),
            )
            reservations.append(reservation)

        Reservation.objects.bulk_create(reservations)
        self.stdout.write(f'  Created {len(reservations)} reservations')


        created_reservations = list(Reservation.objects.all())
        guests = []
        batch_size = 5000
        
        self.stdout.write('Generating guests...')
        for idx, reservation in enumerate(created_reservations):
            for j in range(500):
                first = random.choice(first_names)
                last = random.choice(last_names)
                guests.append(ReservationGuest(
                    reservation=reservation,
                    full_name=f'{first} {last}',
                    email=f'{first.lower()}.{last.lower()}{random.randint(1,99999)}@example.com',
                    phone=f'+1-555-{random.randint(1000,9999)}',
                    dietary_notes=random.choice(['', '', '', 'Vegetarian', 'Vegan', 'Gluten-free', 'No dairy']),
                    is_primary=(j == 0),
                ))
            
            if len(guests) >= batch_size:
                ReservationGuest.objects.bulk_create(guests)
                guests = []
                self.stdout.write(f'  Created { (idx + 1) * 500 } guests so far...')

        if guests:
            ReservationGuest.objects.bulk_create(guests)

        self.stdout.write('  Created 150000 guests')

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete: {len(restaurants)} restaurants, '
            f'{len(all_table_types)} table types, '
            f'{len(reservations)} reservations, '
            f'{len(guests)} guests.'
        ))
