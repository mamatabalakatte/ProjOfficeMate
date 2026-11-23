# 🏢 OfficeMate 2.0 – The Intelligent Virtual Workplace
### Dual-Engine Deep Learning NLP • Interactive Virtual Office • Enterprise Digital Twin
*Built for CSE472 Deep Learning for Natural Language Processing — Project 20: Intelligent Enterprise Assistant for Organizational Efficiency*

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit%20%7C%20Flask%20%7C%20PyTorch-orange)](https://streamlit.io/)
[![NLP Engine](https://img.shields.io/badge/NLP-Bi--LSTM%20%2B%20TF--IDF-success)](https://pytorch.org/)
[![Test Suite](https://img.shields.io/badge/pytest-20%2F20%20passed%20(100%25)-brightgreen)](tests/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌐 Live Deployed Application Links

| Portal / Service | Port | Access Link | Status | Description |
| :--- | :---: | :---: | :---: | :--- |
| **Streamlit Virtual Workplace** | **8501** | **[http://localhost:8501](http://localhost:8501)** | 🟢 **ACTIVE** | Full 17-page interactive virtual headquarters & AI Assistant |
| **OfficeMate REST API (Flask)** | **5000 / 5001** | **[http://127.0.0.1:5000](http://127.0.0.1:5000)** | 🟢 **ACTIVE** | Headless classification, RAG retrieval & digital twin endpoints |
| **GitHub Repository** | — | **[https://github.com/mamatabalakatte/ProjOfficeMate](https://github.com/mamatabalakatte/ProjOfficeMate)** | 🚀 **ONLINE** | Complete source code, models, tests, and documentation |

---

## 🌟 1. Project Overview & Vision

**OfficeMate 2.0** transforms conventional corporate intranets and ticketing portals into an immersive, intelligent virtual office. Employees step into an interactive workplace where they can visit specialized departments (**HR, IT, Administration**), converse with a multi-agent AI assistant, retrieve company policies with verified source citations, diagnose IT incidents with automatic ticket routing, reserve conference rooms with collision prevention, and stress-test organizational operations through a discrete-event **Enterprise Digital Twin**.

---

## 🏗️ 2. High-Level Architecture & Query Workflow

```
                                      +----------------------------------------------------+
                                      |     Streamlit Interactive Front-End (Port 8501)    |
                                      |     17 Dashboard Hubs • Visual HQ • User Cockpit   |
                                      +-------------------------+--------------------------+
                                                                |
                                             Query Input & Persona Context
                                                                |
                                      +-------------------------v--------------------------+
                                      |          Multi-Agent Supervisor Agent              |
                                      |             (agents/supervisor.py)                 |
                                      +----+--------------------+---------------------+----+
                                           |                    |                     |
                  +------------------------+                    |                     +------------------------+
                  |                                             |                                              |
+-----------------v------------------+        +-----------------v------------------+         +-----------------v------------------+
|      NLP Classification Engine     |        |   Semantic Search Engine (RAG)     |         |     Universal Workplace Brain      |
|        (nlp/bilstm_model.py)       |        |     (nlp/semantic_search.py)       |         |    (agents/universal_brain.py)     |
+------------------------------------+        +------------------------------------+         +------------------------------------+
| • Preprocessing & Tokenization     |        | • Sentence Chunking Indexer        |         | • Policy Formatting & Citations    |
| • Bidirectional LSTM (PyTorch)     |        | • TF-IDF + Cosine Similarity       |         | • First-Aid Diagnostics            |
| • TF-IDF Baseline (Scikit-Learn)   |        | • Broad Cross-Dept Fallback        |         | • Professional Email Drafting      |
| • Department & Intent Prediction   |        | • Confidence Thresholding (>= 0.15)|         | • Tech, Coding & Math Knowledge    |
+-----------------+------------------+        +-----------------+------------------+         +-----------------+------------------+
                  |                                             |                                              |
                  +------------------------+                    |                     +------------------------+
                                           |                    |                     |
                                      +----v--------------------v---------------------v----+
                                      |             Automatic Ticket Triage Engine         |
                                      |               (agents/ticket_agent.py)             |
                                      +-------------------------+--------------------------+
                                                                |
                                             Saves & Updates via WAL Transactions
                                                                |
                                      +-------------------------v--------------------------+
                                      |         SQLite Enterprise DB (officemate.db)       |
                                      |  Tickets • Policies • Rooms • Bookings • Telemetry |
                                      +----------------------------------------------------+
```

---

## 📋 3. Project 20 Core Components: Working Process

### 🤖 Component 1: Employee Chatbot Interface
- **Page:** `Page 2: AI Workplace Assistant` ([http://localhost:8501](http://localhost:8501))
- **Working Process:**
  1. An employee submits any inquiry (natural language question, troubleshooting request, email draft request, or policy inquiry).
  2. The interface uses native Streamlit `st.chat_message` components, instantly displaying the user prompt with active persona context.
  3. The inquiry is routed through the **Supervisor Agent**, which dynamically assigns department badges (`🌸 HR Agent`, `💻 IT Agent`, `🏢 Admin Agent`).
  4. Returns rich markdown answers, bullet points, syntax-highlighted code blocks, warning banners for auto-generated tickets, and verified source citations.
  5. Includes user feedback buttons (👍 / 👎) logged directly into the database for continuous evaluation.

### 📚 Component 2: Dataset Creation & Annotation
- **Dataset File:** `data/nlp_dataset.json`
- **Working Process:**
  - Labeled dataset spanning 3 primary departments: `HR`, `IT`, and `ADMIN`.
  - Comprehensive intent taxonomy:
    - **HR Intents:** `leave_inquiry`, `benefits_insurance`, `parental_leave`, `remote_work_policy`, `salary_payroll`
    - **IT Intents:** `vpn_network`, `hardware_issue`, `software_access`, `account_security`, `system_outage`
    - **Admin Intents:** `travel_reimbursement`, `facilities_supplies`, `room_booking`, `visitor_pass`, `office_policy`
  - Split into **Train (80%)** and held-out **Test (20%)** partitions with stratified sampling.

### 🧠 Component 3: Intent & Department Classification
- **Modules:** `nlp/bilstm_model.py`, `nlp/tfidf_baseline.py`, `nlp/preprocessor.py`
- **Working Process:**
  1. **Preprocessing:** Contraction expansion (`don't` $\to$ `do not`), lowercase normalization, punctuation removal, and whitespace normalization.
  2. **Baseline Model:** TF-IDF n-gram vectorizer (1-2 ngrams, sublinear term frequency) coupled with Multinomial / Logistic Regression.
  3. **Deep Learning Model (Bi-LSTM):**
     - Embedding Layer (vocab size ~500, embedding dimension = 64).
     - Bidirectional LSTM layer (hidden dimension = 64 per direction, total output = 128 dimensions).
     - Dropout regularization ($p=0.3$) to prevent overfitting.
     - Fully connected linear classification head with Softmax output.
  4. Predicts both the target **Department** and **User Intent** along with confidence probabilities.

### 🔍 Component 4: Knowledge Base & Answer Retrieval (RAG)
- **Module:** `nlp/semantic_search.py`
- **Database Table:** `knowledge_docs` in `data/officemate.db`
- **Working Process:**
  1. Corporate policy documents (HR handbook, IT security guidelines, travel per diems, remote protocols) are chunked into semantic sentence passages.
  2. Passages are indexed into an n-gram TF-IDF vector space with exact-phrase boosting.
  3. Queries are transformed into vector representations and evaluated using **Cosine Similarity**:
     $$\text{Cosine Similarity}(q, d) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|}$$
  4. Confidence thresholding ($\tau = 0.15$) ensures that only relevant excerpts are cited.
  5. **Cross-Department Fallback:** If department-filtered search does not meet the confidence threshold, the engine automatically broadens the search across all organizational documents.

### 🎫 Component 5: Automatic Ticket Generation & Priority Triage
- **Module:** `agents/ticket_agent.py`
- **Working Process:**
  1. **Trigger Conditions:** Triggered when (a) an actionable hardware/network incident is detected, (b) an exceptional policy approval is requested, or (c) knowledge retrieval confidence is below threshold.
  2. **Priority Determination:** Keyword heuristics and severity rules categorize requests into:
     - `CRITICAL`: Outage, fire, data breach, payroll failure
     - `HIGH`: Broken laptop, locked out, GlobalProtect VPN failure, blocked deadlines
     - `MEDIUM`: Standard inquiries, software installations, access permissions
     - `LOW`: Stationery, desk ergonomics, minor supplies
  3. **Unique Tracking Codes:** Generates formatted codes like `TKT-<DEPT>-YYYYMMDD-###` (e.g. `TKT-IT-20261123-013`).
  4. Automatically records the ticket in the SQLite database with active user requester ID, department routing, and timestamps.

### 📊 Component 6: Admin Dashboard & Kanban Ticket Lifecycle
- **Pages:** `Page 8: Ticket Management`, `Page 16: Admin Control Centre`
- **Working Process:**
  1. **Dual Views:** Interactive Card Grid view and drag-free Agile Kanban Board (`OPEN` $\to$ `IN_PROGRESS` $\to$ `RESOLVED`).
  2. **Role-Based Transparency:** Explicitly labels the **Requester** (👤 Raised by) and the **Performer** (🛠️ Assigned Specialist).
  3. **1-Click Ticket Claiming:** Support specialists can claim tickets directly from the queue with a single click.
  4. **Multi-Perspective Filters:** View all enterprise tickets, only tickets raised by the active user, or tickets assigned to the active user.

### ⚙️ Component 7: Enterprise Digital Twin & SimPy Simulator
- **Pages:** `Page 10: Enterprise Digital Twin`, `Page 11: What-If Simulator`, `Page 13: Predictive Analytics`
- **Modules:** `simulation/digital_twin.py`, `simulation/what_if_simulator.py`, `simulation/predictive_engine.py`
- **Working Process:**
  1. **Telemetry Engine:** Computes real-time operational health scores (0–100%) based on queue depth, SLA violations, and staffing.
  2. **SimPy Queuing Model:** Simulates an $M/M/c$ queuing system over an 8-hour shift:
     - Arrival rate $\lambda$ (Poisson process)
     - Staff capacity $c$ (Support specialists)
     - Service rate $\mu$ (Exponential distribution)
  3. **What-If Shock Scenarios:**
     - 40% IT ticket surge (e.g. major OS migration)
     - 50% HR staffing shortage (holiday peak)
     - Critical network outage (cascading cross-department backlog)
  4. **Predictive Analytics:** 14-day forward forecast using additive seasonal decomposition with automated staffing alerts.

---

## 📈 4. Real Benchmark Evaluation Metrics

Evaluated on held-out test partitions ($N=51$ test samples, 3 classes: `HR`, `IT`, `ADMIN`):

| Evaluation Metric | TF-IDF + Logistic Regression | Bidirectional LSTM (Deep Learning) | Relative Gain |
| :--- | :---: | :---: | :---: |
| **Overall Test Accuracy** | **90.20%** | **92.16%** | **+1.96%** |
| **Macro F1-Score** | **89.47%** | **91.97%** | **+2.50%** |
| **Macro Precision** | **92.06%** | **92.09%** | **+0.03%** |
| **Macro Recall** | **88.25%** | **90.94%** | **+2.69%** |
| **Ticket Routing Accuracy** | **90.20%** | **92.16%** | **+1.96%** |

*Confusion matrices, class breakdown charts, and saliency maps can be explored live in `Page 15: Model Evaluation`.*

---

## 🏢 5. The 17 Interactive Virtual Office Pages

1. **Virtual Office Home:** Interactive cartoon isometric office canvas with clickable departments, employee avatars, and noticeboard.
2. **AI Workplace Assistant:** Dual-engine multi-agent conversational assistant with verified citations and ticket escalation.
3. **HR Department:** Leave balance meters, formal leave request submission, and employee benefit cards.
4. **IT Department:** Infrastructure status indicators, screenshot OCR diagnostic tool, and hardware requests.
5. **Administration Department:** Business travel per diem calculator and office supply requisition.
6. **Employee Workspace:** Personalized cockpit showing submitted tickets, booked rooms, and daily checklist.
7. **Knowledge Base:** Natural language search across all corporate policies with relevance scoring.
8. **Ticket Management:** Kanban board with status transitions, ticket claiming, and role-based filtering.
9. **Meeting Room Booking:** Conference room grid with collision detection and amenity inspection.
10. **Enterprise Digital Twin:** Real-time departmental health telemetry and discrete-event queue monitoring.
11. **What-If Simulator:** Interactive SimPy simulation testing operational shocks and stress limits.
12. **Employee Impact Intelligence:** Privacy-preserving workplace friction driver heatmaps and root cause analysis.
13. **Predictive Analytics:** 14-day ticket volume forecasting and staffing recommendations.
14. **Knowledge Graph:** Interactive visual network graph connecting policies, departments, and resources.
15. **Model Evaluation:** Detailed CSE472 NLP benchmarks, loss curves, confusion matrices, and XAI explainability.
16. **Admin Control Centre:** Human-in-the-loop review queue and corporate policy contradiction detector.
17. **Cafeteria & Lounge:** Subsidized artisan menu, office celebration calendar, peer kudos, and coffee roulette.

---

## 🚀 6. Installation & Quickstart

### Prerequisites
- Python 3.10, 3.11, or 3.12
- macOS, Linux, or Windows

### Step 1: Clone Repository
```bash
git clone https://github.com/mamatabalakatte/ProjOfficeMate.git
cd ProjOfficeMate
```

### Step 2: One-Click Environment Setup
```bash
chmod +x setup.sh
./setup.sh
```
*This automatically creates the virtual environment, installs dependencies, seeds the database, and trains the NLP models.*

### Step 3: Run the Streamlit Virtual Workplace
```bash
./run_frontend.sh
```
*Open **[http://localhost:8501](http://localhost:8501)** in your browser.*

### Step 4 (Optional): Run the Flask REST API
```bash
./run_backend.sh
```
*API available at **[http://localhost:5000](http://localhost:5000)**.*

---

## 🧪 7. Automated Test Suite

Run the full pytest suite across all modules:
```bash
./.venv/bin/pytest tests/ -v
```

**Results (20/20 Passing - 100%):**
- `tests/test_nlp.py` — Text preprocessing, Bi-LSTM & TF-IDF inference, model evaluation
- `tests/test_search.py` — Semantic RAG search, confidence thresholds, cross-department search
- `tests/test_tickets.py` — Priority determination, auto-ticket generation, status transitions
- `tests/test_meeting_rooms.py` — Room existence, booking collision prevention
- `tests/test_digital_twin.py` — Telemetry calculations, SimPy simulation, ticket forecasting
- `tests/test_api.py` — Flask REST API endpoints, classification, and chat routing

---

## 👥 Persona Switching System

OfficeMate 2.0 includes 6 active personas selectable from the sidebar:
- **Alex Chen** — Software Engineer • IT (`alex.chen@company.com`)
- **Sarah Jenkins** — Support Specialist • HR Lead (`sarah.j@company.com`)
- **David Kim** — Support Specialist • IT Lead (`david.kim@company.com`)
- **Marcus Vance** — Facilities Administrator (`marcus.v@company.com`)
- **Priya Sharma** — Data Analyst • HR/Eng (`priya.s@company.com`)
- **Elena Rostova** — Support Specialist • Admin (`elena.r@company.com`)

Switching personas dynamically re-calibrates the Employee Workspace, ticket assignments, permissions, and greeting contexts.
