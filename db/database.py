"""
Database Management Module for OfficeMate 2.0
Supports SQLite with WAL mode for fast concurrent read/write operations.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "officemate.db")

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database with WAL mode."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db(schema_path: Optional[str] = None) -> None:
    """Initializes the database using the schema.sql file."""
    if schema_path is None:
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
        
    with get_db_connection() as conn:
        conn.executescript(schema_sql)
        conn.commit()

# --- Query Helpers ---

def query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def query_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

def execute_insert(query: str, params: tuple = ()) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def execute_update(query: str, params: tuple = ()) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

# --- Ticket Operations ---

def get_tickets(department: Optional[str] = None, status: Optional[str] = None, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
    query = """
        SELECT t.*, d.name as department_name, d.code as department_code, 
               u.full_name as creator_name, a.full_name as assignee_name
        FROM tickets t
        JOIN departments d ON t.department_id = d.id
        JOIN users u ON t.created_by = u.id
        LEFT JOIN users a ON t.assigned_to = a.id
        WHERE 1=1
    """
    params = []
    if department:
        query += " AND (d.code = ? OR d.name = ?)"
        params.extend([department, department])
    if status:
        query += " AND t.status = ?"
        params.append(status)
    if user_id:
        query += " AND t.created_by = ?"
        params.append(user_id)
        
    query += " ORDER BY t.created_at DESC"
    return query_all(query, tuple(params))

def create_ticket(title: str, description: str, department_code: str, priority: str = "MEDIUM", 
                  created_by: int = 1, sentiment: str = "neutral") -> Dict[str, Any]:
    # Lookup department id
    dept = query_one("SELECT id, code FROM departments WHERE code = ? OR name = ?", (department_code, department_code))
    if not dept:
        dept_id = 1
        dept_code = "GEN"
    else:
        dept_id = dept["id"]
        dept_code = dept["code"]

    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    count_today = query_one("SELECT COUNT(*) as count FROM tickets WHERE ticket_code LIKE ?", (f"TKT-{dept_code}-{date_str}-%",))["count"]
    ticket_code = f"TKT-{dept_code}-{date_str}-{count_today + 1:03d}"

    ticket_id = execute_insert(
        """INSERT INTO tickets (ticket_code, title, description, department_id, priority, status, created_by, sentiment, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'OPEN', ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
        (ticket_code, title, description, dept_id, priority, created_by, sentiment)
    )

    # Insert history record
    execute_insert(
        """INSERT INTO ticket_history (ticket_id, actor_id, previous_status, new_status, notes)
           VALUES (?, ?, NULL, 'OPEN', 'Ticket automatically opened')""",
        (ticket_id, created_by)
    )

    # Log audit
    log_audit(created_by, "CREATE_TICKET", f"tickets:{ticket_id}", f"Created ticket {ticket_code}")

    return query_one("SELECT * FROM tickets WHERE id = ?", (ticket_id,))

def update_ticket_status(ticket_id: int, new_status: str, actor_id: int, notes: str = "", assigned_to: Optional[int] = None) -> bool:
    t = query_one("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    if not t:
        return False
    prev_status = t["status"]
    if assigned_to is not None:
        execute_update(
            "UPDATE tickets SET status = ?, resolution_notes = ?, assigned_to = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_status, notes if notes else t["resolution_notes"], assigned_to, ticket_id)
        )
    else:
        execute_update(
            "UPDATE tickets SET status = ?, resolution_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_status, notes if notes else t["resolution_notes"], ticket_id)
        )
    execute_insert(
        "INSERT INTO ticket_history (ticket_id, actor_id, previous_status, new_status, notes) VALUES (?, ?, ?, ?, ?)",
        (ticket_id, actor_id, prev_status, new_status, notes)
    )
    log_audit(actor_id, "UPDATE_TICKET_STATUS", f"tickets:{ticket_id}", f"Changed status from {prev_status} to {new_status}")
    return True

def assign_ticket(ticket_id: int, assignee_id: Optional[int], actor_id: int) -> bool:
    execute_update("UPDATE tickets SET assigned_to = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (assignee_id, ticket_id))
    log_audit(actor_id, "ASSIGN_TICKET", f"tickets:{ticket_id}", f"Assigned ticket to user ID {assignee_id}")
    return True

# --- Meeting Rooms ---

def get_meeting_rooms() -> List[Dict[str, Any]]:
    return query_all("SELECT * FROM meeting_rooms ORDER BY floor, name")

def get_room_bookings(date_str: Optional[str] = None) -> List[Dict[str, Any]]:
    query = """
        SELECT b.*, r.name as room_name, r.floor, r.capacity, u.full_name as organizer_name
        FROM room_bookings b
        JOIN meeting_rooms r ON b.room_id = r.id
        JOIN users u ON b.user_id = u.id
        WHERE b.status = 'CONFIRMED'
    """
    params = []
    if date_str:
        query += " AND b.start_time LIKE ?"
        params.append(f"{date_str}%")
    query += " ORDER BY b.start_time ASC"
    return query_all(query, tuple(params))

def book_room(room_id: int, user_id: int, title: str, start_time: str, end_time: str, attendees_count: int = 2) -> Dict[str, Any]:
    # Check for conflict
    conflict = query_one(
        """SELECT * FROM room_bookings 
           WHERE room_id = ? AND status = 'CONFIRMED'
           AND NOT (end_time <= ? OR start_time >= ?)""",
        (room_id, start_time, end_time)
    )
    if conflict:
        return {"success": False, "error": f"Time slot conflicts with existing booking: '{conflict['title']}' ({conflict['start_time']} to {conflict['end_time']})"}

    booking_id = execute_insert(
        """INSERT INTO room_bookings (room_id, user_id, title, start_time, end_time, attendees_count, status)
           VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED')""",
        (room_id, user_id, title, start_time, end_time, attendees_count)
    )
    log_audit(user_id, "BOOK_ROOM", f"room_bookings:{booking_id}", f"Booked room {room_id} for {title}")
    return {"success": True, "booking_id": booking_id}

# --- Knowledge Docs ---

def get_knowledge_docs(category: Optional[str] = None) -> List[Dict[str, Any]]:
    query = "SELECT k.*, d.name as department_name FROM knowledge_docs k LEFT JOIN departments d ON k.department_id = d.id"
    params = []
    if category and category != "All":
        query += " WHERE k.category = ?"
        params.append(category)
    query += " ORDER BY k.title"
    return query_all(query, tuple(params))

# --- Announcements ---

def get_active_announcements() -> List[Dict[str, Any]]:
    return query_all("SELECT a.*, u.full_name as author_name FROM announcements a LEFT JOIN users u ON a.author_id = u.id WHERE a.is_active = 1 ORDER BY a.created_at DESC")

# --- Audit Logging ---

def log_audit(user_id: Optional[int], action: str, target: str, details: str, ip: str = "127.0.0.1") -> None:
    try:
        execute_insert(
            "INSERT INTO audit_logs (user_id, action, target_entity, details, ip_address) VALUES (?, ?, ?, ?, ?)",
            (user_id, action, target, details, ip)
        )
    except Exception as e:
        print(f"Failed to write audit log: {e}")

# --- Employee Tasks (Persistent) ---

def get_user_tasks(user_id: int = 1) -> List[Dict[str, Any]]:
    # Initialize default tasks if none exist
    count = query_one("SELECT COUNT(*) as count FROM employee_tasks WHERE user_id = ?", (user_id,))
    if count and count["count"] == 0:
        default_tasks = [
            (user_id, "Complete OKR quarterly self-reflection", 1),
            (user_id, "Submit monthly phone & internet reimbursement claim", 0),
            (user_id, "RSVP for Annual Company Town Hall & Hackathon", 1),
            (user_id, "Verify Okta MFA backup token configuration", 0)
        ]
        with get_db_connection() as conn:
            conn.executemany("INSERT INTO employee_tasks (user_id, title, is_completed) VALUES (?, ?, ?)", default_tasks)
            conn.commit()

    return query_all("SELECT * FROM employee_tasks WHERE user_id = ? ORDER BY id ASC", (user_id,))

def toggle_task_completion(task_id: int, is_completed: bool) -> bool:
    execute_update("UPDATE employee_tasks SET is_completed = ? WHERE id = ?", (1 if is_completed else 0, task_id))
    return True

def add_user_task(user_id: int, title: str) -> int:
    return execute_insert("INSERT INTO employee_tasks (user_id, title, is_completed) VALUES (?, ?, 0)", (user_id, title))

# --- Policy Conflict Updates ---

def resolve_policy_conflict(conflict_id: int, actor_id: int = 4) -> bool:
    execute_update("UPDATE policy_conflicts SET status = 'RESOLVED' WHERE id = ?", (conflict_id,))
    log_audit(actor_id, "RESOLVE_POLICY_CONFLICT", f"policy_conflicts:{conflict_id}", f"Admin resolved policy conflict #{conflict_id}")
    return True

# --- Chat Feedback Logging ---

def log_chat_feedback(user_id: int, message: str, rating: str) -> bool:
    execute_insert("INSERT INTO chat_feedback (user_id, message_text, feedback_rating) VALUES (?, ?, ?)", (user_id, message, rating))
    return True
