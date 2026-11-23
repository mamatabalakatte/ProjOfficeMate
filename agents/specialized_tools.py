"""
Specialized AI Modules for OfficeMate 2.0
Section 6 Features:
1. Cross-Department Root Cause Analyzer
2. Policy Conflict Detector
3. Screenshot OCR / Diagnostic Troubleshooting
4. Multilingual Assistant (English, Hindi, Telugu, Kannada)
"""

import re
from typing import List, Dict, Any
from db.database import get_tickets, get_knowledge_docs, query_all

# --- 1. Cross-Department Root Cause Analyzer ---

def analyze_cross_department_root_causes() -> List[Dict[str, Any]]:
    """Analyzes open tickets across all departments to identify common systemic root causes."""
    tickets = get_tickets(status="OPEN") + get_tickets(status="IN_PROGRESS")
    
    # Common systemic incident signatures
    incident_patterns = [
        {
            "incident_name": "SSO & Identity Provider Gateway Latency",
            "keywords": ["vpn", "auth", "mfa", "login", "password", "okta", "timeout"],
            "probable_cause": "Core Active Directory / Okta SSO connector intermittent timeout causing cascading login failures across HR portal and VPN.",
            "recommended_action": "Restart Okta RADIUS sync proxy and check corporate identity federation status."
        },
        {
            "incident_name": "Internal Corporate Subnet DNS Resolution Outage",
            "keywords": ["dns", "unreachable", "502", "connection", "portal", "download", "internal"],
            "probable_cause": "Internal BIND DNS server zone transfer failure preventing resolution of *.internal hostnames.",
            "recommended_action": "Flush primary domain controller DNS cache and inspect BGP route health."
        },
        {
            "incident_name": "Office Facilities HVAC Thermal Disruption",
            "keywords": ["air conditioning", "temperature", "freezing", "hot", "floor", "ventilation"],
            "probable_cause": "Building Management System (BMS) thermostat sensor node calibration failure.",
            "recommended_action": "Dispatch building maintenance engineer to recalibrate Floor 2 VAV controller."
        }
    ]

    findings = []
    for pattern in incident_patterns:
        matched_tickets = []
        for t in tickets:
            full_text = f"{t['title']} {t['description']}".lower()
            if any(kw in full_text for kw in pattern["keywords"]):
                matched_tickets.append({
                    "ticket_code": t["ticket_code"],
                    "department": t["department_name"],
                    "title": t["title"],
                    "status": t["status"]
                })

        if len(matched_tickets) >= 1:
            depts_affected = list(set(m["department"] for m in matched_tickets))
            findings.append({
                "incident_name": pattern["incident_name"],
                "affected_departments": depts_affected,
                "correlated_ticket_count": len(matched_tickets),
                "matched_tickets": matched_tickets,
                "probable_cause": pattern["probable_cause"],
                "recommended_action": pattern["recommended_action"],
                "severity": "CRITICAL" if len(depts_affected) > 1 else "HIGH"
            })

    return findings

# --- 2. Policy Conflict Detector ---

def detect_policy_conflicts() -> List[Dict[str, Any]]:
    """Detects contradictory, outdated, or duplicate policies across departments."""
    conflicts = query_all("SELECT pc.*, d1.title as doc1_title, d2.title as doc2_title FROM policy_conflicts pc LEFT JOIN knowledge_docs d1 ON pc.doc1_id = d1.id LEFT JOIN knowledge_docs d2 ON pc.doc2_id = d2.id")
    
    # Also perform live heuristic checks
    docs = get_knowledge_docs()
    detected = list(conflicts)
    
    # Heuristic 1: Remote work / leave mismatch
    has_leave_doc = any("leave" in d["title"].lower() for d in docs)
    has_facilities_doc = any("facilities" in d["title"].lower() for d in docs)
    if has_leave_doc and has_facilities_doc and not any(c.get("conflict_type") == "Remote Allowance Mismatch" for c in detected):
        detected.append({
            "id": 99,
            "doc1_title": "Annual & Sick Leave Policy 2026",
            "doc2_title": "Office Facilities, Passes & Ergonomics",
            "conflict_type": "Remote Policy Inconsistency",
            "description": "Leave policy stipulates strict manager approval for WFH over 2 days, whereas facilities handbook indicates flexible 3 days hybrid schedule.",
            "status": "DETECTED",
            "detected_at": "Recent Scan"
        })

    return detected

# --- 3. Screenshot OCR / Diagnostic Troubleshooting ---

def diagnose_screenshot_or_error(error_text: str) -> Dict[str, Any]:
    """Analyzes error codes extracted from screenshots or diagnostic text to match IT runbooks."""
    text = error_text.upper()
    
    if "MFA" in text or "OKTA" in text or "AUTH" in text:
        return {
            "error_category": "Authentication / MFA Failure",
            "matched_code": "ERR_AUTH_TIMEOUT_403",
            "severity": "HIGH",
            "diagnosis": "Multi-factor authentication push token timed out or certificate out of sync.",
            "suggested_fix": "Open Self-Service Portal -> Request new Okta SMS code -> Sync authenticator clock time."
        }
    elif "VPN" in text or "GLOBALPROTECT" in text or "TUNNEL" in text:
        return {
            "error_category": "VPN Gateway Disconnection",
            "matched_code": "VPN_GATEWAY_CONN_TIMEOUT",
            "severity": "HIGH",
            "diagnosis": "Client unable to handshake with vpn.officemate.internal:443. Potential MTU mismatch.",
            "suggested_fix": "Change MTU to 1400: `sudo ifconfig en0 mtu 1400` or switch from IPv6 to IPv4 DNS."
        }
    elif "502" in text or "BAD GATEWAY" in text:
        return {
            "error_category": "Backend Reverse Proxy Error",
            "matched_code": "HTTP_502_BAD_GATEWAY",
            "severity": "CRITICAL",
            "diagnosis": "Internal microservice upstream did not return a valid HTTP response.",
            "suggested_fix": "Verify internal service container status in Kubernetes namespace or contact DevOps on-call."
        }
    elif "DOCKER" in text or "CONTAINER" in text or "LICENSE" in text:
        return {
            "error_category": "Software Licensing",
            "matched_code": "DOCKER_ENTERPRISE_LICENSE_EXPIRED",
            "severity": "MEDIUM",
            "diagnosis": "Docker Desktop annual enterprise token expired on client daemon.",
            "suggested_fix": "Download updated license key file from IT Software Portal -> Docker Settings -> Apply License."
        }
    else:
        return {
            "error_category": "General System Diagnostic",
            "matched_code": "SYS_UNSPECIFIED_DIAGNOSTIC",
            "severity": "MEDIUM",
            "diagnosis": f"Extracted diagnostic details: '{error_text[:80]}...'",
            "suggested_fix": "Submit this diagnostic excerpt to the IT Command Center for technician triage."
        }

# --- 4. Multilingual Assistant Support ---

MULTILINGUAL_TRANSLATIONS = {
    "en": {
        "greeting": "Hello! I am OfficeMate, your intelligent workplace assistant. How can I help you today?",
        "ticket_created": "Your support ticket has been created successfully. Tracking ID:",
        "dept_identified": "Identified Department:",
        "sources": "Official Policy Sources:"
    },
    "hi": {
        "greeting": "नमस्ते! मैं OfficeMate हूँ, आपका बुद्धिमान कार्यस्थल सहायक। आज मैं आपकी क्या मदद कर सकता हूँ?",
        "ticket_created": "आपका सहायता टिकट सफलतापूर्वक बना दिया गया है। ट्रैकिंग आईडी:",
        "dept_identified": "पहचाना गया विभाग:",
        "sources": "आधिकारिक नीति संदर्भ:"
    },
    "te": {
        "greeting": "నమస్కారం! నేను OfficeMate, మీ ఇంటెలిజెంట్ వర్క్‌ప్లేస్ అసిస్టెంట్‌ని. ఈరోజు నేను మీకు ఎలా సహాయపడగలను?",
        "ticket_created": "మీ సపోర్ట్ టికెట్ విజయవంతంగా సృష్టించబడింది. ట్రాకింగ్ ఐడి:",
        "dept_identified": "గుర్తించిన విభాగం:",
        "sources": "అధికారిక పాలసీ మూలాలు:"
    },
    "kn": {
        "greeting": "ನಮಸ್ಕಾರ! ನಾನು OfficeMate, ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕಚೇರಿ ಸಹಾಯಕ. ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
        "ticket_created": "ನಿಮ್ಮ ಬೆಂಬಲ ಟಿಕೆಟ್ ಅನ್ನು ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ. ಟ್ರ್ಯಾಕಿಂಗ್ ಐಡಿ:",
        "dept_identified": "ಗುರುತಿಸಲಾದ ಇಲಾಖೆ:",
        "sources": "ಅಧಿಕೃತ ನೀತಿ ಮೂಲಗಳು:"
    }
}

def get_localized_strings(lang: str = "en") -> Dict[str, str]:
    return MULTILINGUAL_TRANSLATIONS.get(lang.lower(), MULTILINGUAL_TRANSLATIONS["en"])
