import os
import re
import json
import random
import urllib.parse
from typing import Dict, List, Any, Optional

class StudyAssetGenerator:
    """
    Generates various learning and revision assets from subject materials:
    1. Full Comprehensive Notes with AI Vector Diagram Images
    2. Short Revision Notes / Cheat Sheet
    3. Interactive Presentation Slides
    4. Week-by-Week / Day-by-Day Learning Roadmap
    5. MCQs & PYQ Practice Sets
    """

    @classmethod
    def _create_architecture_diagram_svg(cls, subject_code: str, k1: str, k2: str) -> str:
        """Create a polished, modern vector architecture diagram image (URL-encoded data URI)."""
        safe_code = subject_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_k1 = k1[:20].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_k2 = k2[:20].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 230" width="100%" height="230">'
            f'<defs>'
            f'<linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#1e293b"/></linearGradient>'
            f'<linearGradient id="box1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f97316"/><stop offset="100%" stop-color="#ea580c"/></linearGradient>'
            f'<linearGradient id="box2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#1d4ed8"/></linearGradient>'
            f'<linearGradient id="box3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#047857"/></linearGradient>'
            f'<marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/>'
            f'</marker>'
            f'</defs>'
            f'<rect width="700" height="230" rx="14" fill="url(#bgGrad)"/>'
            f'<text x="350" y="32" fill="#f8fafc" font-size="13" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">{safe_code} • Architecture &amp; Execution Pipeline</text>'
            f'<rect x="40" y="65" width="170" height="85" rx="10" fill="url(#box1)"/>'
            f'<text x="125" y="98" fill="#ffffff" font-size="12" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">Input Layer</text>'
            f'<text x="125" y="118" fill="#fed7aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">{safe_k1}</text>'
            f'<text x="125" y="135" fill="#ffedd5" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Preconditions Checked</text>'
            f'<line x1="210" y1="107" x2="265" y2="107" stroke="#94a3b8" stroke-width="2.5" marker-end="url(#arrow)"/>'
            f'<text x="238" y="98" fill="#94a3b8" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Dispatch</text>'
            f'<rect x="270" y="65" width="170" height="85" rx="10" fill="url(#box2)"/>'
            f'<text x="355" y="98" fill="#ffffff" font-size="12" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">Processing Engine</text>'
            f'<text x="355" y="118" fill="#bfdbfe" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">{safe_k2}</text>'
            f'<text x="355" y="135" fill="#dbeafe" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">State Transformations</text>'
            f'<line x1="440" y1="107" x2="495" y2="107" stroke="#94a3b8" stroke-width="2.5" marker-end="url(#arrow)"/>'
            f'<text x="468" y="98" fill="#94a3b8" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Commit</text>'
            f'<rect x="500" y="65" width="160" height="85" rx="10" fill="url(#box3)"/>'
            f'<text x="580" y="98" fill="#ffffff" font-size="12" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">Output State</text>'
            f'<text x="580" y="118" fill="#a7f3d0" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Deterministic State</text>'
            f'<text x="580" y="135" fill="#d1fae5" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Bounded Overhead</text>'
            f'<rect x="40" y="175" width="620" height="32" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>'
            f'<text x="350" y="196" fill="#94a3b8" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">📊 LPU Exam Evaluation Rubric: Section C answers with labeled architecture diagrams earn top marks.</text>'
            f'</svg>'
        )
        return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

    @classmethod
    def _create_flowchart_diagram_svg(cls, subject_code: str, k1: str, k2: str) -> str:
        """Create a state flowchart diagram image."""
        safe_code = subject_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_k1 = k1[:18].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_k2 = k2[:18].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 230" width="100%" height="230">'
            f'<defs>'
            f'<linearGradient id="flowBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#18181b"/><stop offset="100%" stop-color="#27272a"/></linearGradient>'
            f'<marker id="fArrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="#f59e0b"/>'
            f'</marker>'
            f'</defs>'
            f'<rect width="700" height="230" rx="14" fill="url(#flowBg)"/>'
            f'<text x="350" y="32" fill="#fafafa" font-size="13" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">{safe_code} • Algorithmic Flow &amp; State Invariant Transitions</text>'
            f'<rect x="40" y="65" width="120" height="60" rx="8" fill="#4338ca"/>'
            f'<text x="100" y="93" fill="#ffffff" font-size="11" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">START</text>'
            f'<text x="100" y="110" fill="#c7d2fe" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Init {safe_k1}</text>'
            f'<line x1="160" y1="95" x2="215" y2="95" stroke="#f59e0b" stroke-width="2" marker-end="url(#fArrow)"/>'
            f'<polygon points="280,65 340,95 280,125 220,95" fill="#b45309" stroke="#f59e0b" stroke-width="1.5"/>'
            f'<text x="280" y="93" fill="#ffffff" font-size="10" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">Condition</text>'
            f'<text x="280" y="106" fill="#fef3c7" font-size="8" font-family="system-ui,sans-serif" text-anchor="middle">Valid Bound?</text>'
            f'<line x1="340" y1="95" x2="415" y2="95" stroke="#f59e0b" stroke-width="2" marker-end="url(#fArrow)"/>'
            f'<text x="375" y="88" fill="#10b981" font-size="9" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">YES</text>'
            f'<rect x="420" y="65" width="140" height="60" rx="8" fill="#047857"/>'
            f'<text x="490" y="93" fill="#ffffff" font-size="11" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">Execute {safe_k2}</text>'
            f'<text x="490" y="110" fill="#a7f3d0" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">Loop Iteration</text>'
            f'<line x1="560" y1="95" x2="615" y2="95" stroke="#f59e0b" stroke-width="2" marker-end="url(#fArrow)"/>'
            f'<rect x="620" y="65" width="50" height="60" rx="8" fill="#b91c1c"/>'
            f'<text x="645" y="100" fill="#ffffff" font-size="11" font-weight="bold" font-family="system-ui,sans-serif" text-anchor="middle">END</text>'
            f'<line x1="280" y1="125" x2="280" y2="160" stroke="#f59e0b" stroke-width="2"/>'
            f'<line x1="280" y1="160" x2="645" y2="160" stroke="#f59e0b" stroke-width="2"/>'
            f'<line x1="645" y1="160" x2="645" y2="125" stroke="#f59e0b" stroke-width="2" marker-end="url(#fArrow)"/>'
            f'<text x="300" y="145" fill="#ef4444" font-size="9" font-weight="bold" font-family="system-ui,sans-serif">NO: Exit Bounds</text>'
            f'<rect x="40" y="185" width="630" height="28" rx="6" fill="#3f3f46"/>'
            f'<text x="355" y="203" fill="#d4d4d8" font-size="9.5" font-family="system-ui,sans-serif" text-anchor="middle">Time Complexity: O(1) best • O(N log N) average • Space: O(1) auxiliary bounds</text>'
            f'</svg>'
        )
        return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

    @classmethod
    def generate_full_notes(cls, text: str, subject_code: str, subject_name: str, unit: str = "Unit 1") -> Dict[str, Any]:
        """Generate structured textbook-quality comprehensive notes with sections, tables, and AI diagram images."""
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        sentences = [s.strip() for s in re.split(r"[.\n]+", text) if len(s.strip()) > 20]

        # Extract primary topics
        words = re.findall(r"\b[A-Z][a-zA-Z0-9_\-]{2,}\b|\b[a-z]{4,}\b", text)
        stops = {"this", "that", "with", "from", "have", "were", "which", "there", "their", "about", "using", "these", "could", "would", "other", "after", "before"}
        keywords = list(dict.fromkeys([w for w in words if w.lower() not in stops]))[:15]
        if not keywords:
            keywords = ["Concepts", "Architecture", "Algorithms", "Optimization", "Implementation"]

        k1 = keywords[0] if len(keywords) > 0 else "Fundamentals"
        k2 = keywords[1] if len(keywords) > 1 else "Core Principles"
        k3 = keywords[2] if len(keywords) > 2 else "Advanced Execution"

        # Generate vector diagram images
        arch_diagram = cls._create_architecture_diagram_svg(subject_code, k1, k2)
        flow_diagram = cls._create_flowchart_diagram_svg(subject_code, k1, k2)

        # Construct sections with embedded diagram images
        sections = [
            {
                "heading": f"1. Orientation & Theoretical Foundations of {k1}",
                "diagram_image": arch_diagram,
                "content": (
                    f"{subject_name} ({subject_code}) establishes foundational paradigms critical for academic mastery at Lovely Professional University.\n\n"
                    f"**Core Definitions:**\n"
                    f"• **{k1}:** Represents the primary structural mechanism designed for systematic state management and execution.\n"
                    f"• **{k2}:** Provides modular abstraction layers to isolate processing logic from lower-level memory boundaries.\n\n"
                    f"**Significance in LPU Curriculum:**\n"
                    f"Mastery of {k1} and {k2} is directly mapped to Course Outcome 1 (CO1) and frequently constitutes 15–20% of the Mid-Term (MTE) and End-Term (ETE) evaluation rubrics."
                )
            },
            {
                "heading": f"2. Detailed Mechanism & Algorithmic Workflow of {k2}",
                "diagram_image": flow_diagram,
                "content": (
                    f"The operational lifecycle follows a rigorous, deterministic sequence:\n\n"
                    f"1. **Precondition Validation:** Verification of resource constraints and input boundaries.\n"
                    f"2. **Processing Pipeline:** Iterative state transformations guided by {k2} rules.\n"
                    f"3. **State Finalization & Cleanup:** Committing outputs and mitigating memory leaks.\n\n"
                    f"**Key Invariant:** Consistency is maintained throughout transactional cycles, guaranteeing fault tolerance under concurrent workloads."
                )
            },
            {
                "heading": f"3. Comparative Analysis: {k1} vs {k2}",
                "content": (
                    f"Understanding trade-offs is essential for LPU 5-mark conceptual questions:\n\n"
                    f"| Criterion | {k1} | {k2} |\n"
                    f"|---|---|---|\n"
                    f"| Primary Purpose | Foundational structure & allocation | Workflow coordination & transformation |\n"
                    f"| Time Complexity | O(1) / O(log n) typical | O(n) dependent on workload complexity |\n"
                    f"| Space Overhead | Low auxiliary memory footprint | Moderate heap allocation for state caching |\n"
                    f"| LPU Exam Frequency | Appeared in ETE 2023, 2024 | Recurring MTE Section B favorite |"
                )
            },
            {
                "heading": f"4. High-Yield LPU Exam Takeaways & Common Traps",
                "content": (
                    f"• **Trap #1:** Confusing best-case execution bounds with amortized average complexity.\n"
                    f"• **Trap #2:** Omitting base cases or resource release calls, leading to memory overflow.\n"
                    f"• **Evaluation Tip:** When answering 10-mark questions in Section C, always provide: (1) Formal Definition, (2) Block Diagram, (3) Pseudocode / Syntax, and (4) Complexity Analysis to secure maximum marks."
                )
            }
        ]

        # Merge extracted sentences from uploaded text
        if sentences:
            sample_insights = "\n".join([f"• {s}." for s in sentences[:8] if not s.endswith(".")])
            sections.insert(1, {
                "heading": f"Extracted Material Summary & Key Insights",
                "content": f"The provided study text emphasizes the following essential points:\n\n{sample_insights}"
            })

        return {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "unit": unit,
            "total_read_time": "7 mins read",
            "sections": sections
        }

    @classmethod
    def generate_short_notes(cls, text: str, subject_code: str, subject_name: str, unit: str = "Unit 1") -> Dict[str, Any]:
        """Generate high-yield revision flashcards, 1-liner memory triggers, and exam cheat sheets."""
        words = re.findall(r"\b[A-Z][a-zA-Z0-9_\-]{2,}\b|\b[a-z]{4,}\b", text)
        stops = {"this", "that", "with", "from", "have", "were", "which", "there", "their", "about", "using", "these"}
        keywords = list(dict.fromkeys([w for w in words if w.lower() not in stops]))[:12]
        if not keywords:
            keywords = ["Algorithm", "Complexity", "Memory", "Architecture", "Optimization"]

        cheat_sheet = [
            {"topic": "Core Principle", "summary": f"{keywords[0] if keywords else 'Core Concept'} is the central paradigm evaluated in {unit} of {subject_code}."},
            {"topic": "Time Complexity Matrix", "summary": "Best: O(1) • Average: O(n log n) • Worst-case: O(n²) under degenerate pivots/imbalances."},
            {"topic": "Space Bound", "summary": "Auxiliary space is bounded by O(1) for iterative approaches and O(n) for recursive stacks."},
            {"topic": "Key Differences", "summary": f"Distinguish clearly between linear vs non-linear representation in {subject_name}."},
            {"topic": "LPU Examiner Favorite", "summary": "State diagrams and step-by-step trace tables receive 70% of rubric marks in Section B."}
        ]

        flashcards = []
        for i, kw in enumerate(keywords[:6]):
            flashcards.append({
                "id": i + 1,
                "question": f"What is the primary role of '{kw}' in {subject_name}?",
                "answer": f"It acts as a primary building block for ensuring deterministic execution, data integrity, and modular scalability.",
                "exam_tag": "High-Yield Flashcard"
            })

        formulas_or_rules = [
            "1. Base Address Formula: Loc(A[i]) = Base + (i - Lower_Bound) * Size",
            "2. Amdahl's Law Speedup: S = 1 / ((1 - P) + (P / N))",
            "3. Recurrence Relation: T(n) = 2T(n/2) + O(n) => O(n log n) via Master Theorem",
            "4. Negative Marking Rule: 1 Correct = +1.0 Mark | 1 Incorrect = -0.25 Mark"
        ]

        return {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "unit": unit,
            "cheat_sheet": cheat_sheet,
            "flashcards": flashcards,
            "high_yield_formulas": formulas_or_rules
        }

    @classmethod
    def generate_slides(cls, text: str, subject_code: str, subject_name: str, unit: str = "Unit 1") -> Dict[str, Any]:
        """Generate a complete slide presentation deck with slide numbers, bullets, code, and speaker notes."""
        words = re.findall(r"\b[A-Z][a-zA-Z0-9_\-]{2,}\b|\b[a-z]{4,}\b", text)
        stops = {"this", "that", "with", "from", "have", "were", "which", "there", "their", "about", "using"}
        keywords = list(dict.fromkeys([w for w in words if w.lower() not in stops]))[:10]
        if not keywords:
            keywords = ["Introduction", "Architecture", "Execution", "Evaluation", "Conclusion"]

        slides = [
            {
                "slide_number": 1,
                "title": f"{subject_name} ({subject_code})",
                "subtitle": f"LPU Comprehensive Lecture & Revision Deck • {unit}",
                "bullets": [
                    "Lovely Professional University — School of Computer Science & Engineering",
                    f"Course Code: {subject_code} | Session 2025–2026",
                    "Mapped to Course Outcomes: CO1, CO2 & Bloom's Levels L1–L4"
                ],
                "code_or_diagram": "",
                "speaker_notes": f"Welcome Vertos. Today we unpack {unit} covering foundational definitions, structural mechanisms, and LPU exam patterns."
            },
            {
                "slide_number": 2,
                "title": f"1. Architectural Overview & Context",
                "subtitle": f"Foundational Pillars of {keywords[0] if keywords else 'the Domain'}",
                "bullets": [
                    f"Defines systematic organization and state management across computing boundaries",
                    f"Mitigates resource bottlenecks through efficient memory hierarchy allocation",
                    "Directly addresses standard LPU Continuous Assessment (CA) objective items"
                ],
                "code_or_diagram": (
                    "+-------------------------------------------------------+\n"
                    "|              User Application / Client Layer         |\n"
                    "+-------------------------------------------------------+\n"
                    "                           │\n"
                    "                           ▼\n"
                    "+-------------------------------------------------------+\n"
                    f"|           {keywords[0] if keywords else 'Core Engine'} Optimization Layer           |\n"
                    "+-------------------------------------------------------+\n"
                    "                           │\n"
                    "                           ▼\n"
                    "+-------------------------------------------------------+\n"
                    "|             Hardware & Runtime Memory Bounds          |\n"
                    "+-------------------------------------------------------+"
                ),
                "speaker_notes": "Emphasize to students that Section A MCQs often target the boundary interface between the application layer and runtime bounds."
            },
            {
                "slide_number": 3,
                "title": f"2. Algorithmic Workflow & Pseudocode",
                "subtitle": "Step-by-step execution logic",
                "bullets": [
                    "Input validation ensures preconditions are met prior to loop entry",
                    "State accumulator tracks intermediate transitions deterministically",
                    "Early termination breaks prevent infinite recursion cycles"
                ],
                "code_or_diagram": (
                    f"def execute_{keywords[1].lower() if len(keywords) > 1 else 'process'}(stream_data):\n"
                    "    # Step 1: Precondition check\n"
                    "    if not stream_data:\n"
                    "        return {'status': 'EMPTY', 'code': 400}\n"
                    "    \n"
                    "    # Step 2: Processing pipeline\n"
                    "    result_buffer = []\n"
                    "    for item in stream_data:\n"
                    "        processed = transform(item)\n"
                    "        result_buffer.append(processed)\n"
                    "    return {'status': 'SUCCESS', 'payload': result_buffer}"
                ),
                "speaker_notes": "Walk through the code line by line. Highlight that LPU evaluators look for proper error condition checks."
            },
            {
                "slide_number": 4,
                "title": f"3. Space-Time Complexity & Trade-Offs",
                "subtitle": "Asymptotic analysis for Mid-Term & End-Term papers",
                "bullets": [
                    "Time Complexity: Best Case O(1) • Average Case O(n log n) • Worst Case O(n²)",
                    "Space Complexity: Auxiliary memory bounded by O(1) for in-place algorithms",
                    "Hardware Cache Locality: Contiguous sequential access yields optimal cache hit ratios"
                ],
                "code_or_diagram": (
                    "Complexity Comparison Matrix:\n"
                    "--------------------------------------------------\n"
                    "Algorithm       Best        Average     Worst\n"
                    "--------------------------------------------------\n"
                    "Linear Flow     O(1)        O(n)        O(n)\n"
                    "Binary Split    O(1)        O(log n)    O(log n)\n"
                    "Divide-Conquer  O(n log n)  O(n log n)  O(n log n)\n"
                    "--------------------------------------------------"
                ),
                "speaker_notes": "Remind students that Big-O notation represents an upper bound, while Theta represents a tight bound."
            },
            {
                "slide_number": 5,
                "title": f"4. LPU Exam Strategy & Scoring Blueprint",
                "subtitle": "How to secure full marks (Grade O / A+)",
                "bullets": [
                    "Section A (MCQs): Beware of negative marking (-0.25). Skip if completely unsure.",
                    "Section B (5 Marks): Always pair written explanations with a neat labeled block diagram or table.",
                    "Section C (10 Marks): Address both theoretical derivation and practical pseudocode implementations.",
                    "Check notes.lpuverto.xyz for recent PYQ repeat frequency and mock test series."
                ],
                "code_or_diagram": "",
                "speaker_notes": "Conclude with words of encouragement. Reinforce the value of time management during the 3-hour End Term Examination."
            }
        ]

        return {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "unit": unit,
            "total_slides": len(slides),
            "slides": slides
        }


    @classmethod
    async def generate_roadmap(cls, text: str, subject_code: str, subject_name: str) -> Dict[str, Any]:
        """
        Generate an AI-powered 9+ CGPA study roadmap with:
        - Subject-specific unit-wise study structure
        - High-yield important questions per unit (MCQ + 5-mark + 10-mark)
        - Day-by-day 7-day intensive schedule tailored to this subject
        - Key formulas, theorems, and must-know concepts
        Uses Gemini AI when API key is available; falls back to rich heuristic plan.
        """
        import os, httpx

        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

        if gemini_key and len(text.strip()) > 50:
            try:
                prompt = f"""You are an expert LPU (Lovely Professional University) academic coach specializing in helping students achieve 9+ CGPA.

Generate a comprehensive 9+ CGPA study roadmap for: **{subject_name} ({subject_code})**

Subject notes/content provided:
---
{text[:8000]}
---

Return ONLY a valid JSON object (no markdown, no code fences) with this exact structure:
{{
  "subject_code": "{subject_code}",
  "subject_name": "{subject_name}",
  "target_goal": "Achieve 9+ CGPA (Grade O / A+) in LPU {subject_name} Examinations",
  "exam_strategy": {{
    "ca_tip": "Strategy for 10-mark CA (2 tests × 5 marks)",
    "mte_tip": "Strategy for 30-mark Mid-Term Exam",
    "ete_tip": "Strategy for 100-mark End-Term Exam (60 MCQ + Part B + Part C)",
    "negative_marking_tip": "How to handle -0.25 negative marking"
  }},
  "units": [
    {{
      "unit_no": 1,
      "unit_title": "Unit title from syllabus",
      "key_topics": ["topic1", "topic2", "topic3", "topic4"],
      "must_know_formulas": ["Formula or theorem 1", "Formula or theorem 2"],
      "important_questions": {{
        "mcq": [
          {{"q": "MCQ question text?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "B", "explanation": "Why B is correct"}},
          {{"q": "MCQ question text 2?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "A", "explanation": "Why A is correct"}}
        ],
        "five_mark": [
          {{"q": "5-mark question", "answer_outline": "Key points: 1. Point one 2. Point two 3. Point three (with diagram if needed)"}}
        ],
        "ten_mark": [
          {{"q": "10-mark question", "answer_outline": "Structured answer: Introduction → Theory → Example → Diagram description → Conclusion"}}
        ]
      }}
    }},
    {{
      "unit_no": 2,
      "unit_title": "Unit 2 title",
      "key_topics": ["topic1", "topic2", "topic3"],
      "must_know_formulas": ["Formula 1"],
      "important_questions": {{
        "mcq": [
          {{"q": "MCQ?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "C", "explanation": "Explanation"}}
        ],
        "five_mark": [{{"q": "5-mark question", "answer_outline": "Key points"}}],
        "ten_mark": [{{"q": "10-mark question", "answer_outline": "Structured answer"}}]
      }}
    }},
    {{
      "unit_no": 3,
      "unit_title": "Unit 3 title",
      "key_topics": ["topic1", "topic2"],
      "must_know_formulas": ["Formula 1"],
      "important_questions": {{
        "mcq": [{{"q": "MCQ?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "A", "explanation": "Explanation"}}],
        "five_mark": [{{"q": "5-mark question", "answer_outline": "Key points"}}],
        "ten_mark": [{{"q": "10-mark question", "answer_outline": "Structured answer"}}]
      }}
    }},
    {{
      "unit_no": 4,
      "unit_title": "Unit 4 title",
      "key_topics": ["topic1", "topic2"],
      "must_know_formulas": [],
      "important_questions": {{
        "mcq": [{{"q": "MCQ?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "B", "explanation": "Explanation"}}],
        "five_mark": [{{"q": "5-mark question", "answer_outline": "Key points"}}],
        "ten_mark": [{{"q": "10-mark question", "answer_outline": "Structured answer"}}]
      }}
    }},
    {{
      "unit_no": 5,
      "unit_title": "Unit 5 title",
      "key_topics": ["topic1", "topic2"],
      "must_know_formulas": [],
      "important_questions": {{
        "mcq": [{{"q": "MCQ?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "D", "explanation": "Explanation"}}],
        "five_mark": [{{"q": "5-mark question", "answer_outline": "Key points"}}],
        "ten_mark": [{{"q": "10-mark question", "answer_outline": "Structured answer"}}]
      }}
    }},
    {{
      "unit_no": 6,
      "unit_title": "Unit 6 title",
      "key_topics": ["topic1", "topic2"],
      "must_know_formulas": [],
      "important_questions": {{
        "mcq": [{{"q": "MCQ?", "options": ["A) opt1", "B) opt2", "C) opt3", "D) opt4"], "answer": "C", "explanation": "Explanation"}}],
        "five_mark": [{{"q": "5-mark question", "answer_outline": "Key points"}}],
        "ten_mark": [{{"q": "10-mark question", "answer_outline": "Structured answer"}}]
      }}
    }}
  ],
  "study_tracks": [
    {{
      "track_name": "⚡ 7-Day 9+ CGPA Sprint for {subject_name}",
      "days": [
        {{"day": "Day 1", "focus": "Unit 1: [specific topic]", "hours": 3, "tasks": ["task1 specific to this subject", "task2", "task3"], "checkpoint": "Specific milestone for this subject"}},
        {{"day": "Day 2", "focus": "Unit 2: [specific topic]", "hours": 3.5, "tasks": ["task1", "task2", "task3"], "checkpoint": "Milestone"}},
        {{"day": "Day 3", "focus": "Unit 3 + MTE Mock", "hours": 4, "tasks": ["task1", "task2", "task3"], "checkpoint": "Score >= 24/30 on MTE Simulation"}},
        {{"day": "Day 4", "focus": "Unit 4: [specific topic]", "hours": 3.5, "tasks": ["task1", "task2", "task3"], "checkpoint": "Milestone"}},
        {{"day": "Day 5", "focus": "Units 5 & 6 + PYQ Study", "hours": 4, "tasks": ["task1", "task2", "task3"], "checkpoint": "Milestone"}},
        {{"day": "Day 6", "focus": "Full ETE 100-Mark Simulation", "hours": 4.5, "tasks": ["Sit for full 3-Hour Timed ETE Mock in Simulator", "Review wrong answers", "Revise weak units"], "checkpoint": "Overall Grade >= A+ on scorecard"}},
        {{"day": "Day 7", "focus": "Final Revision & Mental Rest", "hours": 2, "tasks": ["Read cheat sheets & flashcards one last time", "Review PYQ repeat-probability tags", "Pack Hall Ticket and LPU Student ID"], "checkpoint": "Ready to excel in LPU Examination Hall!"}}
      ]
    }}
  ]
}}

Be specific to {subject_name} - use actual topic names, real formula names, real concept terminology. Make questions exam-realistic at LPU difficulty level."""

                models_to_try = ["gemini-3.5-flash", "gemini-3-flash-preview"]
                roadmap = None

                for model in models_to_try:
                    try:
                        async with httpx.AsyncClient(timeout=5.0) as client:
                            resp = await client.post(
                                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}",
                                json={
                                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                                    "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.4}
                                }
                            )
                        if resp.status_code == 200:
                            result = resp.json()
                            candidates = result.get("candidates", [])
                            if candidates:
                                raw = candidates[0]["content"]["parts"][0]["text"].strip()
                                if raw.startswith("```"):
                                    raw = raw.split("```")[1]
                                    if raw.startswith("json"):
                                        raw = raw[4:]
                                roadmap = json.loads(raw.strip())
                                roadmap["ai_generated"] = True
                                return roadmap
                    except Exception as model_err:
                        print(f"[ROADMAP AI error on {model}]: {model_err}")
                        continue
            except Exception as e:
                print(f"[ROADMAP AI ERROR] {e} — falling back to heuristic")

        # ── Fallback: Rich heuristic roadmap with subject-specific content ──
        words = text.lower().split() if text else []
        # Detect subject domain from code and text
        is_math = any(x in subject_code.lower() for x in ["mth", "mat", "math"])
        is_physics = any(x in subject_code.lower() for x in ["phy", "phys"])
        is_cse = any(x in subject_code.lower() for x in ["cse", "cs", "data", "algo"])
        is_chemistry = any(x in subject_code.lower() for x in ["che", "chem"])
        is_electronics = any(x in subject_code.lower() for x in ["ece", "elec"])

        if is_math:
            units = [
                {"unit_no": 1, "unit_title": "Differential Equations & Applications", "key_topics": ["First Order ODE", "Separable Equations", "Bernoulli's Equation", "Exact Equations"], "must_know_formulas": ["dy/dx + Py = Q (Linear ODE)", "Integrating factor: e^∫P dx", "Bernoulli substitution: v = y^(1-n)"], "important_questions": {"mcq": [{"q": "Which of the following is the integrating factor for dy/dx + y = e^x?", "options": ["A) e^x", "B) e^(-x)", "C) x", "D) e^(2x)"], "answer": "A", "explanation": "IF = e^∫1 dx = e^x"}], "five_mark": [{"q": "Solve the ODE: dy/dx + 2y = 4x", "answer_outline": "1. IF = e^2x 2. Multiply both sides 3. Integrate 4. Solve for y"}], "ten_mark": [{"q": "Explain and solve Bernoulli's differential equation with an example from engineering.", "answer_outline": "Definition → Standard form → Substitution v=y^(1-n) → Reduction to linear ODE → Solve → Back-substitute → Application example"}]}},
                {"unit_no": 2, "unit_title": "Vector Calculus & Gradient", "key_topics": ["Gradient, Divergence, Curl", "Line Integrals", "Green's Theorem", "Stokes' Theorem"], "must_know_formulas": ["∇f = (∂f/∂x)i + (∂f/∂y)j + (∂f/∂z)k", "Divergence: ∇·F", "Curl: ∇×F", "Green's Theorem: ∮C P dx + Q dy = ∬(∂Q/∂x - ∂P/∂y) dA"], "important_questions": {"mcq": [{"q": "The curl of a gradient of any scalar function is always:", "options": ["A) Zero vector", "B) Unit vector", "C) Non-zero", "D) Infinity"], "answer": "A", "explanation": "curl(grad f) = ∇×∇f = 0 always"}], "five_mark": [{"q": "Find the divergence of F = x²i + y²j + z²k", "answer_outline": "div F = ∂(x²)/∂x + ∂(y²)/∂y + ∂(z²)/∂z = 2x + 2y + 2z"}], "ten_mark": [{"q": "State and prove Green's Theorem and apply it to evaluate a given line integral.", "answer_outline": "Statement → Conditions → Proof (split domain) → Example integral → Geometric interpretation → Engineering applications"}]}},
                {"unit_no": 3, "unit_title": "Laplace Transforms", "key_topics": ["Definition & Properties", "Inverse Laplace", "Convolution Theorem", "Application to ODE"], "must_know_formulas": ["L{f(t)} = ∫₀^∞ e^(-st) f(t) dt", "L{e^(at)} = 1/(s-a)", "L{sin(at)} = a/(s²+a²)", "L{cos(at)} = s/(s²+a²)"], "important_questions": {"mcq": [{"q": "The Laplace transform of t^n is:", "options": ["A) n!/s^n", "B) n!/s^(n+1)", "C) (n-1)!/s^n", "D) n/s^(n+1)"], "answer": "B", "explanation": "L{t^n} = n!/s^(n+1) for s > 0"}], "five_mark": [{"q": "Find L{3e^(2t) + 5sin(3t)}", "answer_outline": "Apply linearity: 3·L{e^2t} + 5·L{sin3t} = 3/(s-2) + 15/(s²+9)"}], "ten_mark": [{"q": "Use Laplace transforms to solve the IVP: y'' - 3y' + 2y = e^t, y(0)=1, y'(0)=0", "answer_outline": "Take LT of both sides → Substitute initial conditions → Solve for Y(s) → Partial fractions → Inverse LT → Solution"}]}},
                {"unit_no": 4, "unit_title": "Fourier Series", "key_topics": ["Fourier Coefficients", "Even & Odd Functions", "Half-Range Series", "Parseval's Theorem"], "must_know_formulas": ["a₀ = (1/L)∫f(x)dx", "aₙ = (1/L)∫f(x)cos(nπx/L)dx", "bₙ = (1/L)∫f(x)sin(nπx/L)dx"], "important_questions": {"mcq": [{"q": "For an even function, the Fourier series contains:", "options": ["A) Only sine terms", "B) Only cosine terms", "C) Both sine and cosine", "D) Constant term only"], "answer": "B", "explanation": "Even function: bₙ = 0, so only cosine and a₀"}], "five_mark": [{"q": "Find the Fourier coefficient a₀ for f(x) = x in [-π, π]", "answer_outline": "a₀ = (1/π)∫₋π^π x dx = 0 (odd function integral over symmetric interval)"}], "ten_mark": [{"q": "Find the Fourier series of f(x) = x² in [-π, π] and deduce the sum π²/6 = Σ1/n²", "answer_outline": "Compute a₀, aₙ; use integration by parts; write series; apply Parseval's theorem to deduce π²/6"}]}},
                {"unit_no": 5, "unit_title": "Partial Differential Equations", "key_topics": ["Wave Equation", "Heat Equation", "Laplace Equation", "Method of Separation"], "must_know_formulas": ["Wave: ∂²u/∂t² = c²∂²u/∂x²", "Heat: ∂u/∂t = k∂²u/∂x²", "Laplace: ∂²u/∂x² + ∂²u/∂y² = 0"], "important_questions": {"mcq": [{"q": "The heat equation ∂u/∂t = k∂²u/∂x² is:", "options": ["A) Hyperbolic", "B) Parabolic", "C) Elliptic", "D) None"], "answer": "B", "explanation": "B²-4AC = 0 for heat equation → parabolic"}], "five_mark": [{"q": "Classify the PDE: u_xx + 4u_xy + 4u_yy = 0", "answer_outline": "A=1, B=4, C=4 → B²-4AC = 16-16 = 0 → Parabolic PDE"}], "ten_mark": [{"q": "Solve the 1D heat equation using separation of variables with boundary conditions u(0,t)=u(L,t)=0, u(x,0)=f(x)", "answer_outline": "Assume u=X(x)T(t) → X''/X = T'/kT = -λ² → Solve X and T ODEs → Apply BCs → Fourier series for f(x)"}]}},
                {"unit_no": 6, "unit_title": "Numerical Methods & Applications", "key_topics": ["Newton-Raphson", "Euler's Method", "Runge-Kutta", "Simpson's Rule"], "must_know_formulas": ["Newton-Raphson: x_(n+1) = x_n - f(x_n)/f'(x_n)", "Euler: y_(n+1) = y_n + h·f(x_n, y_n)", "Simpson's 1/3: h/3[y₀+4y₁+2y₂+...+yₙ]"], "important_questions": {"mcq": [{"q": "Newton-Raphson method converges:", "options": ["A) Linearly", "B) Quadratically", "C) Cubically", "D) Does not converge"], "answer": "B", "explanation": "Error ~ [f(root)]² so convergence is quadratic (order 2)"}], "five_mark": [{"q": "Apply Newton-Raphson method to find √2 starting from x₀=1", "answer_outline": "f(x)=x²-2, f'(x)=2x → x₁=1-(-1/2)=1.5 → x₂=1.5-(0.25/3)=1.4167 → converges to 1.4142"}], "ten_mark": [{"q": "Using Runge-Kutta 4th order method, solve dy/dx = x+y, y(0)=1 for y(0.1)", "answer_outline": "k₁=h·f(x₀,y₀), k₂=h·f(x₀+h/2, y₀+k₁/2), k₃=h·f(x₀+h/2, y₀+k₂/2), k₄=h·f(x₀+h, y₀+k₃) → y₁=y₀+(k₁+2k₂+2k₃+k₄)/6"}]}}
            ]
        elif is_cse:
            units = [
                {"unit_no": 1, "unit_title": "Fundamentals & Problem Solving", "key_topics": ["Algorithm Design", "Flowcharts", "Pseudocode", "Time Complexity Basics"], "must_know_formulas": ["Time Complexity: O(n), O(log n), O(n²)", "Space Complexity analysis", "Best/Average/Worst Case"], "important_questions": {"mcq": [{"q": "The time complexity of binary search is:", "options": ["A) O(n)", "B) O(log n)", "C) O(n log n)", "D) O(1)"], "answer": "B", "explanation": "Binary search halves the search space each iteration → O(log n)"}], "five_mark": [{"q": "Explain the concept of time complexity with examples of O(1), O(n), and O(n²).", "answer_outline": "Define Big-O → O(1) example (array access) → O(n) example (linear search) → O(n²) example (bubble sort) → Comparison table"}], "ten_mark": [{"q": "Write an algorithm for binary search and analyze its time and space complexity.", "answer_outline": "Algorithm steps → Pseudocode → Trace with example → Best case O(1) → Worst case O(log n) → Space O(1) iterative vs O(log n) recursive"}]}},
                {"unit_no": 2, "unit_title": "Arrays, Strings & Sorting", "key_topics": ["Array Operations", "String Manipulation", "Bubble/Selection/Insertion Sort", "Merge Sort"], "must_know_formulas": ["Bubble Sort: O(n²) worst", "Merge Sort: O(n log n)", "Quick Sort: O(n²) worst, O(n log n) avg"], "important_questions": {"mcq": [{"q": "Which sorting algorithm is stable and has O(n log n) worst case?", "options": ["A) Quick Sort", "B) Heap Sort", "C) Merge Sort", "D) Bubble Sort"], "answer": "C", "explanation": "Merge Sort is stable and always O(n log n)"}], "five_mark": [{"q": "Trace bubble sort on array [5, 3, 8, 1, 2] showing each pass.", "answer_outline": "Pass 1: [3,5,1,2,8] → Pass 2: [3,1,2,5,8] → Pass 3: [1,2,3,5,8] → Pass 4: No swaps → Sorted"}], "ten_mark": [{"q": "Explain Merge Sort with algorithm, trace on [38,27,43,3,9,82,10] and complexity analysis.", "answer_outline": "Divide phase → Recursively sort halves → Merge step → Full trace → Recurrence T(n)=2T(n/2)+n → Master theorem → O(n log n)"}]}},
                {"unit_no": 3, "unit_title": "Linked Lists & Stacks/Queues", "key_topics": ["Singly/Doubly Linked List", "Stack (LIFO)", "Queue (FIFO)", "Circular Queue"], "must_know_formulas": ["Stack: PUSH O(1), POP O(1)", "Queue: Enqueue O(1), Dequeue O(1)", "Node structure: data + next pointer"], "important_questions": {"mcq": [{"q": "In a stack, which operation adds an element?", "options": ["A) Dequeue", "B) Push", "C) Pop", "D) Insert"], "answer": "B", "explanation": "PUSH adds to top of stack in O(1)"}], "five_mark": [{"q": "Write algorithm for insertion in a doubly linked list at a given position.", "answer_outline": "Create new node → Traverse to position → Adjust prev and next pointers → Handle edge cases (head, tail)"}], "ten_mark": [{"q": "Implement a queue using two stacks and analyze time complexity of each operation.", "answer_outline": "Two stacks S1, S2 → Enqueue: push to S1 O(1) → Dequeue: if S2 empty, pop all from S1 to S2 O(n) amortized O(1) → Explain amortization"}]}},
                {"unit_no": 4, "unit_title": "Trees & Binary Search Trees", "key_topics": ["Binary Tree Traversals", "BST Insert/Delete/Search", "AVL Tree", "Height Balanced Trees"], "must_know_formulas": ["Height of BST: O(log n) avg, O(n) worst", "Inorder of BST = sorted output", "Balance Factor = |height(L) - height(R)| ≤ 1"], "important_questions": {"mcq": [{"q": "Inorder traversal of a BST gives:", "options": ["A) Random output", "B) Reverse sorted", "C) Sorted ascending", "D) Level order"], "answer": "C", "explanation": "BST property ensures inorder = left→root→right = ascending"}], "five_mark": [{"q": "Insert 50, 30, 70, 20, 40 into a BST and draw the resulting tree.", "answer_outline": "Root=50 → 30<50 left → 70>50 right → 20<30 left → 40>30 right → Draw final tree with 5 nodes"}], "ten_mark": [{"q": "Explain AVL tree rotations (LL, RR, LR, RL) with examples and explain why AVL ensures O(log n) operations.", "answer_outline": "AVL property → Imbalance cases → LL: single right rotation → RR: single left rotation → LR: left then right → RL: right then left → Height proof → O(log n) guaranteed"}]}},
                {"unit_no": 5, "unit_title": "Graphs & Shortest Paths", "key_topics": ["BFS", "DFS", "Dijkstra's Algorithm", "Minimum Spanning Tree"], "must_know_formulas": ["BFS: O(V+E)", "DFS: O(V+E)", "Dijkstra: O(V² or E log V)", "Kruskal: O(E log E)"], "important_questions": {"mcq": [{"q": "Which algorithm finds the shortest path in an unweighted graph?", "options": ["A) DFS", "B) BFS", "C) Dijkstra", "D) Prim's"], "answer": "B", "explanation": "BFS explores level by level, guaranteeing shortest path in unweighted graphs"}], "five_mark": [{"q": "Apply BFS on a graph with 5 nodes starting from vertex 1 and list the traversal order.", "answer_outline": "Queue: [1] → Dequeue 1, enqueue neighbors → Continue level by level → Show visited array → Final order"}], "ten_mark": [{"q": "Explain Dijkstra's shortest path algorithm with a weighted graph example and time complexity analysis.", "answer_outline": "Initialize dist[] → Priority queue → Relax edges → Update distances → Trace on example graph → Time O(V²) with array, O(E log V) with heap → Limitation (no negative weights)"}]}},
                {"unit_no": 6, "unit_title": "Dynamic Programming & Greedy", "key_topics": ["Memoization vs Tabulation", "0/1 Knapsack", "LCS", "Activity Selection"], "must_know_formulas": ["0/1 Knapsack DP table", "LCS: L[i][j] = L[i-1][j-1]+1 if match", "Greedy: locally optimal → globally optimal"], "important_questions": {"mcq": [{"q": "Dynamic Programming is based on:", "options": ["A) Greedy choice", "B) Divide and conquer only", "C) Optimal substructure & overlapping subproblems", "D) Backtracking"], "answer": "C", "explanation": "DP requires both optimal substructure and overlapping subproblems"}], "five_mark": [{"q": "Solve the 0/1 Knapsack problem for items with weights [2,3,4] and values [3,4,5] and capacity W=5.", "answer_outline": "Build 2D DP table → dp[i][w] = max(dp[i-1][w], val[i]+dp[i-1][w-wt[i]]) → Fill table → Answer = dp[3][5] = 7"}], "ten_mark": [{"q": "Find the Longest Common Subsequence of 'ABCBDAB' and 'BDCABA' using dynamic programming with full table.", "answer_outline": "Build (m+1)×(n+1) table → Fill using recurrence → Backtrack to find LCS → LCS = 'BDAB' length 4 → Time O(mn) Space O(mn)"}]}}
            ]
        elif is_physics:
            units = [
                {"unit_no": 1, "unit_title": "Wave Optics", "key_topics": ["Interference", "Diffraction", "Polarization", "LASER"], "must_know_formulas": ["Path diff for bright: nλ", "Single slit: a sinθ = nλ", "Brewster's law: tan θ_B = n"], "important_questions": {"mcq": [{"q": "In Young's double-slit experiment, if slit separation is halved, fringe width:", "options": ["A) Halves", "B) Doubles", "C) Remains same", "D) Quadruples"], "answer": "B", "explanation": "Fringe width β = λD/d → if d halved, β doubles"}], "five_mark": [{"q": "Explain the conditions for constructive and destructive interference in thin films.", "answer_outline": "Thin film reflection → Phase change at denser medium → Path diff = 2μt cosθ → Constructive: 2μt = (2n+1)λ/2 → Destructive: 2μt = nλ"}], "ten_mark": [{"q": "Derive the expression for fringe width in Young's Double Slit Experiment and discuss conditions for interference.", "answer_outline": "Setup diagram → Path difference derivation → Condition for maxima/minima → Fringe width β=λD/d → Factors affecting → Applications"}]}},
                {"unit_no": 2, "unit_title": "Quantum Mechanics", "key_topics": ["de Broglie Hypothesis", "Heisenberg Uncertainty", "Schrödinger Equation", "Wave Function"], "must_know_formulas": ["de Broglie: λ = h/mv", "Uncertainty: Δx·Δp ≥ ℏ/2", "Energy: E = hν = ℏω"], "important_questions": {"mcq": [{"q": "de Broglie wavelength of a particle moving with velocity v is:", "options": ["A) h/mv", "B) mv/h", "C) hv/m", "D) m/hv"], "answer": "A", "explanation": "λ = h/p = h/mv (de Broglie relation)"}], "five_mark": [{"q": "State and explain Heisenberg's Uncertainty Principle with two examples.", "answer_outline": "Statement → Δx·Δp ≥ ℏ/2 → Example 1: electron in atom → Example 2: why electrons can't exist in nucleus → Physical interpretation"}], "ten_mark": [{"q": "Derive the time-independent Schrödinger equation for a particle in a box and find the energy eigenvalues.", "answer_outline": "Potential well V=0 inside → Schrödinger eq → Solution ψ = A sin(nπx/L) → Boundary conditions → E_n = n²h²/8mL² → Normalization → Energy levels diagram"}]}},
                {"unit_no": 3, "unit_title": "Electromagnetic Theory", "key_topics": ["Maxwell's Equations", "Electromagnetic Waves", "Poynting Vector", "Skin Depth"], "must_know_formulas": ["∇·E = ρ/ε₀", "∇·B = 0", "∇×E = -∂B/∂t", "∇×B = μ₀J + μ₀ε₀∂E/∂t"], "important_questions": {"mcq": [{"q": "Which Maxwell equation represents Faraday's Law?", "options": ["A) ∇·E = ρ/ε₀", "B) ∇·B = 0", "C) ∇×E = -∂B/∂t", "D) ∇×B = μ₀J"], "answer": "C", "explanation": "∇×E = -∂B/∂t is the differential form of Faraday's Law"}], "five_mark": [{"q": "Define the Poynting vector and explain its physical significance.", "answer_outline": "S = (1/μ₀)(E×B) → Direction of energy flow → Magnitude = power per unit area → Application in wave propagation → SI unit W/m²"}], "ten_mark": [{"q": "Derive the wave equation for electromagnetic waves from Maxwell's equations in free space.", "answer_outline": "Start from curl equations → Take curl of curl E → Use vector identity → Substitute → ∇²E = μ₀ε₀∂²E/∂t² → Compare with wave eq → c = 1/√(μ₀ε₀)"}]}},
                {"unit_no": 4, "unit_title": "Band Theory & Semiconductors", "key_topics": ["Energy Bands", "Fermi Level", "p-n Junction", "Hall Effect"], "must_know_formulas": ["Hall voltage: V_H = IB/net", "Conductivity: σ = ne²τ/m", "Fermi-Dirac: f(E) = 1/(1+e^((E-EF)/kT))"], "important_questions": {"mcq": [{"q": "In intrinsic semiconductor at absolute zero temperature:", "options": ["A) Many free electrons", "B) No free electrons", "C) Only holes", "D) Equal electrons and holes"], "answer": "B", "explanation": "At T=0K, valence band is completely filled, conduction band is empty → No free carriers"}], "five_mark": [{"q": "Explain the formation of depletion region in a p-n junction.", "answer_outline": "Diffusion of carriers → Recombination at junction → Space charge region forms → Built-in electric field → Equilibrium → Width of depletion region"}], "ten_mark": [{"q": "Explain the Hall Effect and derive an expression for Hall coefficient. How is it used to determine carrier type?", "answer_outline": "Setup diagram → Lorentz force on carriers → Charge accumulation → Hall field → Equilibrium → R_H = 1/ne (n-type) or -1/pe (p-type) → Carrier type determination"}]}},
                {"unit_no": 5, "unit_title": "Superconductivity & Lasers", "key_topics": ["Meissner Effect", "BCS Theory", "Stimulated Emission", "Einstein Coefficients"], "must_know_formulas": ["A21/B21 = 8πhν³/c³", "Population inversion condition", "Tc = critical temperature"], "important_questions": {"mcq": [{"q": "Meissner effect in superconductors means:", "options": ["A) High electrical resistance", "B) Zero resistance below Tc", "C) Perfect diamagnetism — expulsion of magnetic field", "D) Strong magnetism"], "answer": "C", "explanation": "Superconductors expel magnetic flux (B=0 inside) → perfect diamagnetism (Meissner effect)"}], "five_mark": [{"q": "What is population inversion and why is it essential for LASER action?", "answer_outline": "Normal: more atoms in lower state → Pumping → More atoms in excited state → Population inversion → Stimulated emission > absorption → Coherent light amplification"}], "ten_mark": [{"q": "Explain construction and working of He-Ne LASER with energy level diagram.", "answer_outline": "Active medium He-Ne gas → Pumping by electrical discharge → He excitation → Collision excites Ne to F₃ level → Transition → 632.8nm red light → 4-level system → Output characteristics"}]}},
                {"unit_no": 6, "unit_title": "Fiber Optics & Applications", "key_topics": ["Total Internal Reflection", "Numerical Aperture", "Acceptance Angle", "Single vs Multimode Fiber"], "must_know_formulas": ["NA = √(n₁²-n₂²)", "Acceptance angle: θ = sin⁻¹(NA)", "TIR condition: θ > θ_c = sin⁻¹(n₂/n₁)"], "important_questions": {"mcq": [{"q": "Numerical Aperture of an optical fiber depends on:", "options": ["A) Only core refractive index", "B) Only cladding refractive index", "C) Both core and cladding refractive indices", "D) Fiber length"], "answer": "C", "explanation": "NA = √(n₁²-n₂²) depends on both n₁ (core) and n₂ (cladding)"}], "five_mark": [{"q": "Derive the expression for acceptance angle of an optical fiber.", "answer_outline": "TIR at core-cladding interface → Snell's law at input face → Relate to critical angle → sin θ_acc = NA = √(n₁²-n₂²) → Acceptance cone"}], "ten_mark": [{"q": "Explain the principle, structure and working of an optical fiber. Compare single-mode and multimode fibers.", "answer_outline": "TIR principle → Structure: core + cladding + buffer → Ray propagation → Meridional vs skew rays → Single mode: small core, one propagation mode, long-haul → Multimode: large core, dispersion → Comparison table → Applications"}]}}
            ]
        else:
            # Generic engineering subject fallback
            units = [
                {"unit_no": i+1, "unit_title": f"Unit {i+1}: Core Module {i+1}", "key_topics": [f"Fundamental Concept {j+1}" for j in range(4)], "must_know_formulas": [f"Key formula/theorem {i+1}"], "important_questions": {"mcq": [{"q": f"A key MCQ from Unit {i+1} of {subject_name}?", "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"], "answer": "A", "explanation": "Correct because it matches the fundamental definition"}], "five_mark": [{"q": f"Explain the core concept of Unit {i+1} in {subject_name} with an example.", "answer_outline": "Definition → Theory → Example → Diagram → Application"}], "ten_mark": [{"q": f"Describe the comprehensive application of Unit {i+1} concepts in real-world engineering scenarios.", "answer_outline": "Introduction → Theory → Derivation → Example → Diagram → Applications → Conclusion"}]}}
                for i in range(6)
            ]

        return {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "target_goal": f"Achieve 9+ CGPA (Grade O / A+) in LPU {subject_name} Examinations",
            "ai_generated": False,
            "exam_strategy": {
                "ca_tip": "Attend all classes, submit assignments on time, and score 8+/10 in each CA by preparing unit 1-3 thoroughly",
                "mte_tip": "Focus on Part A (MCQs) — attempt all 30, avoid random guessing. Target 22+/30 for Grade A+",
                "ete_tip": "Section C 10-mark questions are worth the most — prepare 3 complete answers for each unit",
                "negative_marking_tip": "Only attempt MCQs you are 70%+ sure about. Skip if unsure to avoid -0.25 penalty"
            },
            "units": units,
            "study_tracks": [
                {
                    "track_name": f"⚡ 7-Day 9+ CGPA Sprint for {subject_name}",
                    "days": [
                        {"day": "Day 1", "focus": f"Unit 1: {units[0]['unit_title']}", "hours": 3, "tasks": [f"Read Unit 1 notes for {subject_code}", f"Solve 20 MCQs on {units[0]['key_topics'][0]}", "Memorize key formulas from Unit 1"], "checkpoint": "Score >= 80% on Unit 1 practice quiz"},
                        {"day": "Day 2", "focus": f"Unit 2: {units[1]['unit_title']}", "hours": 3.5, "tasks": [f"Study {units[1]['key_topics'][0]} and {units[1]['key_topics'][1]}", "Practice 5-mark questions from unit 2", "Make formula cheat sheet"], "checkpoint": "Able to solve unit 2 questions without notes"},
                        {"day": "Day 3", "focus": f"Unit 3 + MTE Mock Simulation", "hours": 4, "tasks": ["Complete Unit 3 core concepts", "Sit for full 30-mark MTE simulation in timed mode", "Analyze wrong answers and negative marking deductions"], "checkpoint": "Score >= 24/30 on MTE Simulation"},
                        {"day": "Day 4", "focus": f"Unit 4: {units[3]['unit_title']}", "hours": 3.5, "tasks": [f"Master {units[3]['key_topics'][0]}", f"Practice {units[3]['important_questions']['ten_mark'][0]['q'][:50]}...", "Solve 20 Unit 4 MCQs"], "checkpoint": "Complete unit 4 model answer in 18 minutes"},
                        {"day": "Day 5", "focus": f"Units 5 & 6 + PYQ Review", "hours": 4, "tasks": [f"Study {units[4]['unit_title']} and {units[5]['unit_title']}", "Review 3 years of PYQ papers for repeat questions", "Prepare 10-mark answers for most likely questions"], "checkpoint": "All 6 units revised at least once"},
                        {"day": "Day 6", "focus": "Full ETE 100-Mark Timed Simulation", "hours": 4.5, "tasks": ["Sit for full 3-hour ETE mock in Exam Simulator", "Review color-coded palette (Green=answered, Red=wrong, Purple=skipped)", "Export and review printable LPU exam paper PDF"], "checkpoint": "Overall Grade >= A+ (85%+) on automated scorecard"},
                        {"day": "Day 7", "focus": "Final Revision, High-Yield Review & Mental Rest", "hours": 2, "tasks": ["Read only Short Notes and flashcard cheat sheets", "Review PYQ repeat-probability tags (★★★ = very likely)", "Pack Hall Ticket, LPU Student ID, pens, water bottle"], "checkpoint": "Ready to achieve Grade O in the examination hall!"}
                    ]
                }
            ]
        }

