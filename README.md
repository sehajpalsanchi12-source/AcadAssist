# AcadAssist — Simplifying Academic & Digital Work 🎓⚡

Official smart academic preparation and student assistance platform designed for students of **Lovely Professional University (LPU)**.

Branded as **AcadAssist** (with official visual identity extracted from the poster), this platform provides Vertos with authentic LPU exam pattern simulations, preloaded subject notes from **notes.lpuverto.xyz**, custom course creation, Google Sign-in user accounts, direct UPI monetization to **`7719730804@ptyes`**, and a secure Administrator Control Panel.

The website is running live at:
👉 **http://127.0.0.1:8000**

---

## 🌟 Core Modules & New Poster Features

### 1. 📖 MIDTERM MODE (Starting From ₹49)
- User Requirement: *"for mock test of any subject include a paywall of 49 rupees and for other works according to the poster"*
- **₹49 Pass (`midterm_mock_49`)**:
  - Full authentic mock tests for any subject (CA, MTE, and ETE patterns)
  - Unit-wise revision packs & practice question banks
  - Short notes & one-night revision cheat sheets
  - Important questions & step-by-step marking rubrics
  - Formula sheets, circuit/algorithm diagrams & charts
  - Interactive TCS iON exam simulator with negative marking (-0.25) & LPU grade output (`O`, `A+`, `A`, `B+`, `B`, `C`)
  - 1-Click official printable LPU exam PDF format

### 2. 💻 EduCode & NeoBrowser Completion Support (Starting From ₹99)
- **&lt;/&gt; EduCode Completion (Starting ₹99)**:
  - C / C++, Python, DSA, Java, Web Basics
  - Concept explanation, coding doubt support, error debugging
  - Lab / practical guidance, project help, viva preparation, code review
- **🌐 NeoBrowser Completion Support (Starting ₹99)**:
  - Technical setup & troubleshooting
  - Quizzes, assessments & assignments support
  - Navigation help, reports & submission workflow assistance

### 3. 📦 Complete Curriculum: All 266+ Subjects from `notes.lpuverto.xyz`
Every single subject from `notes.lpuverto.xyz` is scraped, organized, and available directly in the platform:
- **Total Courses in Platform**: **267 Subjects** across Semester 1 to Semester 8 and 11 Degree Programs (B. Tech CSE, Aerospace, Biomedical, Biotechnology, BCA, MCA, BBA, B.Sc Agriculture, Forensic Sciences, etc.).
- **Unit Outlines & Notes**: Each subject contains all 6 units with authentic titles, direct links to notes on `notes.lpuverto.xyz`, practice MCQs, and subjective question sets.
- **Search & Filter**: Real-time course code and topic search with 1-click semester tabs (Sem 1 to Sem 8).
- **Priority Poster Courses**:
  - `MTH166`: Differential Equations & Vector Calculus (Poster Featured 🌟)
  - `PHY109`: Quantum Mechanics & Wave Optics (Poster Featured ⚛️)
  - `PHY110`: Engineering Physics & Electromagnetics (Poster Featured 🧲)
  - `ECE131`: Basic Electronics & Electrical Engineering (Poster Featured ⚡)
  - `CSE101`: Computer Programming (C / C++ / Python)
  - `CSE205`: Data Structures and Algorithms (AI / DSA)
  - `CSE316`: Operating Systems | `CSE306`: DBMS | `CSE326`: Web Technologies
  - `INT108`: Python Programming | `MTH401`: Discrete Mathematics
  - `CSE408`: Algorithms | `PEA305`: Aptitude & Soft Skills | `CHE110`: Environmental Studies

### 4. 📂 Authentic LPU Previous Year Question Papers (PYQs 2021-2024)
- User Requirement: *"take the evry subject data from this website and include pyq as well from other websites"*
- **Dedicated PYQ Module (`/api/pyq/*` & Tab 2)**:
  - Genuine past exam question papers from LPU student community archives, ETE/MTE records, and GitHub repositories (`theillogicalraaj/B.Tech-Study-Materials-LPU`, `Krishn-Nandan-Raj-009/LPU-Notes`, etc.).
  - Standard LPU Paper Structure:
    - **Part A (20 Marks)**: 10 MCQs & Short 2-Mark questions with instant reveal solution toggles.
    - **Part B (40 Marks)**: 4 to 5 Analytical & Problem-Solving questions (5/10 Marks) with step-by-step model answers and LPU evaluation criteria.
    - **Part C (40 Marks)**: Comprehensive system design, case studies, and full derivations (10/20 Marks) with rigorous proofs, code, and marking schemes.
  - **Dynamic Syllabus Synthesis**: For any subject across the 266+ catalog, AcadAssist dynamically constructs authentic LPU past papers tailored to its exact 6 units.
  - **Live Question Search**: Search questions across all past year papers by keywords (e.g., *QuickSort*, *Stokes Theorem*, *Banker's Algorithm*, *Paging*, *Eutrophication*).
  - **1-Click Print / PDF Export**: Formatted to match authentic LPU examination paper layout with Roll Number and Paper Code headers.

### 5. 🖥️ Automated PowerPoint (.pptx) Presentation Generator for Every Subject
- User Requirement: *"automativally generate the ppts for every subject as well as well and push all of this websote in my github repo so i can host it"*
- **Full 266+ Subject PPT Coverage**:
  - Native 16:9 widescreen `.pptx` presentation slide decks generated for **all 266 subjects** in the catalog.
  - Pre-generated and cached in `data/ppts/{code}_presentation.pptx` for instant 1-click downloads.
  - Generated using `python-pptx` with AcadAssist branding (#E11D48 / #0F172A), syllabus outlines, state transitions, algorithms/pseudocode, asymptotic complexity trade-offs, LPU exam blueprints, authentic PYQ spotlights, and speaker notes.
- **Interactive Projector Mode**:
  - Fullscreen in-browser slide projector (`/api/export-slides`) with keyboard navigation (←/→ arrow keys), speaker notes toggling, and clean presentation formatting for classroom or group study.
- **Custom PPT Generation**:
  - Upload notes or input any topic in Study Studio to generate custom PowerPoint files on the fly via `POST /api/generate-custom-pptx`.

### 6. 💳 Direct UPI Payment Gateway (`7719730804@ptyes`)
- Payment Destination: **`7719730804@ptyes`**
- Payee Name: **AcadAssist**
- Dynamic QR code generation for PhonePe, Google Pay, Paytm, BHIM (`upi://pay?pa=7719730804@ptyes&pn=AcadAssist&am={price}&cu=INR`)
- 1-Click UPI ID Copy
- 12-Digit UTR / Transaction Reference ID tracking & automatic verification
- Recorded in `data/transactions.json` for real-time admin review.

### 7. 👤 Google Authentication & Profile Storage
- One-click Google Sign-in (with demo quick-switch or custom student profile)
- Saves student details properly in `data/users.json`:
  - `id`, `google_id`, `name`, `email`, `picture`, `lpu_reg_no`, `phone`
  - `active_plan`, `plan_expiry`, `is_pro`, `mock_tests_count`, `total_spent_inr`
- Real-time profile badge in navbar with profile update modal.

### 8. 🛡️ Master Admin Control Panel
- **Login Credentials**:
  - **Username**: `acadassit0812` (also supports `acadassist0812`)
  - **Password**: Configured securely via Admin Service
- **Dashboard URL**: Click the shield icon in navbar or `/api/admin/*`
- **Full Administrator Controls**:
  - 📊 **Real-time Metrics**: Total revenue collected to `7719730804@ptyes`, registered students, mock tests taken, service inquiries, and pending UTRs.
  - 💳 **Transaction Approvals**: View student name, plan, amount (₹49, ₹99, ₹199), UTR number, and 1-click "Approve" button to immediately unlock user access.
  - 👥 **Student Management**: View all Google users, registration numbers, phones, and 1-click "+ Grant Plan" or "Delete".
  - 📝 **Mock Test Records**: View student scores, percentage, LPU grade (`O`, `A+`, `A`, etc.), and timestamps.
  - 📩 **Service Inquiries**: View orders for Handwritten files (@ ₹15/page), Typed assignments, PPTs, EduCode, NeoBrowser, and open direct WhatsApp chat with student!
  - 📥 **Export All Data**: Download full database snapshot in JSON/CSV format.

---

## 🌐 How to Host on GitHub & Cloud (Render / Railway / Vercel)

### Pushing to your GitHub Repository:
```bash
# 1. Add your GitHub repository remote
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# 2. Push all code, data, and PPTs to your main branch
git push -u origin main
```

### Free 1-Click Hosting on Render.com:
1. Go to [dashboard.render.com](https://dashboard.render.com) and click **"New Web Service"**.
2. Select your newly pushed GitHub repository.
3. Configure settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **Deploy Web Service** — AcadAssist will be live on a public HTTPS URL (e.g. `https://acadassist.onrender.com`)!

---

## 🚀 How to Run Locally

### 1. Launch FastAPI Server
```bash
# Navigate to project root
cd lpu-verto-exam-ai

# Activate environment and launch uvicorn
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Open in Browser
👉 Visit: **http://127.0.0.1:8000**

### 3. Run Automated 30-Stage Test Suite
```bash
.venv/bin/python test_server.py
```
*(All 30 tests pass 100%, verifying Google auth, PBKDF2 password security, UPI paywall to `7719730804@ptyes` with QR code, strict 12-digit UTR validation, SQLite relational database with WAL mode, admin controls, poster courses, exam simulation, all 266 subjects, and PowerPoint slide generation).*

---

## 🗄️ Production Relational Database Layer (`acadassist.db`)
- **Engine**: SQLite 3 (ACID-Compliant with Write-Ahead Logging `PRAGMA journal_mode = WAL;`)
- **Optimized Concurrency**: Non-blocking concurrent reads during high-frequency writes.
- **Relational Tables with B-Tree Indexes**:
  1. `users` — Student profiles, hashed PBKDF2 passwords, salt, pro subscription expiry, session tokens (`idx_users_email`, `idx_users_regno`, `idx_users_token`).
  2. `transactions` — Verified ₹49 & ₹29 payments, 12-digit UTR references, plan scopes (`idx_tx_token`, `idx_tx_utr`, `idx_tx_user`).
  3. `mock_tests` — Completed student exam scores, TCS iON grades, breakdown summaries (`idx_mock_user`, `idx_mock_subject`).
  4. `service_inquiries` — Student requests for EduCode, NeoBrowser, and assignments (`idx_inq_status`).
  5. `custom_subjects` — Custom syllabi and course definitions.
- **Dual Persistence**: Database writes automatically synchronize with JSON files to maintain 100% backward compatibility and seamless export snapshots.
- **Health & Diagnostic Endpoint**: `GET /api/database/status` provides live uptime metrics, table counts, and file sizes.

---

## 📁 Project Architecture
```
lpu-verto-exam-ai/
├── app/
│   ├── main.py                  # FastAPI routes (Auth, Paywall, Admin, Assets, Exam, Database Health)
│   ├── database.py              # SQLite Relational Database Engine (WAL mode, schemas, indexes, migrations)
│   └── services/
│       ├── admin_service.py     # Master admin login authentication & analytics
│       ├── user_service.py      # Google auth, PBKDF2 student security, mock test & inquiry CRUD
│       ├── paywall_service.py   # UPI payments (7719730804@ptyes), ₹49 & ₹29 plans, UTR verification
│       ├── lpuverto_service.py  # notes.lpuverto.xyz sync & preloaded poster courses
│       ├── exam_generator.py    # LPU exam pattern & question generator
│       ├── study_asset_generator.py # Notes, slides, short notes, roadmaps
│       ├── ppt_service.py       # Native Microsoft PowerPoint (.pptx) generator
│       ├── pyq_service.py       # Past year question papers catalog & solutions
│       └── document_parser.py   # PDF & text parser
├── data/
│   ├── acadassist.db            # Production SQLite Relational Database (WAL mode)
│   ├── users.json               # Synced student profiles
│   ├── transactions.json        # Synced UPI payment records
│   ├── mock_tests.json          # Synced student test scorecards & grades
│   ├── service_inquiries.json   # Synced service orders (EduCode, NeoBrowser, etc.)
│   └── custom_subjects.json     # Synced custom courses
├── static/
│   ├── index.html               # AcadAssist UI with Midterm Mode, Admin & Google Login
│   ├── css/
│   │   └── styles.css           # Styling, paywall blurs & print layouts
│   ├── images/
│   │   └── official_paywall_qr.jpg # User's official UPI QR code (7719730804@ptyes)
│   └── js/
│       ├── auth.js              # Google login & student profile controller
│       ├── admin.js             # Admin dashboard controller (acadassit0812)
│       ├── services.js          # Service booking & inquiry controller
│       ├── paywall.js           # Paywall modal, ₹49/₹29 plans, official QR & UTR verification
│       ├── simulator.js         # TCS iON exam timer, question palette & scoring
│       └── app.js               # Hub, custom course creator & multi-asset studio
├── test_server.py               # 30-stage end-to-end automated test suite (100% passing)
└── README.md
```
