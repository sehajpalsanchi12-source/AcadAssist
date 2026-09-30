import os
import re
import io
import json
from typing import Dict, List, Any, Optional

import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

class PPTService:
    """
    Automated PowerPoint (.pptx) & Slide Deck Generator for Lovely Professional University subjects.
    Supports all 266+ subjects scraped from notes.lpuverto.xyz as well as custom user-uploaded content.
    """

    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    PPTS_DIR = os.path.join(DATA_DIR, "ppts")
    ALL_SUBJECTS_FILE = os.path.join(DATA_DIR, "lpu_all_subjects.json")
    PYQ_BANK_FILE = os.path.join(DATA_DIR, "pyq_bank.json")

    # Brand Colors (AcadAssist & LPU Theme)
    COLOR_PRIMARY = RGBColor(225, 29, 72)     # Crimson / Rose #E11D48
    COLOR_DARK = RGBColor(15, 23, 42)         # Slate Dark #0F172A
    COLOR_ACCENT = RGBColor(245, 158, 11)     # Amber / Gold #F59E0B
    COLOR_CARD_BG = RGBColor(248, 250, 252)   # Light Slate BG #F8FAFC
    COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Border #E2E8F0
    COLOR_TEXT_MAIN = RGBColor(30, 41, 59)    # Dark text #1E293B
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)# Muted text #64748B
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_CODE_BG = RGBColor(30, 41, 59)      # Monospace Code Box BG #1E293B
    COLOR_CODE_TEXT = RGBColor(56, 189, 248)  # Light Cyan code text #38BDF8

    _subjects_cache: Optional[Dict[str, Any]] = None
    _pyq_cache: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def _ensure_dir(cls):
        os.makedirs(cls.PPTS_DIR, exist_ok=True)

    @classmethod
    def _load_subjects(cls) -> Dict[str, Any]:
        if cls._subjects_cache is None:
            if os.path.exists(cls.ALL_SUBJECTS_FILE):
                try:
                    with open(cls.ALL_SUBJECTS_FILE, "r", encoding="utf-8") as f:
                        cls._subjects_cache = json.load(f)
                except Exception as e:
                    print(f"Error loading {cls.ALL_SUBJECTS_FILE}: {e}")
                    cls._subjects_cache = {}
            else:
                cls._subjects_cache = {}
        return cls._subjects_cache

    @classmethod
    def _load_pyq(cls) -> List[Dict[str, Any]]:
        if cls._pyq_cache is None:
            if os.path.exists(cls.PYQ_BANK_FILE):
                try:
                    with open(cls.PYQ_BANK_FILE, "r", encoding="utf-8") as f:
                        cls._pyq_cache = json.load(f)
                except Exception as e:
                    print(f"Error loading {cls.PYQ_BANK_FILE}: {e}")
                    cls._pyq_cache = []
            else:
                cls._pyq_cache = []
        return cls._pyq_cache

    @classmethod
    def get_subject_data(cls, subject_code: str) -> Dict[str, Any]:
        """Fetch subject metadata or synthesize default fallback."""
        code_clean = subject_code.strip().upper()
        subjects = cls._load_subjects()
        if code_clean in subjects:
            return subjects[code_clean]
        
        # Check case-insensitive match
        for k, v in subjects.items():
            if k.upper() == code_clean:
                return v

        # Fallback synthetic course
        return {
            "code": code_clean,
            "name": f"{code_clean} Core Fundamentals",
            "semester": "Semester 1",
            "program": "Computer Science & Engineering",
            "credits": "3 Credits",
            "category": "Core",
            "description": f"Comprehensive curriculum and exam preparation for {code_clean}.",
            "units": [
                {"unit": 1, "title": "Fundamental Concepts & Definitions"},
                {"unit": 2, "title": "Architectural Models & Frameworks"},
                {"unit": 3, "title": "Algorithmic Implementations & Workflows"},
                {"unit": 4, "title": "System Design, Protocols & Trade-offs"},
                {"unit": 5, "title": "Advanced Paradigms & Optimization"},
                {"unit": 6, "title": "Emerging Applications & Case Studies"}
            ],
            "landing_url": f"https://notes.lpuverto.xyz/search?q={code_clean}"
        }

    @classmethod
    def generate_presentation_data(cls, subject_code: str, unit: Optional[int] = None) -> Dict[str, Any]:
        """
        Builds a comprehensive 8-12 slide deck data structure with titles, subtitles,
        bullet points, visual diagrams/pseudocode, exam tips, and speaker notes.
        """
        sub = cls.get_subject_data(subject_code)
        code = sub.get("code", subject_code.upper())
        name = sub.get("name", f"{code} Course Deck")
        program = sub.get("program", "School of Computer Science & Engineering")
        semester = sub.get("semester", "Current Academic Session")
        credits = sub.get("credits", "3-4 Credits")
        units = sub.get("units", [])

        # Check for pyq questions
        pyq_list = cls._load_pyq()
        relevant_pyqs = [p for p in pyq_list if p.get("subject_code", "").upper() == code]
        pyq_paper = relevant_pyqs[0] if relevant_pyqs else None

        slides: List[Dict[str, Any]] = []

        # ----------------------------------------------------
        # SLIDE 1: Title Slide (Widescreen Hero)
        # ----------------------------------------------------
        slides.append({
            "slide_number": 1,
            "slide_type": "title",
            "title": f"{code}: {name}",
            "subtitle": f"Lovely Professional University • Academic Presentation & Exam Revision Deck",
            "badge": f"{program} • {semester} • {credits}",
            "bullets": [
                f"Curated from official LPU Verto syllabus & notes repository (notes.lpuverto.xyz)",
                f"Mapped to Course Outcomes (CO1–CO6) and Bloom's Revised Taxonomy (Levels L1–L5)",
                f"Includes High-Yield Exam Formulas, End-Term (ETE) & Mid-Term (MTE) Question Breakdowns"
            ],
            "code_or_diagram": "",
            "exam_tip": f"Designed for students aiming for Grade O (10.0 CGPA) in {code}.",
            "speaker_notes": f"Welcome Vertos to the complete academic slide presentation for {code} ({name}). Today's session walks through theoretical foundations, implementation workflows, and high-frequency examination patterns."
        })

        # ----------------------------------------------------
        # SLIDE 2: Syllabus Architecture & 6-Unit Roadmap
        # ----------------------------------------------------
        unit_bullets = []
        for u in units:
            u_num = u.get("unit", "")
            u_title = u.get("title", f"Unit {u_num}")
            unit_bullets.append(f"Unit {u_num}: {u_title}")
        if not unit_bullets:
            unit_bullets = [
                "Unit 1: Theoretical Foundations & Primary Definitions",
                "Unit 2: Architectural Structures & Core Abstractions",
                "Unit 3: Algorithmic Workflows & Transformations",
                "Unit 4: Systems Analysis, Protocols & Memory Bounds",
                "Unit 5: Performance Tuning, Asymptotics & Security",
                "Unit 6: Practical Implementations & Case Studies"
            ]

        slides.append({
            "slide_number": 2,
            "slide_type": "agenda",
            "title": "Course Blueprint & Syllabus Progression",
            "subtitle": "Modular Breakdown across 6 Academic Units",
            "badge": "LPU Course Outline",
            "bullets": unit_bullets[:6],
            "code_or_diagram": (
                "+-------------------------------------------------------------------------+\n"
                "| [Unit 1 & 2: Foundations] ---> [Unit 3 & 4: Application] ---> [Unit 5 & 6: Mastery] |\n"
                "+-------------------------------------------------------------------------+\n"
                "  Continuous Assessment (CA1, CA2)   Mid-Term Exam (MTE)        End-Term Exam (ETE)"
            ),
            "exam_tip": "Units 1-3 form 100% of MTE syllabus; Units 1-6 form 100% of ETE with heavy emphasis on Units 4-6.",
            "speaker_notes": f"This blueprint outlines the progressive cognitive taxonomy for {code}. Make sure your notes align with the respective unit headings."
        })

        # ----------------------------------------------------
        # SLIDES 3-6: Detailed Unit Breakdowns
        # ----------------------------------------------------
        for idx in range(0, min(len(units), 4)):
            u = units[idx]
            u_no = u.get("unit", idx + 1)
            u_title = u.get("title", f"Unit {u_no} Topics")
            
            # Extract keywords or thematic focus
            words = [w for w in re.findall(r"[A-Za-z]{4,}", u_title) if w.lower() not in {"unit", "introduction", "overview", "study", "studies"}]
            topic_lead = words[0] if words else f"Core Concept {u_no}"
            topic_secondary = words[1] if len(words) > 1 else "Mechanisms"

            slides.append({
                "slide_number": len(slides) + 1,
                "slide_type": "content",
                "title": f"Unit {u_no}: {u_title}",
                "subtitle": f"Key Theoretical Tenets & Structural Mechanisms",
                "badge": f"Unit {u_no} Focus",
                "bullets": [
                    f"Formal Definition: Rigorous specification of {topic_lead} within {name}",
                    f"State Model: Transition pathways governed by {topic_secondary} constraints",
                    f"Invariants & Bounds: Mathematical guarantees ensuring system integrity and reliability",
                    f"Real-World Analogy: Industrial deployments and fault-tolerant architecture"
                ],
                "code_or_diagram": (
                    f"// Unit {u_no} Core Pipeline Paradigm\n"
                    f"[State S0: Init] ---> [Transform: {topic_lead}] ---> [Validation]\n"
                    f"                                    │\n"
                    f"                                    ▼\n"
                    f"                     [State S1: Verified Output]"
                ),
                "exam_tip": f"Frequent 5-mark question in MTE/ETE: 'Explain the working principle and operational characteristics of {topic_lead} with an illustrative diagram.'",
                "speaker_notes": f"When teaching or studying Unit {u_no}, highlight the invariant properties. In LPU examinations, students who draw state transitions get full 5/5 marks in Section B."
            })

        # ----------------------------------------------------
        # SLIDE 7: High-Yield Algorithmic Workflows & Pseudocode
        # ----------------------------------------------------
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "code",
            "title": f"Algorithmic Workflows & Pseudocode Implementation",
            "subtitle": f"Deterministic execution patterns in {code}",
            "badge": "Implementation Logic",
            "bullets": [
                "Precondition Verification: Bounds and null pointer validation before invocation",
                "Core Processing Loop: Iterative state progression maintaining invariant stability",
                "Exception Trapping: Graceful fallback paths preventing unhandled runtime faults",
                "Resource Teardown: Deterministic deallocation mitigating memory leaks"
            ],
            "code_or_diagram": (
                f"algorithm Execute_{code.lower()}_routine(dataset, threshold):\n"
                f"    Input: dataset D of n elements, numeric limit T\n"
                f"    Output: optimized transformation R\n"
                f"    1. if length(D) == 0 or threshold <= 0 then return NULL\n"
                f"    2. initialize accumulator R <- empty_list()\n"
                f"    3. for each record r in D do:\n"
                f"    4.     transformed <- compute_state_metric(r)\n"
                f"    5.     if transformed.score >= T then\n"
                f"    6.         R.append(transformed)\n"
                f"    7. return sort_by_relevance(R)"
            ),
            "exam_tip": "Always write pseudocode with clear indentation, explicit input/output specifications, and step numbering in Section C answers.",
            "speaker_notes": "Walk through this algorithm step-by-step. Note that step 1 prevents edge-case runtime aborts."
        })

        # ----------------------------------------------------
        # SLIDE 8: Asymptotic Analysis & Performance Trade-offs
        # ----------------------------------------------------
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "table",
            "title": "Complexity Analysis & Architectural Trade-offs",
            "subtitle": "Asymptotic bounds and memory footprint comparison",
            "badge": "Performance Matrix",
            "bullets": [
                "Time Complexity: Best Case O(1) • Average Case O(n log n) • Worst Case O(n²)",
                "Space Complexity: O(1) auxiliary space achieved via in-place state manipulation",
                "Scalability Vector: Horizontal partitioning minimizes cache thrashing under concurrent read loads",
                "Trade-off Principle: Prioritizing read throughput introduces minimal write amplification"
            ],
            "code_or_diagram": (
                "+-------------------------------------------------------------------+\n"
                "| Metric / Operation       | Best Case    | Average Case | Worst Case   |\n"
                "+-------------------------------------------------------------------+\n"
                "| Primary Lookups          | O(1)         | O(log n)     | O(n)         |\n"
                "| Batch State Mutations    | O(n)         | O(n log n)   | O(n²)        |\n"
                "| Auxiliary Memory Bounds  | O(1)         | O(log n)     | O(n)         |\n"
                "+-------------------------------------------------------------------+"
            ),
            "exam_tip": "LPU evaluators award 2 extra marks if you contrast worst-case Big-O with tight Theta bounds and cite hardware cache locality.",
            "speaker_notes": "Explain how auxiliary space impacts microservice memory limits and embedded system execution."
        })

        # ----------------------------------------------------
        # SLIDE 9: LPU Examination Blueprint & Marking Scheme
        # ----------------------------------------------------
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "exam",
            "title": f"LPU Examination Blueprint & Scoring Rubrics",
            "subtitle": f"End-Term (ETE) & Mid-Term (MTE) Question Distribution for {code}",
            "badge": "Exam Rubric",
            "bullets": [
                "Part A (20 Marks): 10-20 Objective MCQs & Short Conceptual Definitions (Negative marking -0.25 on competitive sets)",
                "Part B (30 Marks): 6 Analytical Questions (5 Marks each) requiring precise diagrams, step derivations, and comparisons",
                "Part C (20 Marks): 2 Comprehensive Long Questions (10 Marks each) demanding end-to-end design and code implementations",
                "Target Threshold: Aim for 65+ / 70 to secure Grade O (10.0 CGPA) or A+ (9.0+ CGPA)"
            ],
            "code_or_diagram": (
                "Exam Time Allocation (3 Hours / 180 Minutes):\n"
                "  • 00 - 30 min : Part A (MCQ speed & accuracy, mark sure answers first)\n"
                "  • 30 - 110 min: Part B (13 mins per 5-mark answer with labeled diagram)\n"
                "  • 110 - 165 min: Part C (25 mins per 10-mark answer with code + architecture)\n"
                "  • 165 - 180 min: Final Review (underline keywords, verify indices)"
            ),
            "exam_tip": "Never leave questions unattempted. Even partial state definitions or block diagrams yield 2-3 step marks in Part B & C.",
            "speaker_notes": "Guide students on disciplined exam time management. Most marks are lost in Part B due to time exhaustion, not lack of knowledge."
        })

        # ----------------------------------------------------
        # SLIDE 10: Authentic PYQ Spotlight (from PYQ Bank if available)
        # ----------------------------------------------------
        if pyq_paper:
            part_a_data = pyq_paper.get("part_a", [])
            part_b_data = pyq_paper.get("part_b", [])
            sample_part_a = part_a_data if isinstance(part_a_data, list) else part_a_data.get("questions", [])
            sample_part_b = part_b_data if isinstance(part_b_data, list) else part_b_data.get("questions", [])
            q_bullets = []
            for q in sample_part_a[:2]:
                q_bullets.append(f"PYQ Part A ({q.get('marks', 2)}M): {q.get('question', '')[:90]}...")
            for q in sample_part_b[:1]:
                q_bullets.append(f"PYQ Part B ({q.get('marks', 5)}M): {q.get('question', '')[:90]}...")
            pyq_slide_bullets = q_bullets if q_bullets else [
                f"Sample Question 1: Distinguish between static allocation and dynamic memory dispatch in {code}.",
                f"Sample Question 2: Derive the recurrence equation and solve using Master Theorem.",
                f"Sample Question 3: Explain the fault-recovery mechanism under network partition."
            ]
        else:
            pyq_slide_bullets = [
                f"Sample Question 1: Explain the operational lifecycle and fundamental primitives of {code} (5 Marks).",
                f"Sample Question 2: Draw the architectural block diagram and discuss state transitions (5 Marks).",
                f"Sample Question 3: Design a complete end-to-end workflow to solve high-concurrency bottlenecks (10 Marks).",
                f"Sample Question 4: Compare and contrast theoretical guarantees vs empirical execution speeds (5 Marks)."
            ]

        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "pyq",
            "title": f"Previous Year Questions (PYQ) Spotlight",
            "subtitle": f"Recurring Themes from LPU End-Term Examinations (2021–2024)",
            "badge": "LPU PYQ Bank",
            "bullets": pyq_slide_bullets,
            "code_or_diagram": (
                "+-------------------------------------------------------------------+\n"
                "| Golden Rule for 10-Mark Questions in LPU:                         |\n"
                "| 1. Formal Definition (1 Mark)                                     |\n"
                "| 2. Labeled Architectural / Block Diagram (3 Marks)                |\n"
                "| 3. Step-by-Step Working Principle / Mathematical Formula (3 Marks)|\n"
                "| 4. Pseudocode / Implementation Snippet (2 Marks)                  |\n"
                "| 5. Complexity & Edge Case Analysis (1 Mark)                       |\n"
                "+-------------------------------------------------------------------+"
            ),
            "exam_tip": "High frequency topics repeat every 2 to 3 semesters. Check the AcadAssist PYQ Explorer tab for complete papers and model solutions.",
            "speaker_notes": "Present these questions to test class understanding. Ask students how they would break down the 10-mark question rubric."
        })

        # ----------------------------------------------------
        # SLIDE 11: Summary & High-Score Revision Strategy
        # ----------------------------------------------------
        slides.append({
            "slide_number": len(slides) + 1,
            "slide_type": "summary",
            "title": "Comprehensive Summary & Preparation Checklist",
            "subtitle": "Your roadmap to Grade O / 10 CGPA",
            "badge": "Revision Action Plan",
            "bullets": [
                f"Review complete unit-wise study notes on AcadAssist & notes.lpuverto.xyz",
                "Practice 50+ topic-wise MCQs to build speed and eliminate negative marking errors",
                "Solve at least 2 full-length 3-hour mock papers under timed exam conditions",
                "Review cheat sheet formulas and algorithmic invariants the night before the examination"
            ],
            "code_or_diagram": (
                "AcadAssist Learning Ecosystem:\n"
                "  • Notes & Study Studio  : Instant notes, cheat sheets, & flashcards\n"
                "  • PYQ Question Bank     : Authentic past papers with model answers\n"
                "  • Timed Mock Test Engine: Real exam timer with instant score analysis\n"
                "  • Slide Deck Presenter  : Fullscreen projector mode for classroom revision"
            ),
            "exam_tip": "Confidence comes from structured practice. Best of luck for your LPU examinations, Vertos!",
            "speaker_notes": "Conclude the presentation. Direct students to the AcadAssist portal to take their practice mock test."
        })

        return {
            "subject_code": code,
            "subject_name": name,
            "program": program,
            "semester": semester,
            "credits": credits,
            "total_slides": len(slides),
            "generated_at": "Academic Session 2025-2026",
            "landing_url": sub.get("landing_url", f"https://notes.lpuverto.xyz/search?q={code}"),
            "slides": slides
        }

    @classmethod
    def create_pptx(cls, deck_data: Dict[str, Any], output_path: Optional[str] = None) -> bytes:
        """
        Creates a high-resolution, beautifully styled Microsoft PowerPoint (.pptx) file
        in 16:9 widescreen format using python-pptx.
        """
        prs = pptx.Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        blank_layout = prs.slide_layouts[6]
        slides = deck_data.get("slides", [])
        code = deck_data.get("subject_code", "LPU")
        name = deck_data.get("subject_name", "Academic Deck")

        for s_idx, slide_info in enumerate(slides):
            slide = prs.slides.add_slide(blank_layout)
            slide_type = slide_info.get("slide_type", "content")

            # 1. Slide Background Top Accent Banner
            banner_height = Inches(0.18)
            banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), banner_height)
            banner.fill.solid()
            banner.fill.fore_color.rgb = cls.COLOR_PRIMARY
            banner.line.color.rgb = cls.COLOR_PRIMARY

            # 2. Slide Type Specific Layout
            if slide_type == "title":
                cls._render_title_slide(slide, slide_info, code, name)
            elif slide_type == "code":
                cls._render_code_slide(slide, slide_info)
            else:
                cls._render_standard_slide(slide, slide_info)

            # 3. Footer Bar across all slides
            cls._render_footer(slide, s_idx + 1, len(slides), code)

            # 4. Attach Speaker Notes
            notes_text = slide_info.get("speaker_notes", "")
            if notes_text:
                slide.notes_slide.notes_text_frame.text = notes_text

        # Save to buffer
        buf = io.BytesIO()
        prs.save(buf)
        data = buf.getvalue()

        # Save to file if output_path specified
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(data)

        return data

    @classmethod
    def _render_title_slide(cls, slide, info: Dict[str, Any], code: str, name: str):
        # Badge
        badge_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(0.5))
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = (info.get("badge") or "LOVELY PROFESSIONAL UNIVERSITY • OFFICIAL STUDY DECK").upper()
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = cls.COLOR_PRIMARY

        # Main Title Box
        title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(1.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = info.get("title", f"{code}: {name}")
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = cls.COLOR_DARK

        # Subtitle Box
        sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(11.333), Inches(0.8))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        p2 = tf_s.paragraphs[0]
        p2.text = info.get("subtitle", "Comprehensive Academic Presentation & Exam Revision Deck")
        p2.font.size = Pt(17)
        p2.font.color.rgb = cls.COLOR_TEXT_MUTED

        # Content Card (Left Column)
        card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.9), Inches(6.8), Inches(2.7))
        card_shape.fill.solid()
        card_shape.fill.fore_color.rgb = cls.COLOR_CARD_BG
        card_shape.line.color.rgb = cls.COLOR_CARD_BORDER
        card_shape.line.width = Pt(1)

        # Bullets inside Card
        bullets_box = slide.shapes.add_textbox(Inches(1.2), Inches(4.0), Inches(6.4), Inches(2.5))
        tf_c = bullets_box.text_frame
        tf_c.word_wrap = True
        bullets = info.get("bullets", [])
        for i, b in enumerate(bullets):
            p = tf_c.paragraphs[0] if i == 0 else tf_c.add_paragraph()
            p.text = f"•  {b}"
            p.font.size = Pt(13)
            p.font.color.rgb = cls.COLOR_TEXT_MAIN
            p.space_after = Pt(8)

        # Exam Tip Card (Right Column)
        tip_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(3.9), Inches(4.2), Inches(2.7))
        tip_shape.fill.solid()
        tip_shape.fill.fore_color.rgb = RGBColor(254, 242, 242) # Light Rose BG
        tip_shape.line.color.rgb = cls.COLOR_PRIMARY
        tip_shape.line.width = Pt(1.5)

        tip_box = slide.shapes.add_textbox(Inches(8.3), Inches(4.1), Inches(3.8), Inches(2.3))
        tf_tip = tip_box.text_frame
        tf_tip.word_wrap = True
        p_th = tf_tip.paragraphs[0]
        p_th.text = "🎯 LPU ACADEMIC GOAL"
        p_th.font.size = Pt(12)
        p_th.font.bold = True
        p_th.font.color.rgb = cls.COLOR_PRIMARY
        p_th.space_after = Pt(10)

        p_tc = tf_tip.add_paragraph()
        p_tc.text = info.get("exam_tip", "Master all 6 units for 10.0 CGPA (Grade O).")
        p_tc.font.size = Pt(13)
        p_tc.font.color.rgb = cls.COLOR_TEXT_MAIN
        p_tc.space_after = Pt(8)

        p_tlink = tf_tip.add_paragraph()
        p_tlink.text = "🔗 Notes: notes.lpuverto.xyz"
        p_tlink.font.size = Pt(11)
        p_tlink.font.color.rgb = cls.COLOR_TEXT_MUTED

    @classmethod
    def _render_standard_slide(cls, slide, info: Dict[str, Any]):
        # Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.4))
        tf_b = badge_box.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = (info.get("badge") or "ACADEMIC OUTLINE").upper()
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = cls.COLOR_PRIMARY

        # Header Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = info.get("title", "Lecture Slide")
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = cls.COLOR_DARK

        # Subtitle
        sub_text = info.get("subtitle", "")
        if sub_text:
            p_sub = tf.add_paragraph()
            p_sub.text = sub_text
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = cls.COLOR_TEXT_MUTED

        # Left Column: Bullets Card
        has_diagram = bool(info.get("code_or_diagram", "").strip())
        left_width = Inches(6.4) if has_diagram else Inches(11.733)

        card_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), left_width, Inches(4.7))
        card_left.fill.solid()
        card_left.fill.fore_color.rgb = cls.COLOR_CARD_BG
        card_left.line.color.rgb = cls.COLOR_CARD_BORDER
        card_left.line.width = Pt(1)

        bullets_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), left_width - Inches(0.4), Inches(4.4))
        tf_b = bullets_box.text_frame
        tf_b.word_wrap = True
        bullets = info.get("bullets", [])
        for i, b in enumerate(bullets):
            p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p.text = f"•  {b}"
            p.font.size = Pt(13)
            p.font.color.rgb = cls.COLOR_TEXT_MAIN
            p.space_after = Pt(10)

        # Exam Tip at the bottom of left card
        tip = info.get("exam_tip", "")
        if tip:
            p_tip = tf_b.add_paragraph()
            p_tip.text = f"🎯 Exam Tip: {tip}"
            p_tip.font.size = Pt(11)
            p_tip.font.bold = True
            p_tip.font.color.rgb = cls.COLOR_PRIMARY
            p_tip.space_before = Pt(8)

        # Right Column: Diagram or Matrix if present
        if has_diagram:
            card_right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.4), Inches(1.85), Inches(5.133), Inches(4.7))
            card_right.fill.solid()
            card_right.fill.fore_color.rgb = cls.COLOR_DARK
            card_right.line.color.rgb = cls.COLOR_DARK

            diag_box = slide.shapes.add_textbox(Inches(7.55), Inches(2.0), Inches(4.8), Inches(4.4))
            tf_d = diag_box.text_frame
            tf_d.word_wrap = True
            
            p_dh = tf_d.paragraphs[0]
            p_dh.text = "DIAGRAM / SYSTEM SCHEMATIC"
            p_dh.font.size = Pt(10)
            p_dh.font.bold = True
            p_dh.font.color.rgb = cls.COLOR_ACCENT
            p_dh.space_after = Pt(8)

            p_dc = tf_d.add_paragraph()
            p_dc.text = info.get("code_or_diagram", "").strip()
            p_dc.font.size = Pt(9.5)
            p_dc.font.name = "Courier New"
            p_dc.font.color.rgb = RGBColor(226, 232, 240)

    @classmethod
    def _render_code_slide(cls, slide, info: Dict[str, Any]):
        # Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.4))
        tf_b = badge_box.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = (info.get("badge") or "TECHNICAL IMPLEMENTATION").upper()
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = cls.COLOR_PRIMARY

        # Header Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = info.get("title", "Algorithm & Pseudocode")
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = cls.COLOR_DARK

        # Subtitle
        sub_text = info.get("subtitle", "")
        if sub_text:
            p_sub = tf.add_paragraph()
            p_sub.text = sub_text
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = cls.COLOR_TEXT_MUTED

        # Left Column: Code Window Box (Dark Terminal Theme)
        card_code = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(6.8), Inches(4.7))
        card_code.fill.solid()
        card_code.fill.fore_color.rgb = cls.COLOR_CODE_BG
        card_code.line.color.rgb = cls.COLOR_CODE_BG

        code_box = slide.shapes.add_textbox(Inches(0.95), Inches(2.0), Inches(6.5), Inches(4.4))
        tf_c = code_box.text_frame
        tf_c.word_wrap = True

        p_ch = tf_c.paragraphs[0]
        p_ch.text = "TERMINAL // PSEUDOCODE"
        p_ch.font.size = Pt(10)
        p_ch.font.bold = True
        p_ch.font.color.rgb = cls.COLOR_ACCENT
        p_ch.space_after = Pt(8)

        p_code = tf_c.add_paragraph()
        p_code.text = info.get("code_or_diagram", "").strip()
        p_code.font.size = Pt(10)
        p_code.font.name = "Courier New"
        p_code.font.color.rgb = cls.COLOR_CODE_TEXT

        # Right Column: Execution Rules & Exam Tip
        card_right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.85), Inches(4.733), Inches(4.7))
        card_right.fill.solid()
        card_right.fill.fore_color.rgb = cls.COLOR_CARD_BG
        card_right.line.color.rgb = cls.COLOR_CARD_BORDER
        card_right.line.width = Pt(1)

        notes_box = slide.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.4))
        tf_n = notes_box.text_frame
        tf_n.word_wrap = True
        
        p_nh = tf_n.paragraphs[0]
        p_nh.text = "EXECUTION & EVALUATION PRINCIPLES"
        p_nh.font.size = Pt(11)
        p_nh.font.bold = True
        p_nh.font.color.rgb = cls.COLOR_PRIMARY
        p_nh.space_after = Pt(10)

        bullets = info.get("bullets", [])
        for b in bullets:
            p = tf_n.add_paragraph()
            p.text = f"•  {b}"
            p.font.size = Pt(12)
            p.font.color.rgb = cls.COLOR_TEXT_MAIN
            p.space_after = Pt(8)

        tip = info.get("exam_tip", "")
        if tip:
            p_tip = tf_n.add_paragraph()
            p_tip.text = f"🎯 Exam Tip: {tip}"
            p_tip.font.size = Pt(11)
            p_tip.font.bold = True
            p_tip.font.color.rgb = cls.COLOR_PRIMARY
            p_tip.space_before = Pt(8)

    @classmethod
    def _render_footer(cls, slide, current_idx: int, total_slides: int, code: str):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"AcadAssist • LPU Academic Presentation • {code} • Powered by notes.lpuverto.xyz"
        p.font.size = Pt(9)
        p.font.color.rgb = cls.COLOR_TEXT_MUTED

        p_page = tf.add_paragraph()
        p_page.text = f"Slide {current_idx} of {total_slides}"
        p_page.font.size = Pt(9)
        p_page.font.bold = True
        p_page.font.color.rgb = cls.COLOR_PRIMARY
        p_page.alignment = PP_ALIGN.RIGHT

    @classmethod
    def get_or_create_subject_pptx(cls, subject_code: str) -> str:
        """
        Retrieves cached .pptx path or compiles and saves a new .pptx file for the subject.
        Returns the absolute filesystem path to the .pptx file.
        """
        cls._ensure_dir()
        code_clean = subject_code.strip().upper()
        file_path = os.path.join(cls.PPTS_DIR, f"{code_clean}_presentation.pptx")

        if os.path.exists(file_path) and os.path.getsize(file_path) > 1024:
            return file_path

        deck_data = cls.generate_presentation_data(code_clean)
        cls.create_pptx(deck_data, output_path=file_path)
        return file_path

    @classmethod
    def generate_all_subjects(cls, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Batch generates presentation slide decks for all subjects in catalog.
        """
        cls._ensure_dir()
        subjects = cls._load_subjects()
        subject_keys = list(subjects.keys())
        if limit:
            subject_keys = subject_keys[:limit]

        generated = []
        errors = []

        for code in subject_keys:
            try:
                path = cls.get_or_create_subject_pptx(code)
                generated.append({"code": code, "path": path, "size_bytes": os.path.getsize(path)})
            except Exception as e:
                errors.append({"code": code, "error": str(e)})

        return {
            "total_requested": len(subject_keys),
            "total_generated": len(generated),
            "errors_count": len(errors),
            "generated": generated[:10], # sample
            "errors": errors
        }

    @classmethod
    def generate_custom_pptx(cls, title: str, text: str, code: str = "CUSTOM", unit: str = "Unit 1") -> bytes:
        """
        Builds a custom presentation from uploaded student notes or Study Studio prompt.
        """
        from app.services.study_asset_generator import StudyAssetGenerator
        slides_json = StudyAssetGenerator.generate_slides(text, code, title, unit)
        
        # Transform slides into PPT deck format
        deck_data = {
            "subject_code": code,
            "subject_name": title,
            "program": "Lovely Professional University",
            "semester": "Current Term",
            "credits": "Custom Module",
            "slides": slides_json.get("slides", [])
        }
        return cls.create_pptx(deck_data)
