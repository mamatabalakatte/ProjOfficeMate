"""
Page 9: Meeting Room Booking & Scheduling
Interactive room availability, equipment amenities, booking calendar, and conflict prevention.
"""

import streamlit as st
from datetime import datetime, date, time
from db.database import get_meeting_rooms, get_room_bookings, book_room
from frontend.components.illustrations import render_banner_picture, get_room_thumbnail

st.set_page_config(page_title="Meeting Room Booking | OfficeMate 2.0", page_icon="📅", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #6D28D9 0%, #8B5CF6 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">📅 Meeting Room Booking &amp; Calendar</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      Reserve conference rooms, view capacity &amp; AV equipment, with real-time double-booking prevention.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it" style="background: white; color: #6D28D9;">Smart Collision Guard</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Synergy Boardroom Hero Banner
render_banner_picture("boardroom.png", caption="📅 Synergy Boardrooms & Conference Suites • Conflict-Free Engine")
st.write("")

rooms = get_meeting_rooms()

# Room Cards Row
st.subheader("🏢 Available Meeting Spaces")
cols = st.columns(len(rooms))
for i, room in enumerate(rooms):
    with cols[i]:
        thumb = get_room_thumbnail(room['name'])
        st.markdown(f"""
        <div class="om-card" style="height: 100%;">
          {thumb}
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top: 6px;">
            <strong style="color: #6D28D9;">{room['name']}</strong>
            <span class="om-badge badge-success">Active</span>
          </div>
          <div style="font-size: 0.85rem; color: #475569; margin: 6px 0;">
            📍 {room['floor']} • 👥 Capacity: <strong>{room['capacity']} people</strong>
          </div>
          <div style="font-size: 0.78rem; color: #64748B; background: #F1F5F9; padding: 6px 8px; border-radius: 6px;">
            🎛️ {room['amenities']}
          </div>
        </div>
        """, unsafe_allow_html=True)

st.write("")
col_book, col_cal = st.columns([1, 1])

with col_book:
    st.subheader("📝 Reserve a Meeting Room")
    with st.form("book_room_form"):
        selected_room_name = st.selectbox("Select Conference Room", [r["name"] for r in rooms])
        selected_room_id = [r["id"] for r in rooms if r["name"] == selected_room_name][0]
        meeting_title = st.text_input("Meeting Purpose / Title", placeholder="e.g. Q4 Strategy Sync")
        
        book_date = st.date_input("Meeting Date", value=date.today())
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            start_hour = st.selectbox("Start Time", ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"], index=3)
        with col_t2:
            end_hour = st.selectbox("End Time", ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"], index=4)

        attendees = st.number_input("Expected Attendees", min_value=1, max_value=25, value=4)
        
        book_submit = st.form_submit_button("📅 Confirm Reservation", use_container_width=True)
        if book_submit:
            start_iso = f"{book_date} {start_hour}"
            end_iso = f"{book_date} {end_hour}"
            
            if start_hour >= end_hour:
                st.error("End time must be later than start time.")
            else:
                res = book_room(selected_room_id, user_id=1, title=meeting_title, start_time=start_iso, end_time=end_iso, attendees_count=attendees)
                if not res["success"]:
                    st.error(f"❌ Booking Conflict: {res['error']}")
                else:
                    st.success(f"🎉 Reserved {selected_room_name} for '{meeting_title}' on {start_iso}!")
                    st.rerun()

with col_cal:
    st.subheader("🗓️ Scheduled Bookings Calendar")
    bookings = get_room_bookings()
    if not bookings:
        st.info("No active reservations found.")
    else:
        for b in bookings:
            st.markdown(f"""
            <div class="om-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color: #6D28D9;">{b['room_name']}</strong>
                <span class="om-badge badge-open">Confirmed</span>
              </div>
              <h5 style="margin: 6px 0 2px 0;">{b['title']}</h5>
              <div style="font-size: 0.82rem; color: #64748B;">
                ⏰ <strong>{b['start_time']}</strong> to <strong>{b['end_time']}</strong><br>
                👤 Booked by: {b['organizer_name']} • 👥 {b['attendees_count']} attendees
              </div>
            </div>
            """, unsafe_allow_html=True)
