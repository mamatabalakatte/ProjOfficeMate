"""
Active User Context and Persona Management for OfficeMate 2.0
Enables persona switching (Employee, HR Specialist, IT Support, Admin Lead)
and consistent user identity tracking across all workplace hubs.
"""

import streamlit as st
from db.database import query_all, query_one
from frontend.components.avatars import render_employee_badge

def get_active_user():
    """Retrieves the currently authenticated / active user persona from session state."""
    if "active_user_id" not in st.session_state:
        st.session_state["active_user_id"] = 1  # Default: Alex Chen (Software Engineer)

    user_id = st.session_state["active_user_id"]
    user = query_one(
        """SELECT u.*, d.name as dept_name, d.code as dept_code 
           FROM users u 
           LEFT JOIN departments d ON u.department_id = d.id 
           WHERE u.id = ?""",
        (user_id,)
    )
    if not user:
        user = {
            "id": 1,
            "username": "alex.chen",
            "full_name": "Alex Chen",
            "role": "employee",
            "email": "alex.chen@officemate.internal",
            "department_id": 2,
            "dept_name": "Information Technology",
            "dept_code": "IT",
            "status": "available"
        }
    return user

def get_all_users():
    """Returns all workplace users with their roles and department codes."""
    return query_all(
        """SELECT u.id, u.full_name, u.role, u.email, d.name as dept_name, d.code as dept_code 
           FROM users u 
           LEFT JOIN departments d ON u.department_id = d.id 
           ORDER BY u.id"""
    )

def get_support_agents():
    """Returns users with support_agent or admin roles who handle tickets."""
    return query_all(
        """SELECT u.id, u.full_name, u.role, d.code as dept_code 
           FROM users u 
           LEFT JOIN departments d ON u.department_id = d.id 
           WHERE u.role IN ('support_agent', 'admin') 
           ORDER BY u.id"""
    )

def render_user_profile_sidebar():
    """Renders the active persona card and persona switcher dropdown in the Streamlit sidebar."""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 6px 0;">
      <h2 style="margin:0; font-size: 1.4rem; color: #4F46E5; font-weight: 800;">🏢 OfficeMate 2.0</h2>
      <div style="font-size: 0.78rem; color: #64748B; font-weight: 600;">The Intelligent Virtual Workplace</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 Active Persona")

    users = get_all_users()
    user_map = {
        u["id"]: f"{u['full_name']} ({u['role'].replace('_', ' ').title()} • {u['dept_code']})"
        for u in users
    }

    current_id = st.session_state.get("active_user_id", 1)
    if current_id not in user_map:
        current_id = 1
        st.session_state["active_user_id"] = 1

    ids = list(user_map.keys())
    sel_idx = ids.index(current_id)

    new_user_id = st.sidebar.selectbox(
        "Logged in as (Switch Persona):",
        options=ids,
        format_func=lambda x: user_map[x],
        index=sel_idx,
        key="persona_switcher_dropdown"
    )

    if new_user_id != current_id:
        st.session_state["active_user_id"] = new_user_id
        st.rerun()

    active_user = get_active_user()
    role_label = f"{active_user['role'].replace('_', ' ').title()} • {active_user.get('dept_code', 'IT')}"
    st.sidebar.markdown(
        render_employee_badge(
            active_user["full_name"],
            role_label,
            active_user.get("status", "available")
        ),
        unsafe_allow_html=True
    )
