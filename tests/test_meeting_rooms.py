"""
Unit Tests for Meeting Room Booking & Conflict Prevention Engine
"""

import pytest
from db.database import get_meeting_rooms, book_room, get_room_bookings, execute_update

def test_meeting_rooms_exist():
    rooms = get_meeting_rooms()
    assert len(rooms) >= 4
    assert any(r["name"] == "Synergy Boardroom" for r in rooms)

def test_room_booking_conflict_prevention():
    # Attempt booking at time slot that already exists
    # Seed data has Synergy Boardroom booked 2026-11-10 10:00 to 12:00
    res_conflict = book_room(
        room_id=1,
        user_id=1,
        title="Overlapping Meeting",
        start_time="2026-11-10 10:30",
        end_time="2026-11-10 11:30"
    )
    assert res_conflict["success"] is False
    assert "conflicts" in res_conflict["error"]

    # Clean up any previous test booking to ensure idempotency
    execute_update("DELETE FROM room_bookings WHERE title = 'Evening Sync'")
    # Book a valid non-overlapping slot
    res_success = book_room(
        room_id=1,
        user_id=1,
        title="Evening Sync",
        start_time="2026-11-10 18:00",
        end_time="2026-11-10 19:00"
    )
    assert res_success["success"] is True
