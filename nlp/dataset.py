"""
Dataset Generator & Loader for OfficeMate 2.0 NLP Module
CSE472 Deep Learning for NLP - Project 20
Department Classification: HR, IT, ADMIN
Granular Intent Classification
"""

import json
import os
import random
from typing import List, Dict, Any, Tuple
from sklearn.model_selection import train_test_split

DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "nlp_dataset.json")

# Curated benchmark dataset of enterprise employee queries
RAW_SAMPLES = [
    # --- HR Department Queries ---
    {"text": "How many days of paid vacation do I have left this year?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "What is the procedure to apply for 3 weeks of maternity leave?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "Can I take casual leave on Monday after taking sick leave on Friday?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "Do I need a doctor certificate for two days of sick leave?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "How do I check my remaining PTO balance in the HR portal?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "Can unused vacation days be carried over to the next financial year?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "What is the policy for bereavement and compassionate leave?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "How do I submit an emergency leave application without prior notice?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "Are public holidays counted as part of annual leave when taking a full week off?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "What are the rules regarding paternity leave duration and splitting?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "How does unpaid sabbatical leave affect my healthcare benefits?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "Can I encash my unused privilege leaves at the end of the year?", "dept": "HR", "intent": "leave_inquiry"},
    {"text": "What healthcare coverage does the corporate health insurance policy provide?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "How do I add my newborn child or spouse to my group health insurance plan?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "Does company insurance cover dental procedures, cleanings, and braces?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "Where can I download the health insurance cashless claim e-card?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "What is the annual gym and wellness allowance reimbursement limit?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "Are optical checkups, eyeglasses, and lenses covered under employee benefits?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "How do I claim reimbursement for prescription medicines purchased outside?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "Does our insurance policy cover outpatient consultations and diagnostics?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "What are the mental health counseling and therapy support programs available?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "When is the annual employee benefit enrollment window open?", "dept": "HR", "intent": "benefits_insurance"},
    {"text": "Why was my salary deducted for loss of pay this month?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "Where can I download my monthly salary payslips and tax withholding form?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "How do I update my bank account details for payroll direct deposit?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "When will the annual performance bonus be credited to our accounts?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "How is provident fund (PF) contribution calculated on basic salary?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "Who should I contact about an error in my tax deduction at source (TDS)?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "Can I increase my voluntary provident fund (VPF) monthly deduction?", "dept": "HR", "intent": "payroll_salary"},
    {"text": "What is the payroll cutoff date for overtime and shift allowances?", "dept": "HR", "intent": "payroll_salary"},

    # --- IT Department Queries ---
    {"text": "GlobalProtect VPN connection failed with authentication error", "dept": "IT", "intent": "vpn_network"},
    {"text": "My office WiFi is repeatedly disconnecting on the 3rd floor", "dept": "IT", "intent": "vpn_network"},
    {"text": "How do I connect to the corporate VPN from a Linux or Mac machine?", "dept": "IT", "intent": "vpn_network"},
    {"text": "My Okta multi-factor authentication (MFA) push notification is not coming", "dept": "IT", "intent": "vpn_network"},
    {"text": "I got locked out of my corporate Active Directory and email account", "dept": "IT", "intent": "vpn_network"},
    {"text": "How do I reset my domain password after it expired today?", "dept": "IT", "intent": "vpn_network"},
    {"text": "Can IT whitelist our remote team IP address for staging database access?", "dept": "IT", "intent": "vpn_network"},
    {"text": "The VPN client shows timeout while establishing secure tunnel connection", "dept": "IT", "intent": "vpn_network"},
    {"text": "Cannot access internal GitLab server from home without VPN connection", "dept": "IT", "intent": "vpn_network"},
    {"text": "How to register a new phone device for Microsoft Authenticator?", "dept": "IT", "intent": "vpn_network"},
    {"text": "Slow internet download speeds over corporate guest wireless network", "dept": "IT", "intent": "vpn_network"},
    {"text": "Firewall is blocking port 8080 required for local Docker development", "dept": "IT", "intent": "vpn_network"},
    {"text": "How can I request a Docker Desktop and PyCharm Professional license?", "dept": "IT", "intent": "software_access"},
    {"text": "Need access permissions to the AWS production RDS database instance", "dept": "IT", "intent": "software_access"},
    {"text": "Please grant me write access to the main GitHub repository backend repository", "dept": "IT", "intent": "software_access"},
    {"text": "My Slack desktop app keeps crashing on launch with fatal error", "dept": "IT", "intent": "software_access"},
    {"text": "How do I install approved software packages without admin privileges?", "dept": "IT", "intent": "software_access"},
    {"text": "Cannot pull private Docker image from company container registry", "dept": "IT", "intent": "software_access"},
    {"text": "Need Adobe Creative Cloud license for marketing collateral design", "dept": "IT", "intent": "software_access"},
    {"text": "Zoom meetings screen sharing crashes my graphics driver on macOS", "dept": "IT", "intent": "software_access"},
    {"text": "Where can I request access to Jira project boards and Confluence spaces?", "dept": "IT", "intent": "software_access"},
    {"text": "Outlook email client is not syncing incoming emails since yesterday", "dept": "IT", "intent": "software_access"},
    {"text": "My laptop screen is flickering and showing horizontal colored lines", "dept": "IT", "intent": "hardware_issue"},
    {"text": "MacBook Pro battery draining in less than an hour and overheating", "dept": "IT", "intent": "hardware_issue"},
    {"text": "The USB-C docking station is not recognizing external 4K monitors", "dept": "IT", "intent": "hardware_issue"},
    {"text": "My mechanical keyboard spacebar key is stuck and not registering input", "dept": "IT", "intent": "hardware_issue"},
    {"text": "Need a replacement charger adapter for Lenovo ThinkPad work laptop", "dept": "IT", "intent": "hardware_issue"},
    {"text": "Laptop trackpad is unresponsive and mouse pointer is jumping around", "dept": "IT", "intent": "hardware_issue"},
    {"text": "Can I get an external webcam and noise cancelling headset for remote calls?", "dept": "IT", "intent": "hardware_issue"},
    {"text": "Hard drive disk space is 99% full due to system cache and swap files", "dept": "IT", "intent": "hardware_issue"},

    # --- ADMIN Department Queries ---
    {"text": "How do I submit travel expense receipts for flight and hotel reimbursement?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "What is the per diem meal allowance limit for domestic business travel?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "Can I claim taxi cab fare from the airport to hotel during client visit?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "My expense report was rejected because of missing itemized tax receipts", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "How long does it take for finance to approve and disburse approved travel claims?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "What is the mileage reimbursement rate if I use my personal car for client meetings?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "How to book international business flights through company corporate travel agent?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "Can I get an advance cash float for team client dinner and entertainment?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "Where do I submit credit card bills for corporate corporate card expenses?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "What is the maximum hotel room rate allowed per night in Tier 1 cities?", "dept": "ADMIN", "intent": "travel_expense"},
    {"text": "How do I request an ergonomic office chair and adjustable standing desk?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "I lost my office RFID entry access card and need a new security badge", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "The air conditioning on the 2nd floor east wing is freezing cold", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "How do I register two external client visitors for meeting room access tomorrow?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Printer on the 3rd floor hallway is out of cyan toner and jammed with paper", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Can I reserve a dedicated parking space in the basement parking garage?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Where can I collect office stationery, notebooks, sticky notes, and pens?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "The coffee espresso vending machine in the 2nd floor cafeteria is leaking water", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Need courier shipping service to send legal contracts to overseas office", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Can facilities provide an extra dual-monitor desk mount clamp for desk 42?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "How do I request an office locker key for storing personal belongings?", "dept": "ADMIN", "intent": "facilities_supplies"},
    {"text": "Light bulb above my desk is flickering constantly and causing eye strain", "dept": "ADMIN", "intent": "facilities_supplies"}
]

# Generate synthetic variations to provide a solid training corpus (~200+ samples)
TEMPLATES = {
    "leave_inquiry": [
        "I want to check policy regarding {topic} leave balance.",
        "Could you explain the process for applying {topic} off days?",
        "Is {topic} leave allowed for new employees during probation?",
        "What documents are needed when taking {topic} leave?",
        "Can I combine {topic} leave with weekend public holidays?"
    ],
    "benefits_insurance": [
        "Are {topic} healthcare medical expenses covered under company plan?",
        "How do I submit hospital bills for {topic} claim approval?",
        "Does company policy provide reimbursement for {topic} fitness expenses?",
        "Where can I find policy details regarding {topic} coverage?",
        "Can family dependents get coverage for {topic} checkups?"
    ],
    "payroll_salary": [
        "Inquiry regarding {topic} tax deduction on my monthly paycheck.",
        "When is the cutoff for submitting {topic} payroll declarations?",
        "There is a discrepancy in my {topic} component on my payslip.",
        "How do I update my bank account for {topic} deposits?",
        "Who can help me understand my {topic} year-end deductions?"
    ],
    "vpn_network": [
        "Experiencing issues connecting to {topic} network tunnel.",
        "Why does {topic} fail whenever I switch wireless networks?",
        "Need help configuring {topic} on my company-issued machine.",
        "Getting timeout error when authenticating via {topic}.",
        "Can network team check why {topic} is unreachable today?"
    ],
    "software_access": [
        "Requesting software license and activation key for {topic}.",
        "Need access permissions for {topic} developer environment.",
        "My {topic} desktop application crashes during video calls.",
        "How do I submit an approval request to use {topic} tool?",
        "Getting permission denied error when accessing {topic} directory."
    ],
    "hardware_issue": [
        "My work laptop has a faulty {topic} requiring replacement.",
        "Need urgent IT hardware support for broken {topic}.",
        "The {topic} connected to my workstation stopped functioning.",
        "Can I exchange my damaged {topic} at the IT support desk?",
        "Experiencing intermittent failure with my laptop {topic}."
    ],
    "travel_expense": [
        "How do I file an expense claim for business {topic} expenses?",
        "What is the maximum allowed budget for business trip {topic}?",
        "My claim for {topic} was returned asking for receipt clarification.",
        "Can I get reimbursement for {topic} incurred during client workshop?",
        "Where in the finance portal do I upload {topic} receipts?"
    ],
    "facilities_supplies": [
        "Requesting office assistance regarding {topic} on our floor.",
        "Can facilities team check the {topic} near the conference room?",
        "How do I order new {topic} for our team workstation area?",
        "The {topic} in the reception lobby is out of order.",
        "Need a replacement {topic} for my assigned office desk."
    ]
}

TOPIC_MAP = {
    "leave_inquiry": ("HR", ["vacation", "sick", "casual", "maternity", "paternity", "emergency", "bereavement", "unpaid"]),
    "benefits_insurance": ("HR", ["dental", "vision", "gym wellness", "prescription drug", "outpatient", "dependent health", "annual health checkup"]),
    "payroll_salary": ("HR", ["bonus", "tax withholding", "provident fund", "salary payslip", "direct deposit", "overtime pay"]),
    "vpn_network": ("IT", ["GlobalProtect VPN", "corporate WiFi", "Okta MFA token", "firewall port", "SSH bastion", "Active Directory domain"]),
    "software_access": ("IT", ["Docker Desktop", "PyCharm IDE", "AWS console", "GitHub repo", "Slack workspace", "Jira board", "Figma design"]),
    "hardware_issue": ("IT", ["laptop battery", "external 4K monitor", "docking station", "mechanical keyboard", "USB-C charger", "webcam microphone"]),
    "travel_expense": ("IT_or_ADMIN", ["flight tickets", "hotel per diem", "airport taxi fare", "client dinner meal", "car mileage allowance"]),
    "facilities_supplies": ("ADMIN", ["ergonomic chair", "RFID access card", "air conditioning temperature", "printer toner", "stationery supplies", "parking slot"])
}

def generate_augmented_dataset() -> List[Dict[str, Any]]:
    random.seed(42)
    dataset = list(RAW_SAMPLES)
    
    for intent, templates in TEMPLATES.items():
        dept, topics = TOPIC_MAP[intent]
        if intent == "travel_expense":
            dept = "ADMIN"
        for topic in topics:
            for tmpl in templates:
                text = tmpl.format(topic=topic)
                dataset.append({
                    "text": text,
                    "dept": dept,
                    "intent": intent
                })
                
    random.shuffle(dataset)
    return dataset

def get_train_val_test_splits(test_size: float = 0.15, val_size: float = 0.15) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    os.makedirs(os.path.dirname(DATASET_FILE), exist_ok=True)
    if not os.path.exists(DATASET_FILE):
        dataset = generate_augmented_dataset()
        with open(DATASET_FILE, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2)
    else:
        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            dataset = json.load(f)

    # Stratified split by department
    depts = [d["dept"] for d in dataset]
    train_val, test = train_test_split(dataset, test_size=test_size, random_state=42, stratify=depts)
    
    val_rel_size = val_size / (1.0 - test_size)
    depts_train_val = [d["dept"] for d in train_val]
    train, val = train_test_split(train_val, test_size=val_rel_size, random_state=42, stratify=depts_train_val)
    
    return train, val, test

if __name__ == "__main__":
    tr, v, te = get_train_val_test_splits()
    print(f"Dataset generated: Train={len(tr)}, Val={len(v)}, Test={len(te)}, Total={len(tr)+len(v)+len(te)}")
