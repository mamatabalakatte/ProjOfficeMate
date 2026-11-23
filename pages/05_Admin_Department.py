"""
Page 5: Administration & Facilities Department
Travel reimbursements, ergonomic supplies, building passes, and office logistics.
"""

import streamlit as st
from db.database import get_tickets, create_ticket, get_knowledge_docs
from frontend.components.illustrations import render_banner_picture
from frontend.components.user_context import get_active_user, render_user_profile_sidebar

st.set_page_config(page_title="Admin & Facilities | OfficeMate 2.0", page_icon="🏢", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
active_user = get_active_user()

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #B45309 0%, #D97706 50%, #F59E0B 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🏢 Administration &amp; Facilities</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      Workplace logistics, travel expense reimbursement, building badges, and ergonomic workstation gear.
    </p>
  </div>
  <div>
    <span class="om-badge badge-admin" style="background: white; color: #B45309;">Department Lead: Marcus Vance</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Admin & Facilities Hero Banner
render_banner_picture("admin_desk.png", caption="🏢 Administration & Workplace Facilities • Travel Claims & Logistics")
st.write("")

tab_calc, tab_req, tab_policies, tab_tickets = st.tabs([
    "💰 Travel Reimbursement Calculator",
    "📦 Request Supplies / Passes",
    "📜 Admin Policies",
    "🎫 Admin Tickets"
])

with tab_calc:
    st.markdown("#### Interactive Business Travel Allowance Calculator")
    st.caption("Calculate eligible per diem and hotel claims according to 2026 Admin Travel Guidelines.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        trip_days = st.slider("Number of Business Travel Days", min_value=1, max_value=30, value=3)
        city_tier = st.selectbox("Destination City Tier", ["Tier-1 ($180 max hotel/night)", "Tier-2 ($120 max hotel/night)"])
        hotel_nightly = st.number_input("Actual Hotel Nightly Rate ($)", min_value=0.0, max_value=500.0, value=165.0)
        cab_fares = st.number_input("Total Taxi / Airport Cab Fares ($)", min_value=0.0, value=75.0)

    with col_c2:
        per_diem_rate = 85.0
        hotel_cap = 180.0 if "Tier-1" in city_tier else 120.0
        allowed_hotel = min(hotel_nightly, hotel_cap) * max(0, trip_days - 1)
        total_per_diem = per_diem_rate * trip_days
        grand_total = total_per_diem + allowed_hotel + cab_fares

        st.markdown(f"""
        <div class="om-card" style="background: #FEF3C7; border-color: #FDE68A;">
          <h4 style="margin:0 0 8px 0; color: #92400E;">Calculated Eligible Reimbursement</h4>
          <div style="font-size: 2.2rem; font-weight: 800; color: #B45309; margin-bottom: 8px;">${grand_total:,.2f}</div>
          <div style="font-size: 0.88rem; color: #78350F; line-height: 1.6;">
            • Per Diem Meals ({trip_days} days @ $85): <strong>${total_per_diem:,.2f}</strong><br>
            • Approved Hotel ({trip_days - 1} nights): <strong>${allowed_hotel:,.2f}</strong><br>
            • Ground Transportation: <strong>${cab_fares:,.2f}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 Auto-Draft Expense Reimbursement Ticket", use_container_width=True):
            t = create_ticket(
                f"Travel Expense Claim: ${grand_total:,.2f} ({trip_days} days)",
                f"Itemized travel reimbursement request for {trip_days} days trip. Total eligible claim: ${grand_total:,.2f}.",
                "ADMIN",
                "MEDIUM",
                created_by=active_user["id"]
            )
            st.success(f"✅ Ticket `{t['ticket_code']}` drafted on behalf of **{active_user['full_name']}** and submitted to Marcus Vance for disbursement review!")

with tab_req:
    st.markdown("#### Facilities & Ergonomic Supplies Requisition")
    with st.form("admin_req_form"):
        req_type = st.selectbox("Request Type", ["Ergonomic Chair / Standing Desk Mount", "Replacement RFID Access Card", "Visitor Guest Parking Pass", "Office Stationery Package", "HVAC / Temperature Adjustment"])
        title = st.text_input("Title / Desk Location", placeholder="e.g. Ergonomic chair adjustment for Desk 42-B")
        desc = st.text_area("Details", placeholder="Provide specifications, guest names, or delivery instructions...")
        priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=1)
        
        submit_admin = st.form_submit_button("🚀 Submit Facilities Request", use_container_width=True)
        if submit_admin:
            if not title or not desc:
                st.error("Please provide both title and details.")
            else:
                ticket = create_ticket(title, desc, "ADMIN", priority, created_by=active_user["id"])
                st.success(f"✅ Requisition Ticket `{ticket['ticket_code']}` opened on behalf of **{active_user['full_name']}**! Marcus Vance has been notified.")

with tab_policies:
    st.markdown("#### Administration & Travel Guidelines")
    docs = get_knowledge_docs(category="ADMIN")
    for doc in docs:
        with st.expander(f"📘 {doc['title']} (v{doc['version']})", expanded=True):
            st.write(doc["content"])
            st.caption(f"Tags: {doc['tags']}")

with tab_tickets:
    st.markdown("#### Active Facilities & Admin Tickets")
    tickets = get_tickets(department="ADMIN")
    for t in tickets:
        p_color = {"CRITICAL": "#EF4444", "HIGH": "#EA580C", "MEDIUM": "#2563EB", "LOW": "#10B981"}.get(t["priority"], "#6B7280")
        st.markdown(f"""
        <div class="om-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; color: #4338CA;">{t['ticket_code']}</span>
            <div>
              <span class="om-badge" style="background: {p_color}20; color: {p_color};">{t['priority']}</span>
              <span class="om-badge badge-admin">{t['status']}</span>
            </div>
          </div>
          <h4 style="margin: 8px 0 4px 0;">{t['title']}</h4>
          <p style="color: #475569; font-size: 0.9rem;">{t['description']}</p>
        </div>
        """, unsafe_allow_html=True)
