"""
Administration Specialist Agent for OfficeMate 2.0
Handles travel reimbursements, office facilities, passes, ergonomic supplies, and office services.
"""

from typing import Dict, Any, List

class AdminAgent:
    def __init__(self):
        self.department_name = "Administration & Facilities"
        self.department_code = "ADMIN"

    def respond(self, query: str, intent: str, kb_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not kb_matches:
            return {
                "handled": False,
                "message": "No administrative facility policy matches this request."
            }

        top_match = kb_matches[0]
        sources = [f"**{m['title']}** (Relevance: {m['score']:.1%})" for m in kb_matches]

        extra_info = ""
        if intent == "travel_expense":
            extra_info = (
                "\n\n**Expense Claim Reminder:**\n"
                "• Upload original itemized GST/tax receipts within 30 days.\n"
                "• Per diem covers up to $85/day without receipts for incidentals."
            )
        elif intent == "facilities_supplies":
            extra_info = (
                "\n\n**Facilities Note:**\n"
                "Ergonomic chair and dual-monitor desk mounts are delivered within 48 hours of ticket submission."
            )

        explanation = (
            f"Hello! Regarding your facilities/finance inquiry from **{top_match['title']}**:\n\n"
            f"> *\"{top_match['text']}\"*{extra_info}\n\n"
            f"For physical replacements or urgent facility issues, you can visit the Administration desk or track via tickets."
        )

        return {
            "handled": True,
            "department": "ADMIN",
            "agent_name": "Marcus (Admin & Facilities Lead)",
            "message": explanation,
            "citations": sources,
            "top_match": top_match
        }
