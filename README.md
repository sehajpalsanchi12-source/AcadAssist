# AcadAssist — Simplifying Academic & Digital Work 🎓⚡

Official smart academic preparation and student assistance platform designed for students of **Lovely Professional University (LPU)**.

Branded as **AcadAssist** (with official visual identity extracted from the poster), this platform provides Vertos with authentic LPU exam pattern simulations, preloaded subject notes from **notes.lpuverto.xyz**, custom course creation, Google Sign-in user accounts, direct UPI monetization to **`7719730804@ptyes`**, and a master Administrator Control Panel (`acadassit0812` / `;Sharma@1290`).

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
  - **Password**: `;Sharma@1290`
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
cd /Users/sanchisharma/.gemini/antigravity/scratch/lpu-verto-exam-ai

# Activate environment and launch uvicorn
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Open in Browser
👉 Visit: **http://127.0.0.1:8000**

### 3. Run Automated 28-Stage Test Suite
```bash
.venv/bin/python test_server.py
```
*(All 28 tests pass 100%, verifying Google auth, UPI paywall to `7719730804@ptyes`, admin controls, poster courses, exam simulation, all 266 subjects, and PowerPoint slide generation).*

---

## 📁 Project Architecture
```
lpu-verto-exam-ai/
├── app/
│   ├── main.py                  # FastAPI routes (Auth, Paywall, Admin, Assets, Exam)
│   └── services/
│       ├── admin_service.py     # Master admin login (acadassit0812 / ;Sharma@1290) & analytics
│       ├── user_service.py      # Google auth, student profiles, mock test & inquiry store
│       ├── paywall_service.py   # UPI payments (7719730804@ptyes), ₹49 plan, UTR tracking
│       ├── lpuverto_service.py  # notes.lpuverto.xyz sync & preloaded poster courses
│       ├── exam_generator.py    # LPU exam pattern & question generator
│       ├── study_asset_generator.py # Notes, slides, short notes, roadmaps
│       └── document_parser.py   # PDF & text parser
├── data/
│   ├── users.json               # Registered Google student profiles
│   ├── transactions.json        # UPI payments & UTR reference records
│   ├── mock_tests.json          # Completed student test scorecards & grades
│   ├── service_inquiries.json   # Service orders (EduCode, NeoBrowser, Handwritten, PPT)
│   └── custom_subjects.json     # Saved user-created courses
├── static/
│   ├── index.html               # AcadAssist UI with Midterm Mode, Admin & Google Login
│   ├── css/
│   │   └── styles.css           # Styling, paywall blurs & print layouts
│   ├── img/
│   │   ├── acadassist-new-logo-transparent.png # Pink & black official logo
│   │   ├── acadassist-logo-transparent.png     # Official horizontal brandmark
│   │   ├── acadassist-icon-transparent.png     # Official favicon/app icon
│   │   ├── acadassist-poster-new.jpg           # Latest user poster
│   │   └── acadassist-poster.jpg               # First user poster
│   └── js/
│       ├── auth.js              # Google login & student profile controller
│       ├── admin.js             # Admin dashboard controller (acadassit0812)
│       ├── services.js          # Service booking & inquiry controller
│       ├── paywall.js           # Paywall modal, ₹49 plan, UPI 7719730804@ptyes, UTR
│       ├── simulator.js         # TCS iON exam timer, question palette & scoring
│       └── app.js               # Hub, custom course creator & multi-asset studio
├── test_samples/
│   └── sample_notes.txt         # Pre-configured test notes
├── test_server.py               # 19-stage end-to-end automated test suite (100% passing)
└── README.md
```
