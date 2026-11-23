"""
IT Specialist Agent for OfficeMate 2.0
Handles network, software licenses, hardware issues, credentials, and troubleshooting.
"""

from typing import Dict, Any, List

class ITAgent:
    def __init__(self):
        self.department_name = "Information Technology"
        self.department_code = "IT"

    def respond(self, query: str, intent: str, kb_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not kb_matches:
            return {
                "handled": False,
                "message": "No matching IT runbook or knowledge documentation found."
            }

        top_match = kb_matches[0]
        sources = [f"**{m['title']}** (Relevance: {m['score']:.1%})" for m in kb_matches]

        troubleshoot_steps = ""
        if intent == "vpn_network":
            troubleshoot_steps = (
                "\n\n**Quick Troubleshooting Checklist:**\n"
                "1. Verify internet connectivity on your base machine.\n"
                "2. Check gateway `vpn.officemate.internal:443`.\n"
                "3. Re-verify Okta MFA push notification on your registered mobile device.\n"
                "4. If still unresolved, restart GlobalProtect service."
            )
        elif intent == "software_access":
            troubleshoot_steps = (
                "\n\n**Software Request Notice:**\n"
                "Enterprise software licenses (Docker, PyCharm, AWS) are auto-provisioned upon manager sign-off via IT self-service."
            )

        explanation = (
            f"Hi there! IT Command Center reference from **{top_match['title']}**:\n\n"
            f"> *\"{top_match['text']}\"*{troubleshoot_steps}\n\n"
            f"If your workstation hardware or access requires technician intervention, an IT support ticket can be opened immediately."
        )

        return {
            "handled": True,
            "department": "IT",
            "agent_name": "David (IT Support Lead)",
            "message": explanation,
            "citations": sources,
            "top_match": top_match
        }
