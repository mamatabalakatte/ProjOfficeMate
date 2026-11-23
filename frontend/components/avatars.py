"""
Cartoon Character Avatars for OfficeMate 2.0
Pure SVG cartoon character generators with base64 Data-URI encoding.
"""

import base64

def get_avatar_svg(name: str, role: str = "Staff", color: str = "#4F46E5", accessory: str = "glasses", size: int = 64) -> str:
    """Generates an embedded cute cartoon avatar as an inline HTML <img> tag with base64 Data URI."""
    # Deterministic palette based on name
    palettes = {
        "Sarah Jenkins": {"skin": "#FCD34D", "hair": "#B45309", "shirt": "#EC4899", "bg": "#FCE7F3", "dept": "HR"},
        "David Kim": {"skin": "#FBBF24", "hair": "#1E293B", "shirt": "#3B82F6", "bg": "#DBEAFE", "dept": "IT"},
        "Marcus Vance": {"skin": "#F59E0B", "hair": "#4B5563", "shirt": "#F59E0B", "bg": "#FEF3C7", "dept": "ADMIN"},
        "Alex Chen": {"skin": "#FCD34D", "hair": "#1E1B4B", "shirt": "#6366F1", "bg": "#EEF2FF", "dept": "DEV"},
        "Elena Rostova": {"skin": "#FBBF24", "hair": "#D97706", "shirt": "#10B981", "bg": "#D1FAE5", "dept": "ADMIN"},
        "Priya Sharma": {"skin": "#F59E0B", "hair": "#312E81", "shirt": "#8B5CF6", "bg": "#EDE9FE", "dept": "ENG"}
    }
    p = palettes.get(name, {"skin": "#FCD34D", "hair": "#374151", "shirt": color, "bg": "#F3F4F6", "dept": role})

    raw_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{size}" height="{size}">'
        f'<circle cx="50" cy="50" r="50" fill="{p["bg"]}"/>'
        f'<path d="M22 92 C22 68, 78 68, 78 92 Z" fill="{p["shirt"]}"/>'
        f'<path d="M42 70 L50 82 L58 70 Z" fill="#FFFFFF"/>'
        f'<circle cx="50" cy="46" r="24" fill="{p["skin"]}"/>'
        f'<path d="M26 44 C26 24, 74 24, 74 44 C66 30, 34 30, 26 44 Z" fill="{p["hair"]}"/>'
        f'<circle cx="42" cy="45" r="3" fill="#1E293B"/>'
        f'<circle cx="58" cy="45" r="3" fill="#1E293B"/>'
        f'<circle cx="43" cy="44" r="1" fill="#FFFFFF"/>'
        f'<circle cx="59" cy="44" r="1" fill="#FFFFFF"/>'
        f'<circle cx="36" cy="51" r="3" fill="#FCA5A5" opacity="0.6"/>'
        f'<circle cx="64" cy="51" r="3" fill="#FCA5A5" opacity="0.6"/>'
        f'<path d="M44 54 Q50 60 56 54" stroke="#1E293B" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
        f'</svg>'
    )
    b64_data = base64.b64encode(raw_svg.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64_data}" width="{size}" height="{size}" alt="{name}" style="border-radius: 50%; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; vertical-align: middle;" />'

def render_employee_badge(name: str, role: str, status: str = "available") -> str:
    status_colors = {
        "available": ("#10B981", "Available"),
        "in_meeting": ("#F59E0B", "In Meeting"),
        "away": ("#6B7280", "On Break"),
        "offline": ("#EF4444", "Offline")
    }
    color, text = status_colors.get(status, ("#10B981", "Active"))
    avatar = get_avatar_svg(name, role, size=46)

    return (
        f'<div style="display: flex; align-items: center; gap: 12px; padding: 10px 14px; '
        f'background: white; border: 1px solid #E2E8F0; border-radius: 12px; '
        f'box-shadow: 0 2px 6px rgba(0,0,0,0.04); margin-bottom: 8px;">'
        f'<div>{avatar}</div>'
        f'<div style="flex: 1;">'
        f'<div style="font-weight: 700; color: #1E293B; font-size: 0.95rem;">{name}</div>'
        f'<div style="color: #64748B; font-size: 0.78rem;">{role}</div>'
        f'<div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">'
        f'<span style="width: 8px; height: 8px; border-radius: 50%; background: {color}; display: inline-block;"></span>'
        f'<span style="font-size: 0.72rem; color: #475569; font-weight: 600;">{text}</span>'
        f'</div></div></div>'
    )
