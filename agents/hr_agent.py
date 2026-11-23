"""
HR Specialist Agent for OfficeMate 2.0
Handles queries concerning leave policies, benefits, insurance, payroll, and onboarding.
"""

from typing import Dict, Any, List

class HRAgent:
    def __init__(self):
        self.department_name = "Human Resources"
        self.department_code = "HR"

    def respond(self, query: str, intent: str, kb_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates an authoritative HR response citing official policies."""
        if not kb_matches:
            return {
                "handled": False,
                "message": "I could not find an official HR policy addressing your specific inquiry."
            }

        top_match = kb_matches[0]
        sources = [f"**{m['title']}** (Confidence: {m['score']:.1%})" for m in kb_matches]

        explanation = (
            f"Hello! According to our **{top_match['title']}**:\n\n"
            f"> *\"{top_match['text']}\"*\n\n"
            f"If you need to submit a formal leave request or claim benefit reimbursements, "
            f"you can also do so directly through the HR Department tab or submit an HR ticket for manager review."
        )

        return {
            "handled": True,
            "department": "HR",
            "agent_name": "Sarah (HR Specialist)",
            "message": explanation,
            "citations": sources,
            "top_match": top_match
        }
