import os
import json
import httpx
from dotenv import load_dotenv
load_dotenv()  # Load .env file (GEMINI_API_KEY etc.) at startup
from typing import Optional, Any, Dict, List
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.document_parser import DocumentParser
from app.services.lpuverto_service import LPUVertoService
from app.services.exam_generator import ExamGenerator
from app.services.paywall_service import PaywallService
from app.services.study_asset_generator import StudyAssetGenerator
from app.services.user_service import UserService
from app.services.admin_service import AdminService
from app.services.pyq_service import PYQService
from app.services.ppt_service import PPTService
from app.services.ai_chat_service import AIChatService
from app.database import Database

app = FastAPI(
    title="AcadAssist LPU AI Exam Prep",
    description="AI-powered MCQ, Notes, Slides, Short Notes, and Roadmap Generator aligned with LPU Examination Pattern",
    version="1.2.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers & Hardening Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

# Initialize Real Relational Database
@app.on_event("startup")
async def startup_event():
    """Initialize SQLite Relational Database, migrate existing JSON data, and configure WAL mode."""
    Database.init_db()
    print("[Database] SQLite Relational Database connected & initialized with WAL mode.")

# Static directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

# ── Database Health & Diagnostics Endpoint ────────────────────────────────

@app.get("/api/database/status")
async def get_database_status():
    """Return real-time diagnostic health metrics for SQLite database."""
    try:
        stats = Database.get_stats()
        return JSONResponse(status_code=200, content={"success": True, "database": stats})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

# ── Catalog & LPU Verto API Endpoints ─────────────────────────────────────

@app.get("/api/preloaded-subjects")
async def get_preloaded_subjects():
    """Return preloaded high-priority subjects already bundled from notes.lpuverto.xyz."""
    return LPUVertoService.get_preloaded_subjects()

@app.get("/api/all-subjects")
async def get_all_subjects(
    search: Optional[str] = Query(None),
    semester: Optional[str] = Query(None),
    program: Optional[str] = Query(None),
    limit: Optional[int] = Query(None)
):
    """Return all 266+ subjects from notes.lpuverto.xyz with optional filtering."""
    return LPUVertoService.get_all_subjects_list(search=search, semester=semester, program=program, limit=limit)

@app.get("/api/subject/{code}")
async def get_subject_detail(code: str):
    """Return detailed syllabus, units, and notes metadata for a specific subject code."""
    subject = LPUVertoService.get_subject_by_code(code)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {code} not found in catalog")
    return subject

# ── PowerPoint (.pptx) & Slide Deck Endpoints ─────────────────────────────

@app.get("/api/subject/{code}/presentation")
async def get_subject_presentation(code: str, unit: Optional[int] = Query(None)):
    """Return structured slide deck JSON for in-browser presentation projector."""
    try:
        deck_data = PPTService.generate_presentation_data(code, unit=unit)
        return deck_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presentation: {str(e)}")

@app.get("/api/subject/{code}/download-pptx")
async def download_subject_pptx(code: str):
    """Download compiled native Microsoft PowerPoint (.pptx) file for the subject."""
    try:
        file_path = PPTService.get_or_create_subject_pptx(code)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Failed to locate generated PowerPoint file.")
        
        filename = f"{code.upper()}_presentation.pptx"
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error preparing PowerPoint file: {str(e)}")

@app.get("/api/all-ppts")
async def get_all_ppts():
    """List status and download links for all subject PowerPoint presentations."""
    subjects = PPTService._load_subjects()
    ppts_dir = PPTService.PPTS_DIR
    items = []
    for code, s in subjects.items():
        pptx_path = os.path.join(ppts_dir, f"{code}_presentation.pptx")
        exists = os.path.exists(pptx_path)
        items.append({
            "code": code,
            "name": s.get("name", ""),
            "semester": s.get("semester", ""),
            "program": s.get("program", ""),
            "download_url": f"/api/subject/{code}/download-pptx",
            "presentation_url": f"/api/subject/{code}/presentation",
            "ready": exists,
            "size_bytes": os.path.getsize(pptx_path) if exists else 0
        })
    return {
        "total_subjects": len(subjects),
        "total_ppts_ready": sum(1 for it in items if it["ready"]),
        "items": items
    }

@app.post("/api/generate-custom-pptx")
async def generate_custom_pptx_endpoint(
    title: str = Form("Academic Presentation"),
    code: str = Form("CUSTOM"),
    unit: str = Form("Unit 1"),
    text: str = Form(...)
):
    """Generate and download custom .pptx PowerPoint file from user notes or text."""
    try:
        pptx_bytes = PPTService.generate_custom_pptx(title=title, text=text, code=code, unit=unit)
        filename = f"{code.upper()}_presentation.pptx"
        return Response(
            content=pptx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom PPT generation error: {str(e)}")

# ── PYQ (Previous Year Questions) API Endpoints ───────────────────────────

@app.get("/api/pyq/subjects")
async def get_pyq_subjects():
    """List all subjects that have PYQ examination papers available."""
    return PYQService.get_pyq_subjects()

@app.get("/api/pyq/papers")
async def get_pyq_papers(
    subject: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    term: Optional[str] = Query(None)
):
    """Retrieve list of past examination papers filtered by subject code, year, or exam term."""
    return PYQService.get_papers(subject_code=subject, year=year, term=term)

@app.get("/api/pyq/paper/{paper_id}")
async def get_pyq_paper(paper_id: str):
    """Retrieve full PYQ paper with questions, options, step-by-step model solutions and rubrics."""
    paper = PYQService.get_paper_by_id(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail=f"Paper '{paper_id}' not found")
    return paper

@app.get("/api/pyq/search")
async def search_pyq_questions(q: str = Query(...)):
    """Search for questions across all past year papers by keyword or topic."""
    return PYQService.search_questions(q)

@app.get("/api/custom-subjects")
async def get_custom_subjects():
    """Return user-created custom courses."""
    return LPUVertoService.get_custom_subjects()

class CustomSubjectModel(BaseModel):
    code: str
    name: str
    semester: str = "Sem1"
    program: str = "B. Tech. CSE"
    credits: int = 4
    category: str = "Custom Course"
    description: str = ""
    units: list = []

@app.post("/api/custom-subject")
async def create_custom_subject(data: CustomSubjectModel):
    """Save a user-created custom subject."""
    return LPUVertoService.save_custom_subject(data.dict())

@app.delete("/api/custom-subject/{code}")
async def delete_custom_subject(code: str):
    """Delete a user-created custom subject."""
    success = LPUVertoService.delete_custom_subject(code)
    return {"success": success}

@app.get("/api/programs")
async def get_programs():
    """List available LPU degree programs."""
    return await LPUVertoService.get_programs()

@app.get("/api/structure")
async def get_structure(program: str = Query("B. Tech. CSE")):
    """Get semester, subject, and unit structure for an LPU program."""
    return await LPUVertoService.get_structure(program)

@app.get("/api/search")
async def search_catalog(q: str = Query(...), program: str = Query("B. Tech. CSE")):
    """Search subjects or topics in notes.lpuverto.xyz catalog."""
    return await LPUVertoService.search_catalog(q, program)

@app.get("/api/unit-mcqs")
async def get_unit_mcqs(sem: str = Query(...), subject: str = Query(...), unit: str = Query(...)):
    """Fetch live MCQs from notes.lpuverto.xyz."""
    return await LPUVertoService.get_unit_mcqs(sem, subject, unit)

@app.get("/api/unit-notes")
async def get_unit_notes(sem: str = Query(...), subject: str = Query(...), unit: str = Query(...)):
    """Fetch live unit notes from notes.lpuverto.xyz."""
    text = await LPUVertoService.get_unit_notes(sem, subject, unit)
    return {"notes": text}

# ── Multi-Asset Study Material Generator (Notes, Slides, Short Notes, Roadmap) ──

@app.post("/api/generate-asset")
async def generate_study_asset(
    asset_type: str = Form("notes"),  # 'notes', 'short_notes', 'slides', 'roadmap'
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None),
    subject_code: str = Form("CSE101"),
    subject_name: str = Form("Computer Programming"),
    semester: str = Form("Sem2"),
    unit: str = Form("Unit1"),
    token: Optional[str] = Form(None)
):
    """
    Generate diverse learning materials:
    - notes: In-depth unit study notes
    - short_notes: Revision cheat sheet & memory flashcards
    - slides: Presentation slide deck outline
    - roadmap: Week-by-week 9+ CGPA study plan
    """
    # Verify User Token (Free users can generate assets, pro unlocks all deep assets)
    user_status = PaywallService.verify_token(token)
    is_pro = user_status.get("is_pro", False)

    extracted_text = ""
    if file and file.filename:
        try:
            file_bytes = await file.read()
            extracted_text = DocumentParser.parse_uploaded_file(file.filename, file_bytes)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File extraction error: {str(e)}")

    if text_content and text_content.strip():
        extracted_text = (extracted_text + "\n\n" + text_content.strip()).strip()

    # If no text provided, fetch study notes directly from notes.lpuverto.xyz!
    if not extracted_text:
        try:
            extracted_text = await LPUVertoService.get_unit_notes(semester, subject_code, unit)
        except Exception:
            extracted_text = f"Curriculum and syllabus study notes for {subject_name} ({subject_code}) {unit} based on LPU standards."

    if not extracted_text.strip():
        extracted_text = f"Curriculum and syllabus study notes for {subject_name} ({subject_code}) {unit} based on LPU standards."

    clean_unit = unit.replace("Unit", "Unit ")

    if asset_type == "notes":
        result = StudyAssetGenerator.generate_full_notes(extracted_text, subject_code, subject_name, clean_unit)
    elif asset_type == "short_notes":
        result = StudyAssetGenerator.generate_short_notes(extracted_text, subject_code, subject_name, clean_unit)
    elif asset_type == "slides":
        result = StudyAssetGenerator.generate_slides(extracted_text, subject_code, subject_name, clean_unit)
    elif asset_type == "roadmap":
        result = await StudyAssetGenerator.generate_roadmap(extracted_text, subject_code, subject_name)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported asset type: {asset_type}")

    result["asset_type"] = asset_type
    result["is_pro_user"] = is_pro
    return result

@app.post("/api/export-slides", response_class=HTMLResponse)
async def export_slides_html(deck: dict):
    """Render interactive fullscreen HTML slide presentation."""
    slides = deck.get("slides", [])
    subject_code = deck.get("subject_code", "CSE101")
    subject_name = deck.get("subject_name", "Course Material")
    unit = deck.get("unit", "Unit 1")

    slides_html = ""
    for idx, s in enumerate(slides):
        bullets_html = "".join([f"<li style='margin-bottom: 12px; font-size: 1.15rem; line-height: 1.6;'>{b}</li>" for b in s.get("bullets", [])])
        code_html = ""
        if s.get("code_or_diagram"):
            code_html = f"<pre style='background: #0f172a; color: #38bdf8; padding: 16px; border-radius: 12px; font-size: 0.9rem; overflow-x: auto; margin-top: 16px; border: 1px solid #1e293b; font-family: monospace;'>{s.get('code_or_diagram')}</pre>"

        speaker_html = ""
        if s.get("speaker_notes"):
            speaker_html = f"<div style='margin-top: 24px; padding: 12px 16px; background: rgba(249, 115, 22, 0.1); border-left: 4px solid #f97316; border-radius: 6px; font-size: 0.85rem; color: #cbd5e1;'><strong>🎙️ Speaker Notes:</strong> {s.get('speaker_notes')}</div>"

        display_style = "block" if idx == 0 else "none"
        slides_html += f"""
        <div class="slide" id="slide-{idx}" style="display: {display_style}; width: 100%; max-width: 900px; min-height: 520px; background: #1e293b; border: 1px solid #334155; border-radius: 24px; padding: 48px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 16px; margin-bottom: 24px;">
                <span style="font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; color: #f97316;">{subject_code} • {unit}</span>
                <span style="font-size: 0.85rem; font-weight: bold; color: #94a3b8;">Slide {idx + 1} of {len(slides)}</span>
            </div>
            <h1 style="font-size: 1.85rem; font-weight: 800; color: #f8fafc; margin-bottom: 8px;">{s.get('title')}</h1>
            {f"<h3 style='font-size: 1rem; color: #94a3b8; font-weight: 500; margin-bottom: 24px;'>{s.get('subtitle')}</h3>" if s.get('subtitle') else ""}
            <ul style="color: #e2e8f0; padding-left: 24px;">
                {bullets_html}
            </ul>
            {code_html}
            {speaker_html}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{subject_code} - Presentation Slides</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: #0b1120;
                color: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            .controls {{
                margin-top: 24px;
                display: flex;
                gap: 12px;
                align-items: center;
            }}
            .btn {{
                padding: 10px 20px;
                background: #f97316;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 0.9rem;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .btn:hover {{ background: #ea580c; }}
            .btn-secondary {{
                background: #334155;
            }}
            .btn-secondary:hover {{ background: #475569; }}
        </style>
    </head>
    <body>
        {slides_html}

        <div class="controls">
            <button class="btn btn-secondary" onclick="prevSlide()">← Previous (Left Arrow)</button>
            <button class="btn" onclick="nextSlide()">Next (Right Arrow) →</button>
            <button class="btn btn-secondary" onclick="toggleFullScreen()">⛶ Fullscreen</button>
        </div>

        <script>
            let current = 0;
            const total = {len(slides)};

            function showSlide(idx) {{
                if (idx < 0 || idx >= total) return;
                document.querySelectorAll('.slide').forEach((el, i) => {{
                    el.style.display = i === idx ? 'block' : 'none';
                }});
                current = idx;
            }}

            function nextSlide() {{
                if (current < total - 1) showSlide(current + 1);
            }}

            function prevSlide() {{
                if (current > 0) showSlide(current - 1);
            }}

            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') nextSlide();
                else if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
            }});

            function toggleFullScreen() {{
                if (!document.fullscreenElement) {{
                    document.documentElement.requestFullscreen();
                }} else if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ── Exam Generation Endpoint ──────────────────────────────────────────────

@app.post("/api/generate-exam")
async def generate_exam(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None),
    subject_code: str = Form("CSE101"),
    subject_name: str = Form("Computer Programming"),
    program: str = Form("B. Tech. CSE"),
    semester: str = Form("Sem2"),
    unit: str = Form("Unit1"),
    exam_type: str = Form("ete"),
    mcq_count: int = Form(15),
    short_count: int = Form(4),
    long_count: int = Form(2),
    difficulty: str = Form("Mixed"),
    negative_marking: bool = Form(True),
    fetch_lpuverto_data: bool = Form(True),
    token: Optional[str] = Form(None)
):
    """
    Generate an authentic LPU Exam Paper from:
    1. Uploaded notes/PDF/document
    2. Direct text paste
    3. Direct LPU Verto subject code and unit notes from notes.lpuverto.xyz
    """
    # 1. Verify User Pro Status (per-subject access isolation)
    is_pro = PaywallService.has_mock_access(token, subject_code)

    extracted_text = ""
    # Check if a file was uploaded
    if file and file.filename:
        try:
            file_bytes = await file.read()
            extracted_text = DocumentParser.parse_uploaded_file(file.filename, file_bytes)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File extraction error: {str(e)}")

    # Check if raw text was provided
    if text_content and text_content.strip():
        extracted_text = (extracted_text + "\n\n" + text_content.strip()).strip()

    # If no text provided, fetch study notes directly from notes.lpuverto.xyz!
    lpu_mcqs = []
    if fetch_lpuverto_data:
        try:
            # Try fetching real unit MCQs from notes.lpuverto.xyz
            lpu_mcqs = await LPUVertoService.get_unit_mcqs(semester, subject_code, unit)
            if not extracted_text:
                fetched_notes = await LPUVertoService.get_unit_notes(semester, subject_code, unit)
                extracted_text = fetched_notes
        except Exception as e:
            print(f"LPU Verto fetch error: {e}")

    # Fallback default text if still empty
    if not extracted_text.strip():
        extracted_text = f"Comprehensive syllabus and lecture material for {subject_name} ({subject_code}) based on Lovely Professional University academic curriculum."

    # Generate complete exam paper
    paper = await ExamGenerator.generate_exam(
        text_content=extracted_text,
        subject_code=subject_code,
        subject_name=subject_name,
        exam_type=exam_type,
        mcq_count=mcq_count,
        short_count=short_count,
        long_count=long_count,
        difficulty=difficulty,
        negative_marking=negative_marking,
        is_pro_user=is_pro,
        lpu_verto_mcqs=lpu_mcqs if fetch_lpuverto_data else None
    )

    return paper

# ── User & Google Authentication Endpoints ───────────────────────────────

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    lpu_reg_no: Optional[str] = None
    phone: Optional[str] = None

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    """Securely register a student with salted PBKDF2 password hashing."""
    res = UserService.register_user(
        name=req.name,
        email=req.email,
        password=req.password,
        lpu_reg_no=req.lpu_reg_no,
        phone=req.phone
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message"))
    try:
        Database.record_visit(
            session_id=res.get("session_token", "reg_sess"),
            path="/api/auth/register",
            user_id=req.name or req.email
        )
    except Exception:
        pass
    return res

class LoginRequest(BaseModel):
    identifier: str
    password: str

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    """Securely authenticate a student with Email or LPU Reg No and password."""
    res = UserService.login_user(
        identifier=req.identifier,
        password=req.password
    )
    if not res.get("success"):
        raise HTTPException(status_code=401, detail=res.get("message"))
    try:
        user_name = res.get("user", {}).get("name") or req.identifier
        Database.record_visit(
            session_id=res.get("session_token", "login_sess"),
            path="/api/auth/login",
            user_id=user_name
        )
    except Exception:
        pass
    return res

class GoogleAuthRequest(BaseModel):
    google_id: str
    name: str
    email: str
    picture: Optional[str] = None
    lpu_reg_no: Optional[str] = None
    phone: Optional[str] = None

@app.post("/api/auth/google")
async def google_auth(req: GoogleAuthRequest):
    """Authenticate or register student using Google account details."""
    res = UserService.google_auth(
        google_id=req.google_id,
        name=req.name,
        email=req.email,
        picture=req.picture,
        lpu_reg_no=req.lpu_reg_no,
        phone=req.phone
    )
    if res.get("success") and res.get("session_token"):
        try:
            Database.record_visit(
                session_id=res["session_token"],
                path="/api/auth/google",
                user_id=req.name or req.email
            )
        except Exception:
            pass
    return res

@app.get("/api/auth/me")
async def get_current_user(token: Optional[str] = Query(None), authorization: Optional[str] = Header(None)):
    """Fetch current logged-in user and active subscription status."""
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1].strip()
    user = UserService.get_user_by_token(token)
    if not user:
        return {"authenticated": False, "user": None}
    return {"authenticated": True, "user": user}

class UpdateProfileRequest(BaseModel):
    user_id: str
    lpu_reg_no: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None

@app.post("/api/auth/update-profile")
async def update_user_profile(req: UpdateProfileRequest):
    """Update student registration number or phone."""
    return UserService.update_profile(req.user_id, req.lpu_reg_no, req.phone, req.name)

# ── User Activities & Purchases History ───────────────────────────────────

class UserActivityRequest(BaseModel):
    user_id: Optional[str] = None
    activity_type: str
    title: str
    subject_code: Optional[str] = None
    details: Optional[Any] = None

@app.post("/api/user/activity")
async def record_user_activity_endpoint(req: UserActivityRequest):
    """Record student activity or response (mock tests, study assets, chat)."""
    act = UserService.record_user_activity(
        user_id=req.user_id or "guest",
        activity_type=req.activity_type,
        title=req.title,
        subject_code=req.subject_code,
        details=req.details
    )
    return {"success": True, "activity": act}

@app.get("/api/user/activities")
async def get_user_activities_endpoint(user_id: str = Query(...), limit: int = Query(50)):
    """Retrieve saved activities and question responses for a student account."""
    activities = UserService.get_user_activities(user_id, limit=limit)
    return {"success": True, "activities": activities}

@app.get("/api/user/purchases")
async def get_user_purchases_endpoint(user_id: str = Query(...)):
    """Retrieve all verified purchases, subject passes, and transaction receipts."""
    return UserService.get_user_purchases(user_id)

# ── Paywall & UPI Payment Endpoints (Destination: 8053122848@ptyes) ─────────

@app.get("/api/paywall/plans")
async def get_plans():
    return PaywallService.get_plans()

@app.get("/api/paywall/upi-info")
async def get_upi_info(amount: float = 49.0, plan_name: str = "Mock Test Pass"):
    """Get UPI ID (8053122848@ptyes), intent link, and dynamic QR code."""
    return {
        "upi_id": PaywallService.UPI_ID,
        "payee_name": PaywallService.UPI_PAYEE_NAME,
        "amount": amount,
        "payment_link": PaywallService.get_upi_payment_link(amount, plan_name),
        "qr_url": PaywallService.get_upi_qr_url(amount, plan_name)
    }

class CouponRequest(BaseModel):
    code: str
    plan_id: str

@app.post("/api/paywall/coupon")
async def validate_coupon(req: CouponRequest):
    return PaywallService.validate_coupon(req.code, req.plan_id)

class CheckoutRequest(BaseModel):
    plan_id: str
    payment_method: str = "upi"
    coupon_code: Optional[str] = None
    user_name: str = "LPU Student"
    reg_no: str = "12000000"
    phone: Optional[str] = None
    utr_ref: Optional[str] = None
    user_id: Optional[str] = None
    subject_code: Optional[str] = None

@app.post("/api/paywall/checkout")
async def checkout(req: CheckoutRequest):
    import asyncio
    res = PaywallService.process_checkout(
        plan_id=req.plan_id,
        payment_method=req.payment_method,
        coupon_code=req.coupon_code,
        user_name=req.user_name,
        reg_no=req.reg_no,
        phone=req.phone,
        utr_ref=req.utr_ref,
        user_id=req.user_id,
        subject_code=req.subject_code
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message"))

    # Auto-notify admin on WhatsApp when a real UPI payment is pending approval
    if res.get("pending") and not res.get("verified"):
        asyncio.create_task(_notify_admin_whatsapp(res, req))

    return res

async def _notify_admin_whatsapp(res: dict, req):
    """Send WhatsApp notification to admin (8053122848) when a pending payment needs approval."""
    try:
        callmebot_key = os.getenv("CALLMEBOT_API_KEY", "").strip()
        admin_phone = "918053122848"
        plan_name = res.get("plan", req.plan_id)
        amount = res.get("amount_paid", "?")
        utr = res.get("utr_ref", "N/A")
        tx_id = res.get("transaction_id", "N/A")
        student = req.user_name or "Student"
        reg = req.reg_no or "N/A"
        subj = req.subject_code or "General"

        msg = (
            f"🔔 AcadAssist Payment Pending!\n"
            f"Student: {student} (Reg: {reg})\n"
            f"Plan: {plan_name} | Subject: {subj}\n"
            f"Amount: ₹{amount} | UTR: {utr}\n"
            f"TxID: {tx_id}\n"
            f"➡️ Login to admin panel to approve."
        )
        encoded_msg = msg.replace(" ", "%20").replace("\n", "%0A")

        if callmebot_key:
            url = f"https://api.callmebot.com/whatsapp.php?phone={admin_phone}&apikey={callmebot_key}&text={encoded_msg}"
            async with httpx.AsyncClient(timeout=10) as client:
                await client.get(url)
        # Always log for admin visibility in server logs
        print(f"[PAYMENT PENDING] {student} | {plan_name} | ₹{amount} | UTR:{utr} | TxID:{tx_id}")
    except Exception as e:
        print(f"[WA NOTIFY ERROR] {e}")


@app.get("/api/paywall/verify")
async def verify_token(token: Optional[str] = Query(None)):
    return PaywallService.verify_token(token)

@app.get("/api/paywall/status/{tx_id}")
async def get_payment_status(tx_id: str):
    """Poll payment approval status. Returns is_approved=True with token when admin approves."""
    return PaywallService.check_payment_status(tx_id)

# ── AI Study Chat (Gemini-powered) ──────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    history: list = []

@app.post("/api/ai/chat")
async def ai_study_chat(req: ChatRequest):
    """
    Intelligent AI study assistant for LPU students.
    Configured for unlimited usage across multiple users with or without Gemini API key.
    """
    return await AIChatService.get_response(
        message=req.message,
        subject_code=req.subject_code,
        subject_name=req.subject_name,
        history=req.history
    )


# ── Mock Test Result Submission ──────────────────────────────────────────

class MockTestSubmitRequest(BaseModel):
    user_id: Optional[str] = None
    user_name: str = "LPU Student"
    subject_code: str
    subject_name: str
    exam_type: str = "Midterm Mock Test"
    score: float
    total_marks: float
    percentage: float
    grade: str
    summary: dict = {}

@app.post("/api/mock-test/submit")
async def submit_mock_test(req: MockTestSubmitRequest):
    """Save completed mock test scorecard to database for student & admin view."""
    return UserService.record_mock_test(
        user_id=req.user_id,
        user_name=req.user_name,
        subject_code=req.subject_code,
        subject_name=req.subject_name,
        exam_type=req.exam_type,
        score=req.score,
        total_marks=req.total_marks,
        percentage=req.percentage,
        grade=req.grade,
        summary=req.summary
    )

# ── Service Inquiries (EduCode, NeoBrowser, Handwritten, Web Dev, PPT) ────

class ServiceInquiryRequest(BaseModel):
    service_category: str
    student_name: str
    phone: str
    email: Optional[str] = None
    details: str
    subject_or_topic: Optional[str] = None
    deadline: Optional[str] = None
    budget: Optional[str] = None
    reg_no: Optional[str] = None
    urgency: Optional[str] = None
    custom_specs: Optional[Dict[str, Any]] = None

@app.post("/api/services/inquiry")
async def submit_service_inquiry(req: ServiceInquiryRequest):
    """Receive student service order inquiries and save to database."""
    full_details = req.details
    meta_tags = []
    if req.budget:
        meta_tags.append(f"Budget: ₹{req.budget}")
    if req.reg_no:
        meta_tags.append(f"Reg: {req.reg_no}")
    if req.urgency:
        meta_tags.append(f"Urgency: {req.urgency}")
    if req.custom_specs:
        specs_str = ", ".join(f"{k}: {v}" for k, v in req.custom_specs.items() if v)
        if specs_str:
            meta_tags.append(f"Specs: [{specs_str}]")
    if meta_tags:
        full_details = f"[{' | '.join(meta_tags)}]\n{req.details}"

    return UserService.record_service_inquiry(
        service_category=req.service_category,
        student_name=req.student_name,
        phone=req.phone,
        email=req.email,
        details=full_details,
        subject_or_topic=req.subject_or_topic,
        deadline=req.deadline
    )

# ── Admin Panel Endpoints (Master Control & Approvals) ─────────────────

class AdminLoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/admin/login")
async def admin_login(req: AdminLoginRequest):
    """Authenticate administrator with exact credentials."""
    res = AdminService.login(req.username, req.password)
    if not res.get("success"):
        raise HTTPException(status_code=401, detail=res.get("message"))
    return res

@app.get("/api/admin/stats")
async def get_admin_stats(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return AdminService.get_dashboard_stats()

@app.get("/api/admin/users")
async def get_admin_users(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return UserService.list_all_users()

class GrantPlanRequest(BaseModel):
    plan_id: str
    plan_name: str
    duration_days: int = 180
    subject_code: Optional[str] = None

@app.post("/api/admin/users/{user_id}/grant-plan")
async def admin_grant_plan(user_id: str, req: GrantPlanRequest, token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return UserService.grant_user_plan(user_id, req.plan_id, req.plan_name, req.duration_days, 0.0, req.subject_code)

@app.delete("/api/admin/users/{user_id}")
async def admin_delete_user(user_id: str, token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    success = UserService.delete_user(user_id)
    return {"success": success}

@app.get("/api/admin/transactions")
async def get_admin_transactions(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return PaywallService.list_all_transactions()

class TransactionStatusRequest(BaseModel):
    status: str

@app.post("/api/admin/transactions/{tx_id}/status")
async def admin_update_transaction_status(tx_id: str, req: TransactionStatusRequest, token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    success = PaywallService.update_transaction_status(tx_id, req.status)
    return {"success": success, "status": req.status}

@app.get("/api/admin/mock-tests")
async def get_admin_mock_tests(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return UserService.list_all_mock_tests()

@app.get("/api/admin/service-requests")
async def get_admin_service_requests(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return UserService.list_service_inquiries()

class ServiceStatusRequest(BaseModel):
    status: str

@app.post("/api/admin/service-requests/{req_id}/status")
async def admin_update_service_status(req_id: str, req: ServiceStatusRequest, token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    success = UserService.update_inquiry_status(req_id, req.status)
    return {"success": success, "status": req.status}

@app.get("/api/admin/export")
async def admin_export_data(token: Optional[str] = Query(None)):
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return AdminService.export_all_data()

@app.post("/api/admin/reset/revenue")
async def admin_reset_revenue(token: Optional[str] = Query(None)):
    """Reset all revenue and transaction records in the database."""
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return AdminService.reset_revenue()

@app.post("/api/admin/reset/users")
async def admin_reset_users(token: Optional[str] = Query(None)):
    """Reset all registered students in the database."""
    if not AdminService.verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin session.")
    return AdminService.reset_users()


# ── Printable Official LPU Exam Paper ────────────────────────────────────

class ExportRequest(BaseModel):
    paper: dict
    show_solutions: bool = False

@app.post("/api/export-printable", response_class=HTMLResponse)
async def export_printable(req: ExportRequest):
    p = req.paper
    show_sol = req.show_solutions

    mcqs_html = ""
    for q in p.get("sections", {}).get("section_a", {}).get("questions", []):
        opts_html = "".join([f"<div style='margin-left: 20px; margin-bottom: 4px;'><strong>({opt['label']})</strong> {opt['text']}</div>" for opt in q.get("options", [])])
        sol_html = ""
        if show_sol:
            sol_html = f"<div style='margin: 8px 0 12px 20px; padding: 8px; background: #f0fdf4; border-left: 3px solid #22c55e;'><strong>Ans: Option ({q.get('correct_option')})</strong><br><small>{q.get('explanation')}</small></div>"

        mcqs_html += f"""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; font-weight: 600;">
                <span>Q{q.get('q_number', 1)}. {q.get('question')}</span>
                <span>[1 Mark]</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 6px;">Tag: {q.get('pyq_tag', 'LPU PYQ')} | Bloom: {q.get('difficulty', 'Medium')}</div>
            {opts_html}
            {sol_html}
        </div>
        """

    short_html = ""
    for q in p.get("sections", {}).get("section_b", {}).get("questions", []):
        sol_html = ""
        if show_sol:
            sol_html = f"<div style='margin: 8px 0 12px 20px; padding: 8px; background: #f8fafc; border-left: 3px solid #3b82f6;'><strong>Model Solution:</strong><br><pre style='font-family: inherit; white-space: pre-wrap;'>{q.get('model_answer')}</pre><br><small><strong>Marking Rubric:</strong><br>{q.get('marking_rubric')}</small></div>"

        short_html += f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; font-weight: 600;">
                <span>Q{q.get('q_number', 1)}. {q.get('question')}</span>
                <span>[{q.get('marks', 5)} Marks]</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 6px;">CO: {q.get('course_outcome', 'CO1')} | {q.get('pyq_tag', 'LPU PYQ')}</div>
            {sol_html}
        </div>
        """

    long_html = ""
    for q in p.get("sections", {}).get("section_c", {}).get("questions", []):
        sol_html = ""
        if show_sol:
            sol_html = f"<div style='margin: 8px 0 12px 20px; padding: 8px; background: #f8fafc; border-left: 3px solid #8b5cf6;'><strong>Model Comprehensive Solution (Option A):</strong><br><pre style='font-family: inherit; white-space: pre-wrap;'>{q.get('model_answer')}</pre><br><small><strong>Marking Rubric:</strong><br>{q.get('marking_rubric')}</small></div>"

        long_html += f"""
        <div style="margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px dashed #cbd5e1;">
            <div style="display: flex; justify-content: space-between; font-weight: 600;">
                <span>Q{q.get('q_number', 1)} (A). {q.get('option_a')}</span>
                <span>[10 Marks]</span>
            </div>
            <div style="text-align: center; font-weight: bold; margin: 8px 0; color: #475569;">--- OR ---</div>
            <div style="display: flex; justify-content: space-between; font-weight: 600;">
                <span>Q{q.get('q_number', 1)} (B). {q.get('option_b')}</span>
                <span>[10 Marks]</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-top: 6px;">CO: {q.get('course_outcome', 'CO3')} | {q.get('pyq_tag', 'LPU ETE Section C')}</div>
            {sol_html}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{p.get('subject_code')} - {p.get('exam_title')}</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 40px; color: #111; line-height: 1.5; }}
            .header-table {{ width: 100%; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 15px; }}
            .roll-box {{ border: 1px solid #000; width: 160px; height: 26px; display: inline-block; vertical-align: middle; }}
            .instructions {{ font-size: 12px; margin-bottom: 20px; padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; }}
            .section-title {{ background: #0f172a; color: #fff; padding: 6px 10px; font-weight: bold; margin: 25px 0 15px 0; text-transform: uppercase; font-size: 13px; }}
            @media print {{
                body {{ margin: 15mm; font-size: 12pt; }}
                .no-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="margin-bottom: 20px; text-align: right;">
            <button onclick="window.print()" style="padding: 10px 20px; background: #f97316; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">🖨️ Print / Save as PDF</button>
        </div>

        <table class="header-table">
            <tr>
                <td style="text-align: center;">
                    <h2 style="margin: 0; text-transform: uppercase;">LOVELY PROFESSIONAL UNIVERSITY, PUNJAB</h2>
                    <h4 style="margin: 4px 0 10px 0;">{p.get('exam_title')} — {p.get('session')}</h4>
                </td>
            </tr>
            <tr>
                <td>
                    <table style="width: 100%; font-size: 13px;">
                        <tr>
                            <td><strong>Course Code:</strong> {p.get('subject_code')}</td>
                            <td><strong>Course Title:</strong> {p.get('subject_name')}</td>
                        </tr>
                        <tr>
                            <td><strong>Time Allowed:</strong> {p.get('duration_minutes')} Minutes</td>
                            <td><strong>Maximum Marks:</strong> {p.get('total_marks')}</td>
                        </tr>
                        <tr>
                            <td><strong>Student Registration No:</strong> <span class="roll-box"></span></td>
                            <td><strong>Negative Marking:</strong> {p.get('negative_mark_value', 0)} per wrong MCQ</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <div class="instructions">
            <strong>General Instructions for Candidates:</strong>
            <ul style="margin: 5px 0 0 20px; padding: 0;">
                {"".join([f"<li>{inst}</li>" for inst in p.get('instructions', [])])}
            </ul>
        </div>

        <div class="section-title">SECTION A: OBJECTIVE & MULTIPLE CHOICE QUESTIONS (Compulsory)</div>
        {mcqs_html}

        {f'<div class="section-title">SECTION B: SHORT / CONCEPTUAL QUESTIONS</div>' + short_html if short_html.strip() else ''}

        {f'<div class="section-title">SECTION C: COMPREHENSIVE / ANALYTICAL QUESTIONS (With Internal Choices)</div>' + long_html if long_html.strip() else ''}

        <div style="margin-top: 40px; text-align: center; border-top: 1px solid #ccc; padding-top: 10px; font-size: 11px; color: #64748b;">
            Generated via AcadAssist AI Exam Prep Platform • Aligned with LPU Curriculum Standards
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ── Admin Portal Page Route ──────────────────────────────────────────────

@app.get("/admin", response_class=FileResponse)
async def serve_admin_portal():
    """Serve the Master Admin Control & Payment Approval Portal."""
    admin_html = os.path.join(STATIC_DIR, "admin.html")
    if os.path.exists(admin_html):
        return FileResponse(admin_html)
    raise HTTPException(status_code=404, detail="Admin portal not found.")

# ── Visitor Analytics Logging ────────────────────────────────────────────

class VisitLogRequest(BaseModel):
    session_id: Optional[str] = None
    path: Optional[str] = "/"
    user_id: Optional[str] = None

@app.post("/api/analytics/visit")
async def record_visitor_hit(req: VisitLogRequest):
    """Log an active page hit/session for admin live visitor tracking."""
    session_id = req.session_id or "anon_guest"
    path = req.path or "/"
    Database.record_visit(
        session_id=session_id,
        path=path,
        user_id=req.user_id,
        ip="127.0.0.1",
        user_agent="browser"
    )
    return {"success": True}

# Serve Frontend static assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static_prefix")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

