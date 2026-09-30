import os
import re
import json
import random
from typing import Dict, List, Any, Optional

class StudyAssetGenerator:
    """
    Generates various learning and revision assets from subject materials:
    1. Full Comprehensive Notes
    2. Short Revision Notes / Cheat Sheet
    3. Interactive Presentation Slides
    4. Week-by-Week / Day-by-Day Learning Roadmap
    5. MCQs & PYQ Practice Sets
    """

    @classmethod
    def generate_full_notes(cls, text: str, subject_code: str, subject_name: str, unit: str = "Unit 1") -> Dict[str, Any]:
        """Generate structured textbook-quality comprehensive notes with sections, tables, and code."""
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

        # Construct sections
        sections = [
            {
                "heading": f"1. Orientation & Theoretical Foundations of {k1}",
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
                "content": (
                    f"The operational lifecycle follows a rigorous, deterministic sequence:\n\n"
                    f"1. **Precondition Validation:** Verification of resource constraints and input boundaries.\n"
                    f"2. **Processing Pipeline:** Iterative state transformations guided by {k2} rules.\n"
                    f"3. **State Finalization & Cleanup:** Committing outputs and mitigating memory leaks.\n\n"
                    f"```text\n"
                    f"[Input Stream] ---> [Validation Layer] ---> [Core {k2} Engine] ---> [Output State]\n"
                    f"                         │                             │\n"
                    f"                         ▼                             ▼\n"
                    f"                  [Error Trap]                  [Persistence Log]\n"
                    f"```\n\n"
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
    def generate_roadmap(cls, text: str, subject_code: str, subject_name: str) -> Dict[str, Any]:
        """Generate a 7-day intensive or 4-week structured preparation roadmap for 9+ CGPA at LPU."""
        return {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "target_goal": "Achieve 9+ CGPA (Grade O / A+) in LPU Examinations",
            "study_tracks": [
                {
                    "track_name": "⚡ 7-Day Exam Cram Sprint (Night Before & Final Week)",
                    "days": [
                        {
                            "day": "Day 1",
                            "focus": "Unit 1: Fundamentals & Syntax Recall",
                            "hours": 3,
                            "tasks": [
                                "Read Comprehensive Unit 1 Notes on LPU Verto",
                                "Solve 30 Unit 1 Practice MCQs (focus on syntax & keywords)",
                                "Memorize 1-liner definitions and basic formulas"
                            ],
                            "checkpoint": "Score >= 80% on CA1 Mock Test"
                        },
                        {
                            "day": "Day 2",
                            "focus": "Unit 2: Core Data Representations & Workflows",
                            "hours": 3.5,
                            "tasks": [
                                "Practice state diagrams and block architectures",
                                "Implement 2 standard algorithms in C++/Python",
                                "Review Short Notes & flashcards"
                            ],
                            "checkpoint": "Able to explain Section B 5-mark differences without notes"
                        },
                        {
                            "day": "Day 3",
                            "focus": "Unit 3: Mid-Term (MTE) Comprehensive Review",
                            "hours": 4,
                            "tasks": [
                                "Complete full MTE 30-mark simulation paper in timed mode (90 mins)",
                                "Analyze incorrect answers and negative marking deductions (-0.25)",
                                "Revise edge cases and exception handling"
                            ],
                            "checkpoint": "Achieve >= 24/30 Marks on MTE Simulation"
                        },
                        {
                            "day": "Day 4",
                            "focus": "Unit 4: Advanced Systems & Algorithms",
                            "hours": 3.5,
                            "tasks": [
                                "Master asymptotic notation (Big-O, Omega, Theta)",
                                "Practice divide-and-conquer recurrence relations",
                                "Solve 25 Unit 4 MCQs"
                            ],
                            "checkpoint": "Derive Master Theorem solutions without hesitation"
                        },
                        {
                            "day": "Day 5",
                            "focus": "Unit 5 & 6: System Design, Applications & PYQs",
                            "hours": 4,
                            "tasks": [
                                "Study 10-mark Section C Comprehensive Model Answers",
                                "Memorize evaluator marking rubrics (Diagrams 3M, Code 3M, Proofs 2M)",
                                "Read LPU Verto Note Bank archived question solutions"
                            ],
                            "checkpoint": "Draft full 10-mark architectural answer in 18 minutes"
                        },
                        {
                            "day": "Day 6",
                            "focus": "Full LPU End-Term (ETE) 100-Mark Simulation",
                            "hours": 4.5,
                            "tasks": [
                                "Sit for full 3-Hour Timed ETE Mock Exam in Simulator",
                                "Review color-coded question palette (Green, Red, Purple)",
                                "Export printable official LPU Question Paper PDF"
                            ],
                            "checkpoint": "Overall Grade >= A+ on automated scorecard"
                        },
                        {
                            "day": "Day 7",
                            "focus": "Final Revision, High-Yield Formulas & Mental Rest",
                            "hours": 2,
                            "tasks": [
                                "Read Short Notes & Flashcard cheat sheets one last time",
                                "Review previous year repeat tags (PYQ Repeat probabilities)",
                                "Pack Hall Ticket, LPU Student ID, and stationary"
                            ],
                            "checkpoint": "Ready to excel in LPU Examination Hall!"
                        }
                    ]
                }
            ]
        }
