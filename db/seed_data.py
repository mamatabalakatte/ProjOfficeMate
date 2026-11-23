"""
Seed Data Script for OfficeMate 2.0
Populates realistic corporate workplace data for demonstration and testing.
"""

from db.database import init_db, get_db_connection, execute_insert
import hashlib

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def seed():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data for fresh seed
    tables = [
        "audit_logs", "room_bookings", "meeting_rooms", "ticket_history",
        "tickets", "chat_messages", "conversations", "announcements",
        "policy_conflicts", "knowledge_docs", "users", "departments"
    ]
    for t in tables:
        cursor.execute(f"DELETE FROM {t}")
    conn.commit()

    # 1. Departments
    cursor.executemany(
        """INSERT INTO departments (id, name, code, head, budget, active_staff, description)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            (1, "Human Resources", "HR", "Sarah Jenkins", 250000.0, 5, "Employee relations, talent acquisition, leave management, and company benefits."),
            (2, "Information Technology", "IT", "Alex Rivera", 450000.0, 8, "Network infrastructure, enterprise software, hardware maintenance, and tech support."),
            (3, "Administration", "ADMIN", "Marcus Vance", 180000.0, 4, "Office facilities, supply chain, travel reimbursements, and asset logistics.")
        ]
    )

    # 2. Users
    pw = hash_pw("officemate123")
    cursor.executemany(
        """INSERT INTO users (id, username, password_hash, full_name, email, department_id, role, avatar, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            (1, "alex.chen", pw, "Alex Chen", "alex.chen@officemate.internal", 2, "employee", "https://api.dicebear.com/7.x/bottts/svg?seed=Alex", "available"),
            (2, "sarah.j", pw, "Sarah Jenkins", "sarah.j@officemate.internal", 1, "support_agent", "https://api.dicebear.com/7.x/bottts/svg?seed=Sarah", "available"),
            (3, "david.it", pw, "David Kim", "david.kim@officemate.internal", 2, "support_agent", "https://api.dicebear.com/7.x/bottts/svg?seed=David", "in_meeting"),
            (4, "marcus.v", pw, "Marcus Vance", "marcus.v@officemate.internal", 3, "admin", "https://api.dicebear.com/7.x/bottts/svg?seed=Marcus", "available"),
            (5, "priya.sharma", pw, "Priya Sharma", "priya.s@officemate.internal", 1, "employee", "https://api.dicebear.com/7.x/bottts/svg?seed=Priya", "available"),
            (6, "elena.rostova", pw, "Elena Rostova", "elena.r@officemate.internal", 3, "support_agent", "https://api.dicebear.com/7.x/bottts/svg?seed=Elena", "away")
        ]
    )

    # 3. Meeting Rooms
    cursor.executemany(
        """INSERT INTO meeting_rooms (id, name, floor, capacity, amenities, is_available)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (1, "Synergy Boardroom", "Floor 3", 16, "4K Dual Displays, Zoom Rooms Kit, Whiteboard, Polycom Mic", 1),
            (2, "Innovate Lab", "Floor 2", 8, "Smart TV, AirMedia, Glass Whiteboard, Conference Phone", 1),
            (3, "Focus Pod Alpha", "Floor 1", 4, "Acoustic Wall, 40-inch Monitor, Web Camera", 1),
            (4, "Creative Den", "Floor 2", 6, "Standing Desks, Mobile Whiteboard, Apple TV", 1)
        ]
    )

    # 4. Room Bookings (today and tomorrow)
    cursor.executemany(
        """INSERT INTO room_bookings (room_id, user_id, title, start_time, end_time, attendees_count, status)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            (1, 4, "Executive Quarterly Review", "2026-11-10 10:00", "2026-11-10 12:00", 12, "CONFIRMED"),
            (2, 2, "HR People Sync", "2026-11-10 14:00", "2026-11-10 15:00", 6, "CONFIRMED"),
            (3, 1, "Engineering 1-on-1", "2026-11-10 16:00", "2026-11-10 16:30", 2, "CONFIRMED"),
            (2, 3, "Sprint Planning & Demo", "2026-11-11 11:00", "2026-11-11 12:30", 8, "CONFIRMED")
        ]
    )

    # 5. Knowledge Base Documents
    cursor.executemany(
        """INSERT INTO knowledge_docs (id, title, category, department_id, content, tags, version)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            (
                1, "Annual & Sick Leave Policy 2026", "HR", 1,
                "OfficeMate employees are entitled to 20 paid vacation days, 10 casual leave days, and 12 sick leave days annually. "
                "Sick leaves extending beyond 3 consecutive calendar days require a certified medical practitioner note. "
                "Vacation requests exceeding 5 consecutive working days must be submitted at least 2 weeks in advance via the HR portal. "
                "Unused vacation days up to 8 days can be carried over to the following financial year before March 31st.",
                "leave, vacation, sick leave, pto, holidays, absence", "2.1"
            ),
            (
                2, "Health Insurance & Wellness Benefits", "HR", 1,
                "Comprehensive medical insurance covers employees and immediate dependents (spouse and up to two children) up to $500,000 per policy year. "
                "Dental checkups and vision optical tests are reimbursed up to $750 annually. "
                "Our wellness perk includes an annual $600 gym or fitness membership reimbursement. "
                "Maternity leave covers 26 fully paid weeks; paternity leave provides 4 fully paid weeks.",
                "insurance, health, medical, wellness, gym, maternity, paternity, benefits", "1.4"
            ),
            (
                3, "IT Security, VPN & Network Access Guide", "IT", 2,
                "All remote connections to internal production clusters require the GlobalProtect VPN with Multi-Factor Authentication (MFA). "
                "VPN Client configuration: Server address is vpn.officemate.internal using port 443. "
                "If VPN fails with 'Authentication Failure' or 'Timeout', first reset your MFA token via the Self-Service Security Portal. "
                "Never share your private SSH keys or corporate credentials. Laptops must run disk encryption (FileVault / BitLocker) at all times.",
                "vpn, network, mfa, security, password, wifi, globalprotect, credentials", "3.0"
            ),
            (
                4, "Software Installation & Development Tooling", "IT", 2,
                "Approved IDEs include VS Code, PyCharm Professional, and IntelliJ IDEA. "
                "Docker Desktop licenses are provided through IT enterprise portal. "
                "To request access to cloud accounts (AWS/GCP), submit an IT ticket with manager approval. "
                "For laptop hardware issues, visit the IT Command Center on Floor 2 between 9:00 AM and 5:00 PM on weekdays.",
                "software, ide, docker, pycharm, vscode, laptop, hardware, macbook, monitor", "1.2"
            ),
            (
                5, "Travel & Expense Reimbursement Policy", "ADMIN", 3,
                "Domestic business travel per diem allowance is $85 for meals and incidental expenses. "
                "Hotel accommodations must be booked through the corporate travel partner up to $180/night in Tier-1 cities. "
                "All expense receipts must be uploaded to the Admin reimbursement portal within 30 days of expense incurrence. "
                "Receipts over $25 require an itemized invoice showing business purpose and attendees.",
                "expense, travel, reimbursement, per diem, receipts, hotel, flight, finance", "2.0"
            ),
            (
                6, "Office Facilities, Passes & Ergonomics", "ADMIN", 3,
                "Employees are eligible for one ergonomic desk setup (lumbar chair, dual monitor arm, vertical mouse) upon joining. "
                "Replacement RFID badge passes incur a $15 fee if lost. Temporary visitor guest passes must be registered at least 24 hours prior at the Reception Desk. "
                "Electric vehicle charging stations on Basement Level B2 are free for all employees.",
                "ergonomics, chair, desk, visitor, badge, parking, facilities, cafeteria, access", "1.1"
            )
        ]
    )

    # 6. Policy Conflicts (for Policy Conflict Detector feature)
    cursor.executemany(
        """INSERT INTO policy_conflicts (doc1_id, doc2_id, conflict_type, description, status)
           VALUES (?, ?, ?, ?, ?)""",
        [
            (1, 6, "Remote Allowance Mismatch", "Leave Policy 2026 mentions 10 days work-from-home cap while Facilities Guide states flexible 3 days/week remote.", "DETECTED")
        ]
    )

    # 7. Announcements
    cursor.executemany(
        """INSERT INTO announcements (title, body, category, author_id, priority, is_active)
           VALUES (?, ?, ?, ?, ?, ?)""",
        [
            ("Annual Company Town Hall & Hackathon 2026", "Join CEO and leadership this Thursday at 3 PM in Synergy Boardroom and virtual live stream for our quarterly town hall followed by Hackathon kick-off!", "Company", 4, "URGENT", 1),
            ("New Organic Salad & Espresso Bar at Cafeteria", "Starting Monday, the 2nd Floor Cafeteria is launching an artisan espresso bar and organic salad station. Enjoy 50% discount during opening week!", "Cafeteria", 2, "NORMAL", 1),
            ("Scheduled Network Infrastructure Maintenance", "IT will perform core firewall upgrades this Saturday between 02:00 AM and 04:00 AM. Internal VPN services will experience intermittent disconnections.", "IT", 3, "NORMAL", 1)
        ]
    )

    # 8. Seed Tickets
    cursor.executemany(
        """INSERT INTO tickets (ticket_code, title, description, department_id, priority, status, created_by, assigned_to, sentiment, resolution_notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            ("TKT-HR-20261108-001", "Paternity Leave Allowance Clarification", "I would like to confirm if paternity leave can be split into two two-week blocks or taken continuously.", 1, "MEDIUM", "RESOLVED", 1, 2, "positive", "Confirmed via HR policy section 3.2 that leave can be split across baby's first 6 months."),
            ("TKT-IT-20261109-001", "GlobalProtect VPN timeout on macOS Sonoma", "Connection drops every 15 minutes when connecting from home fiber broadband.", 2, "HIGH", "IN_PROGRESS", 1, 3, "negative", "Investigating MTU size negotiation issue on router profile."),
            ("TKT-IT-20261109-002", "Docker Desktop License Renewal Needed", "License prompt says expired today, cannot spin up local development microservices.", 2, "CRITICAL", "OPEN", 5, 3, "negative", None),
            ("TKT-ADMIN-20261107-001", "Ergonomic Mesh Chair Armrest Replacement", "Right armrest height adjustment lever snapped off on desk 34-B.", 3, "LOW", "RESOLVED", 5, 4, "neutral", "Facilities swapped the chair with a brand new Herman Miller unit."),
            ("TKT-ADMIN-20261109-003", "Client Visit Visitor Parking Pass Request", "Need 2 reserved visitor parking spaces on level B1 for prospective clients this Friday.", 3, "MEDIUM", "OPEN", 1, 4, "positive", None),
            ("TKT-HR-20261110-002", "Health Insurance Dependent Card Download Error", "Insurance portal gives error 502 when trying to download spouse e-card.", 1, "HIGH", "OPEN", 5, 2, "negative", None)
        ]
    )

    conn.commit()
    conn.close()
    print("OfficeMate 2.0 database initialized and seeded successfully!")

if __name__ == "__main__":
    seed()
