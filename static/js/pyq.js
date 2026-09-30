/**
 * PYQ (Previous Year Questions) Controller for AcadAssist
 * Manages LPU Past Exam Papers (2021-2024) ETE & MTE
 * Integrated with Exam Simulator, Multi-Course Catalog & Print Engine
 */

const PYQManager = {
  currentSubject: "MTH166",
  currentPaperId: "MTH166-2024-ETE",
  availableSubjects: [],
  allCoursesList: [],
  papersList: [],
  currentPaper: null,

  async init() {
    await this.loadSubjects();
    await this.loadAllCoursesDropdown();
    this.setupListeners();
  },

  setupListeners() {
    const searchInput = document.getElementById("pyq-search-input");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.trim();
        if (q.length >= 3) {
          this.searchQuestions(q);
        } else if (q.length === 0) {
          const resBox = document.getElementById("pyq-search-results");
          if (resBox) resBox.classList.add("hidden");
        }
      });
    }
  },

  async loadSubjects() {
    try {
      const res = await fetch("/api/pyq/subjects");
      this.availableSubjects = await res.json();
      this.renderSubjectSelector();
      if (this.availableSubjects.length > 0) {
        const initial = this.availableSubjects[0].code;
        await this.selectSubject(initial);
      }
    } catch (err) {
      console.error("Error loading PYQ subjects:", err);
    }
  },

  async loadAllCoursesDropdown() {
    const dropdown = document.getElementById("pyq-subject-dropdown");
    if (!dropdown) return;

    try {
      let subjects = window.allAvailableSubjects;
      if (!subjects || !subjects.length) {
        const res = await fetch("/api/all-subjects");
        subjects = await res.json();
      }
      this.allCoursesList = subjects || [];
      
      const currentVal = dropdown.value;
      dropdown.innerHTML = `
        <option value="">Select any LPU Course (266+ available)...</option>
        ${this.allCoursesList.map(s => `
          <option value="${s.code}">${s.code} — ${s.name || s.title || 'Course Material'}</option>
        `).join("")}
      `;
      if (currentVal) dropdown.value = currentVal;
    } catch (e) {
      console.warn("Could not load full courses dropdown for PYQ:", e);
    }
  },

  renderSubjectSelector() {
    const container = document.getElementById("pyq-subject-pills");
    if (!container) return;

    container.innerHTML = this.availableSubjects.map(s => `
      <button onclick="PYQManager.selectSubject('${s.code}')" id="pyq-pill-${s.code}" class="pyq-sub-pill px-3 py-1.5 rounded-xl text-xs font-bold transition-all border whitespace-nowrap ${s.code === this.currentSubject ? 'bg-pink-500 text-white border-pink-500 shadow-sm' : 'bg-gray-50 dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-200 dark:border-slate-700 hover:border-pink-400'}">
        <span>${s.code}</span>
        <span class="ml-1 text-[10px] opacity-80">(${s.paper_count} papers)</span>
      </button>
    `).join("");
  },

  async selectSubject(code) {
    if (!code) return;
    this.currentSubject = code.toUpperCase();

    // Synchronize dropdown
    const dropdown = document.getElementById("pyq-subject-dropdown");
    if (dropdown) dropdown.value = this.currentSubject;
    
    // Update pills active styling or add pill dynamically if not present
    document.querySelectorAll(".pyq-sub-pill").forEach(p => {
      p.classList.remove("bg-pink-500", "text-white", "border-pink-500", "shadow-sm");
      p.classList.add("bg-gray-50", "dark:bg-slate-800", "text-gray-700", "dark:text-slate-300", "border-gray-200", "dark:border-slate-700");
    });

    let activePill = document.getElementById(`pyq-pill-${this.currentSubject}`);
    if (!activePill) {
      const container = document.getElementById("pyq-subject-pills");
      if (container) {
        const btn = document.createElement("button");
        btn.id = `pyq-pill-${this.currentSubject}`;
        btn.onclick = () => PYQManager.selectSubject(this.currentSubject);
        btn.className = "pyq-sub-pill px-3 py-1.5 rounded-xl text-xs font-bold transition-all border whitespace-nowrap bg-pink-500 text-white border-pink-500 shadow-sm";
        btn.innerHTML = `<span>${this.currentSubject}</span><span class="ml-1 text-[10px] opacity-80">(Papers)</span>`;
        container.prepend(btn);
        activePill = btn;
      }
    } else {
      activePill.classList.remove("bg-gray-50", "dark:bg-slate-800", "text-gray-700", "dark:text-slate-300", "border-gray-200", "dark:border-slate-700");
      activePill.classList.add("bg-pink-500", "text-white", "border-pink-500", "shadow-sm");
    }

    try {
      const res = await fetch(`/api/pyq/papers?subject=${this.currentSubject}`);
      this.papersList = await res.json();
      this.renderPapersList();

      if (this.papersList.length > 0) {
        await this.loadPaper(this.papersList[0].paper_id);
      } else {
        const viewer = document.getElementById("pyq-paper-viewer");
        if (viewer) {
          viewer.innerHTML = `
            <div class="p-12 text-center text-gray-400 bg-white dark:bg-slate-900 rounded-3xl border border-gray-200 dark:border-slate-800">
              <p class="font-bold text-sm">No archive papers found for ${this.currentSubject}.</p>
              <button onclick="loadSubjectIntoExamGenerator('${this.currentSubject}')" class="mt-4 px-4 py-2 rounded-xl bg-orange-500 text-white font-bold text-xs hover:bg-orange-600 transition-all">
                📝 Synthesize Exam Paper with AI
              </button>
            </div>
          `;
        }
      }
    } catch (err) {
      console.error(`Error loading papers for ${code}:`, err);
    }
  },

  renderPapersList() {
    const listContainer = document.getElementById("pyq-papers-list");
    if (!listContainer) return;

    if (!this.papersList.length) {
      listContainer.innerHTML = `
        <div class="p-6 text-center text-gray-400 bg-white dark:bg-slate-900 rounded-2xl border border-gray-200 dark:border-slate-800">
          No papers for this course yet.
        </div>
      `;
      return;
    }

    listContainer.innerHTML = this.papersList.map(p => `
      <div onclick="PYQManager.loadPaper('${p.paper_id}')" class="cursor-pointer p-4 rounded-2xl border transition-all ${p.paper_id === this.currentPaperId ? 'bg-pink-50 dark:bg-pink-950/20 border-pink-500 shadow-sm' : 'bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-800 hover:border-pink-300'}">
        <div class="flex items-center justify-between gap-2">
          <span class="text-xs font-black uppercase text-pink-600 dark:text-pink-400">${p.year} • ${p.term}</span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-300">${p.max_marks} Marks</span>
        </div>
        <h4 class="font-bold text-sm text-gray-900 dark:text-white mt-1 leading-snug">${p.subject_code} — ${p.subject_name}</h4>
        <div class="flex items-center gap-3 text-[11px] text-gray-500 dark:text-slate-400 mt-2">
          <span>⏱️ ${p.duration_minutes} Mins</span>
          <span>📝 ${p.total_questions} Questions</span>
          <span>🏛️ ${p.paper_code || 'Main'}</span>
        </div>
      </div>
    `).join("");
  },

  async loadPaper(paperId) {
    this.currentPaperId = paperId;
    const viewer = document.getElementById("pyq-paper-viewer");
    if (!viewer) return;

    viewer.innerHTML = `
      <div class="p-12 text-center text-gray-400 bg-white dark:bg-slate-900 rounded-3xl border border-gray-200 dark:border-slate-800 space-y-3">
        <svg class="animate-spin h-8 w-8 text-pink-500 mx-auto" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <span class="text-xs font-bold text-gray-600 dark:text-slate-300 block">Loading authentic examination question paper & marking solutions...</span>
      </div>
    `;

    try {
      const res = await fetch(`/api/pyq/paper/${paperId}`);
      if (!res.ok) throw new Error("Paper not found");
      this.currentPaper = await res.json();
      this.renderFullPaper(this.currentPaper);
      this.renderPapersList(); // Re-render to highlight active paper
    } catch (err) {
      viewer.innerHTML = `<div class="p-8 text-center text-red-500 bg-white dark:bg-slate-900 rounded-2xl border border-red-200">Failed to load paper: ${err.message}</div>`;
    }
  },

  renderFullPaper(p) {
    const viewer = document.getElementById("pyq-paper-viewer");
    if (!viewer) return;

    const partA = p.part_a || [];
    const partB = p.part_b || [];
    const partC = p.part_c || [];

    viewer.innerHTML = `
      <!-- Paper Sheet Container (Authentic LPU Exam Layout) -->
      <div id="printable-pyq-paper" class="bg-white dark:bg-slate-900 rounded-3xl border border-gray-200 dark:border-slate-800 p-6 sm:p-10 shadow-lg space-y-8 animate-fade-in">
        
        <!-- Header Section -->
        <div class="border-b-2 border-dashed border-gray-300 dark:border-slate-700 pb-6 text-center space-y-2">
          <div class="flex items-center justify-between text-[11px] font-bold text-gray-500 dark:text-slate-400">
            <span>Roll No: ____________________</span>
            <span>Paper Code: <strong class="text-pink-500 font-mono">${p.paper_code || '11823/A'}</strong></span>
          </div>

          <h2 class="text-xl sm:text-2xl font-black uppercase tracking-tight text-gray-900 dark:text-white pt-2">
            LOVELY PROFESSIONAL UNIVERSITY
          </h2>
          <p class="text-xs font-bold text-gray-600 dark:text-slate-300 uppercase tracking-widest">
            ${p.term} — ${p.year}
          </p>
          <div class="inline-block px-4 py-1.5 rounded-full bg-pink-50 dark:bg-pink-950/40 border border-pink-200 dark:border-pink-800 text-pink-600 dark:text-pink-400 font-black text-sm">
            ${p.subject_code} — ${p.subject_name.toUpperCase()}
          </div>

          <div class="flex items-center justify-center gap-6 pt-3 text-xs font-bold text-gray-700 dark:text-slate-300">
            <span>Time Allowed: <strong>${p.duration_minutes} Minutes</strong></span>
            <span>•</span>
            <span>Maximum Marks: <strong>${p.max_marks} Marks</strong></span>
          </div>

          <div class="mt-4 p-3 rounded-xl bg-gray-50 dark:bg-slate-800/60 text-left text-xs text-gray-600 dark:text-slate-400 border border-gray-200 dark:border-slate-700">
            <strong>Instructions:</strong> ${p.instructions || 'Attempt all questions according to internal section choices. Negative marking is applicable to Part A MCQs.'}
          </div>

          <!-- Action bar -->
          <div class="flex flex-wrap items-center justify-between gap-2 pt-3 no-print border-t border-gray-100 dark:border-slate-800 mt-4">
            <div class="flex items-center gap-2">
              <button onclick="PYQManager.startMockFromPYQ('${p.paper_id}')" class="px-4 py-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-black text-xs shadow-md shadow-orange-500/20 transition-all flex items-center gap-1.5">
                <span>⚡ Test in Exam Simulator</span>
              </button>
              <button onclick="loadSubjectIntoExamGenerator('${p.subject_code}')" class="px-3.5 py-2 rounded-xl bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-xs font-bold text-gray-700 dark:text-slate-200 transition-colors">
                <span>📝 Generate Variant</span>
              </button>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="window.print()" class="px-3.5 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-xs font-bold text-gray-700 dark:text-slate-200 flex items-center gap-1.5 transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                <span>🖨️ Print Paper</span>
              </button>
              <button onclick="PYQManager.toggleAllSolutions()" id="btn-toggle-all-solutions" class="px-3.5 py-2 rounded-xl bg-pink-50 hover:bg-pink-100 dark:bg-pink-950/40 text-xs font-bold text-pink-600 dark:text-pink-400 border border-pink-200 dark:border-pink-800 transition-colors">
                👁️ Reveal All Model Answers
              </button>
            </div>
          </div>
        </div>

        <!-- PART A: MCQs & Short Questions -->
        ${partA.length > 0 ? `
          <div class="space-y-4">
            <div class="flex items-center justify-between border-b border-gray-200 dark:border-slate-800 pb-2">
              <h3 class="font-black text-base uppercase text-gray-900 dark:text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span>
                PART A — MCQs & Short Answer Questions
              </h3>
              <span class="text-xs font-bold text-gray-500 dark:text-slate-400">Compulsory (${partA.reduce((sum, q) => sum + (q.marks || 2), 0)} Marks)</span>
            </div>

            <div class="space-y-4">
              ${partA.map((q, idx) => `
                <div class="p-4 rounded-2xl bg-gray-50 dark:bg-slate-800/40 border border-gray-100 dark:border-slate-800 space-y-3">
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-start gap-2">
                      <span class="font-mono font-black text-sm text-pink-600 dark:text-pink-400">Q${q.q_no || idx + 1}.</span>
                      <p class="font-bold text-sm text-gray-900 dark:text-white leading-relaxed">${q.question}</p>
                    </div>
                    <span class="shrink-0 text-xs font-bold px-2 py-0.5 rounded bg-gray-200 dark:bg-slate-700 text-gray-700 dark:text-slate-300">[${q.marks || 2} Marks]</span>
                  </div>

                  ${q.options && q.options.length > 0 ? `
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 pl-6">
                      ${q.options.map((opt, optIdx) => `
                        <div class="p-2.5 rounded-xl border border-gray-200 dark:border-slate-700 text-xs font-medium text-gray-800 dark:text-slate-200 flex items-center gap-2">
                          <span class="w-5 h-5 rounded-full bg-gray-100 dark:bg-slate-800 flex items-center justify-center font-bold text-[10px] text-gray-500">${String.fromCharCode(65 + optIdx)}</span>
                          <span>${opt}</span>
                        </div>
                      `).join("")}
                    </div>
                  ` : ''}

                  <!-- Solution toggle -->
                  <div class="pt-2 pl-6">
                    <button onclick="PYQManager.toggleSolution('sol-part-a-${idx}')" class="text-xs font-bold text-pink-600 dark:text-pink-400 hover:underline flex items-center gap-1">
                      <span>💡 View Solution & Explanation</span>
                    </button>
                    <div id="sol-part-a-${idx}" class="pyq-sol-box hidden mt-2 p-3 rounded-xl bg-pink-50/60 dark:bg-pink-950/20 border border-pink-200 dark:border-pink-800 text-xs text-gray-800 dark:text-slate-200 space-y-1">
                      ${q.correct_option ? `<div><strong>Correct Answer:</strong> <span class="text-pink-600 dark:text-pink-400 font-bold">${q.correct_option}</span></div>` : ''}
                      <div><strong>Explanation:</strong> ${q.solution}</div>
                    </div>
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ''}

        <!-- PART B: 5/10-Mark Analytical Questions -->
        ${partB.length > 0 ? `
          <div class="space-y-4 pt-4">
            <div class="flex items-center justify-between border-b border-gray-200 dark:border-slate-800 pb-2">
              <h3 class="font-black text-base uppercase text-gray-900 dark:text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-orange-500"></span>
                PART B — Analytical & Problem Solving Questions
              </h3>
              <span class="text-xs font-bold text-gray-500 dark:text-slate-400">Attempt Any ${partB.length > 2 ? partB.length - 1 : partB.length} (${partB.reduce((sum, q) => sum + (q.marks || 10), 0)} Marks)</span>
            </div>

            <div class="space-y-4">
              ${partB.map((q, idx) => `
                <div class="p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/40 border border-gray-100 dark:border-slate-800 space-y-3">
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-start gap-2">
                      <span class="font-mono font-black text-sm text-orange-600 dark:text-orange-400">Q${q.q_no || idx + partA.length + 1}.</span>
                      <div>
                        <span class="text-[10px] font-bold uppercase tracking-wider text-orange-600 dark:text-orange-400 block mb-1">${q.unit || 'Core Unit'}</span>
                        <p class="font-bold text-sm text-gray-900 dark:text-white leading-relaxed">${q.question}</p>
                      </div>
                    </div>
                    <span class="shrink-0 text-xs font-bold px-2.5 py-1 rounded bg-orange-100 dark:bg-orange-950/60 text-orange-700 dark:text-orange-300">[${q.marks || 10} Marks]</span>
                  </div>

                  <!-- Solution toggle -->
                  <div class="pt-2 pl-6">
                    <button onclick="PYQManager.toggleSolution('sol-part-b-${idx}')" class="text-xs font-bold text-orange-600 dark:text-orange-400 hover:underline flex items-center gap-1">
                      <span>📖 View Step-by-Step Model Answer & Rubric</span>
                    </button>
                    <div id="sol-part-b-${idx}" class="pyq-sol-box hidden mt-3 p-4 rounded-xl bg-orange-50/60 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-800 text-xs text-gray-800 dark:text-slate-200 space-y-2">
                      <div class="font-semibold whitespace-pre-line">${q.solution}</div>
                      ${q.rubric ? `
                        <div class="pt-2 border-t border-orange-200 dark:border-orange-800/50 text-[11px] text-orange-800 dark:text-orange-300">
                          <strong>LPU Marking Scheme:</strong> ${q.rubric}
                        </div>
                      ` : ''}
                    </div>
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ''}

        <!-- PART C: 10/20-Mark Comprehensive & Derivations -->
        ${partC.length > 0 ? `
          <div class="space-y-4 pt-4">
            <div class="flex items-center justify-between border-b border-gray-200 dark:border-slate-800 pb-2">
              <h3 class="font-black text-base uppercase text-gray-900 dark:text-white flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                PART C — Comprehensive Case Study & Long Derivations
              </h3>
              <span class="text-xs font-bold text-gray-500 dark:text-slate-400">Attempt Any ${partC.length > 1 ? partC.length - 1 : 1} (${partC.reduce((sum, q) => sum + (q.marks || 20), 0)} Marks)</span>
            </div>

            <div class="space-y-4">
              ${partC.map((q, idx) => `
                <div class="p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/40 border border-gray-100 dark:border-slate-800 space-y-3">
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-start gap-2">
                      <span class="font-mono font-black text-sm text-purple-600 dark:text-purple-400">Q${q.q_no || idx + partA.length + partB.length + 1}.</span>
                      <div>
                        <span class="text-[10px] font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400 block mb-1">${q.unit || 'Core Specialization'}</span>
                        <p class="font-bold text-sm text-gray-900 dark:text-white leading-relaxed">${q.question}</p>
                      </div>
                    </div>
                    <span class="shrink-0 text-xs font-bold px-2.5 py-1 rounded bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300">[${q.marks || 20} Marks]</span>
                  </div>

                  <!-- Solution toggle -->
                  <div class="pt-2 pl-6">
                    <button onclick="PYQManager.toggleSolution('sol-part-c-${idx}')" class="text-xs font-bold text-purple-600 dark:text-purple-400 hover:underline flex items-center gap-1">
                      <span>🔬 View Full Mathematical Proof / Implementation</span>
                    </button>
                    <div id="sol-part-c-${idx}" class="pyq-sol-box hidden mt-3 p-4 rounded-xl bg-purple-50/60 dark:bg-purple-950/20 border border-purple-200 dark:border-purple-800 text-xs text-gray-800 dark:text-slate-200 space-y-2">
                      <div class="font-semibold whitespace-pre-line leading-relaxed">${q.solution}</div>
                      ${q.rubric ? `
                        <div class="pt-2 border-t border-purple-200 dark:border-purple-800/50 text-[11px] text-purple-800 dark:text-purple-300">
                          <strong>Step-by-step Evaluation Rubric:</strong> ${q.rubric}
                        </div>
                      ` : ''}
                    </div>
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ''}

        <!-- Footer / Watermark -->
        <div class="pt-6 border-t border-gray-200 dark:border-slate-800 flex items-center justify-between text-[11px] text-gray-400 dark:text-slate-500">
          <span>Source: ${p.source || 'LPU Past Examination Archive'}</span>
          <span>Curated for Lovely Professional University Students • AcadAssist</span>
        </div>

      </div>
    `;
  },

  startMockFromPYQ(paperId) {
    if (!this.currentPaper || this.currentPaper.paper_id !== paperId) return;
    const p = this.currentPaper;

    if (!window.ExamSimulator) {
      alert("Exam simulator module not ready. Please try again.");
      return;
    }

    const simPaper = {
      exam_title: `${p.subject_code} — ${p.term} (${p.year}) Real PYQ Paper`,
      subject_code: p.subject_code,
      subject_name: p.subject_name,
      duration_minutes: p.duration_minutes || 60,
      total_marks: p.max_marks || 100,
      negative_marking: -0.25,
      sections: {
        section_a: {
          title: "Section A: Objective & Multiple Choice Questions",
          instructions: "Attempt all questions. Correct MCQ awards marks; -0.25 negative marking applies.",
          questions: (p.part_a || []).map((q, idx) => ({
            id: `mcq_${idx + 1}`,
            question_number: idx + 1,
            question_text: q.question,
            options: (q.options && q.options.length) ? q.options : ["Optimal formulation", "Boundary convergence", "State transition", "Arbitrary state"],
            correct_option: q.correct_option ? (q.correct_option.length === 1 ? q.correct_option : "A") : "A",
            explanation: q.solution || "Refer to LPU marking rubric.",
            marks: q.marks || 2,
            negative_marks: 0.25,
            unit: "Unit 1",
            difficulty: "Medium"
          }))
        },
        section_b: {
          title: "Section B: Analytical & Conceptual Questions",
          instructions: "Attempt questions with clear steps and diagrams.",
          questions: (p.part_b || []).map((q, idx) => ({
            id: `short_${idx + 1}`,
            question_number: idx + 1,
            question_text: q.question,
            solution: q.solution,
            marking_rubric: q.rubric || "Step-by-step logic: 4M | Accuracy: 6M",
            marks: q.marks || 10,
            unit: q.unit || "Core"
          }))
        },
        section_c: {
          title: "Section C: Comprehensive / Analytical Questions",
          instructions: "Attempt long-form case studies and comprehensive proofs.",
          questions: (p.part_c || []).map((q, idx) => ({
            id: `long_${idx + 1}`,
            question_number: idx + 1,
            question_text: q.question,
            solution: q.solution,
            marking_rubric: q.rubric || "Full proof: 10M | Edge cases & trade-offs: 10M",
            marks: q.marks || 20,
            unit: q.unit || "Specialization"
          }))
        }
      }
    };

    window.ExamSimulator.init(simPaper);
    if (typeof switchTab === 'function') {
      switchTab('tab-simulator');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  toggleSolution(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
      el.classList.toggle("hidden");
    }
  },

  toggleAllSolutions() {
    const boxes = document.querySelectorAll(".pyq-sol-box");
    const anyHidden = Array.from(boxes).some(b => b.classList.contains("hidden"));
    boxes.forEach(b => {
      if (anyHidden) {
        b.classList.remove("hidden");
      } else {
        b.classList.add("hidden");
      }
    });
    const btn = document.getElementById("btn-toggle-all-solutions");
    if (btn) {
      btn.innerText = anyHidden ? "🙈 Hide All Model Answers" : "👁️ Reveal All Model Answers";
    }
  },

  async searchQuestions(query) {
    const resultsContainer = document.getElementById("pyq-search-results");
    if (!resultsContainer) return;

    try {
      const res = await fetch(`/api/pyq/search?q=${encodeURIComponent(query)}`);
      const hits = await res.json();

      resultsContainer.classList.remove("hidden");
      if (hits.length === 0) {
        resultsContainer.innerHTML = `<div class="p-4 text-xs text-gray-500">No questions found matching "${query}".</div>`;
        return;
      }

      resultsContainer.innerHTML = `
        <div class="p-3 bg-pink-50 dark:bg-pink-950/30 border-b border-pink-100 dark:border-pink-900/50 text-xs font-bold text-pink-700 dark:text-pink-300">
          Found ${hits.length} questions matching "${query}":
        </div>
        <div class="max-h-80 overflow-y-auto divide-y divide-gray-100 dark:divide-slate-800">
          ${hits.map(h => `
            <div class="p-3 text-xs hover:bg-gray-50 dark:hover:bg-slate-800/60 cursor-pointer" onclick="PYQManager.selectSubject('${h.subject_code}'); document.getElementById('pyq-search-results').classList.add('hidden')">
              <div class="flex items-center justify-between text-[10px] text-gray-400 font-bold mb-1">
                <span>${h.subject_code} • ${h.year} ${h.term}</span>
                <span class="text-pink-500 font-bold">${h.marks}M</span>
              </div>
              <p class="font-bold text-gray-800 dark:text-slate-200 line-clamp-2">${h.question}</p>
            </div>
          `).join("")}
        </div>
      `;
    } catch (err) {
      console.error("Search error:", err);
    }
  }
};

window.PYQManager = PYQManager;
document.addEventListener("DOMContentLoaded", () => {
  PYQManager.init();
});
