import pytest
from datetime import date
from reservations.models import (
    Restaurant, TableType, MenuItem, Reservation, ReservationGuest, ReservationStatus
)



def test_restaurant_str():
    r = Restaurant(name="Test Rest")
    assert str(r) == "Test Rest"

def test_table_type_str():
    r = Restaurant(name="Test Rest")
    tt = TableType(restaurant=r, name="VIP")
    assert str(tt) == "VIP - Test Rest"

def test_menu_item_str():
    r = Restaurant(name="Test Rest")
    m = MenuItem(restaurant=r, name="Burger", price=10.0)
    assert str(m) == "Burger"

def test_reservation_str():
    r = Restaurant(name="Test Rest")
    tt = TableType(restaurant=r, name="VIP")
    rs = ReservationStatus(name="CONFIRMED")
    res = Reservation(
        restaurant=r, 
        table_type=tt, 
        status=rs,
        reservation_date=date(2026, 1, 1),
        customer_name="Alice"
    )
    assert str(res) == "Reservation Alice (2026-01-01)"

def test_reservation_guest_str():
    r = Restaurant(name="Test Rest")
    tt = TableType(restaurant=r, name="VIP")
    rs = ReservationStatus(name="CONFIRMED")
    res = Reservation(
        restaurant=r, 
        table_type=tt, 
        status=rs,
        reservation_date=date(2026, 1, 1),
        customer_name="Alice"
    )
    g = ReservationGuest(reservation=res, full_name="Bob")
    assert str(g) == "Bob"
