/**
 * LPU Verto AI Exam Prep - Interactive Exam Simulator & Practice Engine
 */

const ExamSimulator = {
  currentPaper: null,
  activeSection: 'section_a', // 'section_a', 'section_b', 'section_c'
  currentQuestionIndex: 0,
  userAnswers: {}, // { 'mcq_1': 'B' }
  questionStatus: {}, // { 'mcq_1': 'answered' | 'unanswered' | 'review' | 'unvisited' }
  timerInterval: null,
  secondsRemaining: 0,
  isPracticeMode: true, // practice mode reveals answers; test mode is timed simulation

  init(paperData) {
    this.currentPaper = paperData;
    this.activeSection = 'section_a';
    this.currentQuestionIndex = 0;
    this.userAnswers = {};
    this.questionStatus = {};

    // Initialize statuses for all questions
    const allMcqs = paperData.sections.section_a.questions || [];
    allMcqs.forEach((q, idx) => {
      this.questionStatus[q.id] = idx === 0 ? 'unanswered' : 'unvisited';
    });

    this.secondsRemaining = (paperData.duration_minutes || 60) * 60;
    this.renderSimulatorHeader();
    this.renderQuestionPalette();
    this.renderCurrentQuestion();
    this.renderSubjectiveSections();
    this.startTimer();
    this.setupControls();
  },

  renderSimulatorHeader() {
    const titleEl = document.getElementById('sim-exam-title');
    const courseCodeEl = document.getElementById('sim-course-code');
    const maxMarksEl = document.getElementById('sim-max-marks');
    const totalQsEl = document.getElementById('sim-total-qs');

    if (titleEl) titleEl.textContent = this.currentPaper.exam_title;
    if (courseCodeEl) courseCodeEl.textContent = `${this.currentPaper.subject_code} - ${this.currentPaper.subject_name}`;
    if (maxMarksEl) maxMarksEl.textContent = `${this.currentPaper.total_marks} Marks`;
    
    const mcqCt = this.currentPaper.sections.section_a.questions.length;
    const shortCt = this.currentPaper.sections.section_b.questions.length;
    const longCt = this.currentPaper.sections.section_c.questions.length;
    if (totalQsEl) totalQsEl.textContent = `${mcqCt} MCQs + ${shortCt} Short + ${longCt} Long`;
  },

  renderQuestionPalette() {
    const paletteContainer = document.getElementById('question-palette');
    if (!paletteContainer) return;

    paletteContainer.innerHTML = '';
    const mcqs = this.currentPaper.sections.section_a.questions || [];

    mcqs.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn palette-unvisited';
      btn.textContent = idx + 1;
      btn.setAttribute('data-q-idx', idx);

      const status = this.questionStatus[q.id] || 'unvisited';
      if (status === 'answered') btn.classList.replace('palette-unvisited', 'palette-answered');
      else if (status === 'unanswered') btn.classList.replace('palette-unvisited', 'palette-unanswered');
      else if (status === 'review') btn.classList.replace('palette-unvisited', 'palette-review');

      if (idx === this.currentQuestionIndex) {
        btn.classList.add('ring-2', 'ring-orange-500', 'scale-105');
      }

      btn.addEventListener('click', () => {
        this.goToQuestion(idx);
      });

      paletteContainer.appendChild(btn);
    });

    this.updatePaletteCounters();
  },

  updatePaletteCounters() {
    let answered = 0, unanswered = 0, review = 0, unvisited = 0;
    const mcqs = this.currentPaper.sections.section_a.questions || [];

    mcqs.forEach(q => {
      const s = this.questionStatus[q.id] || 'unvisited';
      if (s === 'answered') answered++;
      else if (s === 'unanswered') unanswered++;
      else if (s === 'review') review++;
      else unvisited++;
    });

    const elA = document.getElementById('count-answered');
    const elU = document.getElementById('count-unanswered');
    const elR = document.getElementById('count-review');
    const elV = document.getElementById('count-unvisited');

    if (elA) elA.textContent = answered;
    if (elU) elU.textContent = unanswered;
    if (elR) elR.textContent = review;
    if (elV) elV.textContent = unvisited;
  },

  hasPaperAccess() {
    if (!this.currentPaper) return false;
    const code = this.currentPaper.subject_code;
    const pm = window.PaywallManager;
    if (!pm) return false;
    return pm.hasMockAccess(code) || pm.hasSubjectAccess(code);
  },

  renderCurrentQuestion() {
    const container = document.getElementById('mcq-question-area');
    if (!container) return;

    const mcqs = this.currentPaper.sections.section_a.questions || [];
    if (this.currentQuestionIndex >= mcqs.length) return;

    const q = mcqs[this.currentQuestionIndex];
    const isLocked = q.is_locked && !this.hasPaperAccess();
    const selectedOpt = this.userAnswers[q.id] || null;

    let optionsHtml = '';
    (q.options || []).forEach(opt => {
      const isSelected = selectedOpt === opt.label;
      const isCorrect = opt.label === q.correct_option;
      
      let borderClass = 'border-gray-200 dark:border-slate-700 hover:border-orange-400 dark:hover:border-orange-500';
      let bgClass = 'bg-white dark:bg-slate-800';

      if (this.isPracticeMode && selectedOpt) {
        if (isCorrect) {
          borderClass = 'border-green-500 bg-green-50 dark:bg-green-950/40 text-green-900 dark:text-green-200';
        } else if (isSelected && !isCorrect) {
          borderClass = 'border-red-500 bg-red-50 dark:bg-red-950/40 text-red-900 dark:text-red-200';
        }
      } else if (isSelected) {
        borderClass = 'border-orange-500 bg-orange-50 dark:bg-orange-950/30';
      }

      optionsHtml += `
        <div onclick="ExamSimulator.selectOption('${q.id}', '${opt.label}')"
             class="flex items-start gap-3 p-4 rounded-xl border-2 ${borderClass} ${bgClass} cursor-pointer transition-all duration-200">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center font-bold text-sm shrink-0 ${isSelected ? 'bg-orange-500 text-white' : 'bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-slate-300'}">
            ${opt.label}
          </div>
          <div class="text-sm sm:text-base font-medium text-gray-800 dark:text-slate-200 pt-0.5 leading-snug">
            ${opt.text}
          </div>
        </div>
      `;
    });

    // Explanation / Paywall box
    let explanationHtml = '';
    if (this.isPracticeMode && selectedOpt) {
      if (isLocked) {
        explanationHtml = `
          <div class="paywall-blur-box mt-6 border border-amber-300 dark:border-amber-700/60 rounded-xl overflow-hidden">
            <div class="paywall-blur-content p-4 bg-amber-50 dark:bg-amber-950/20">
              <h5 class="font-bold text-gray-800 dark:text-gray-200">LPU Verified Explanation & Distractor Analysis:</h5>
              <p class="text-sm mt-1">This question appeared in LPU End Term Exam Dec 2023. The key concept requires evaluating boundary condition state transitions and time complexity tradeoffs.</p>
            </div>
            <div class="paywall-overlay">
              <div class="flex items-center gap-3 justify-center mb-2">
                <img src="/static/images/official_paywall_qr.jpg" alt="Official Paytm UPI QR" class="w-14 h-14 rounded-lg border-2 border-sky-400 bg-white p-0.5 shadow-sm shrink-0">
                <div class="text-left">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-black bg-amber-500 text-white shadow-sm">
                    🔒 PRO EXCLUSIVE SOLUTION
                  </span>
                  <div class="text-xs font-bold text-gray-800 dark:text-white mt-0.5">Scan QR to Unlock Evaluator Key</div>
                </div>
              </div>
              <p class="text-xs text-gray-700 dark:text-slate-300 font-semibold mb-3">
                Pay ₹29 to mk9817223@okicici & verify 12-digit UTR to unlock instantly.
              </p>
              <button onclick="PaywallManager.openCheckoutModal('mock_test_29', '${this.currentPaper ? this.currentPaper.subject_code : ''}')" class="px-5 py-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white text-xs font-bold rounded-lg shadow-md transition-all">
                Verify Payment & Unlock (₹29) →
              </button>
            </div>
          </div>
        `;
      } else {
        explanationHtml = `
          <div class="mt-6 p-4 rounded-xl border border-green-200 dark:border-green-800/60 bg-green-50/70 dark:bg-green-950/20 animate-fade-in-up">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-green-700 dark:text-green-400">
                ✓ Correct Answer: Option (${q.correct_option})
              </span>
              <span class="text-xs text-gray-500 dark:text-slate-400 font-medium">LPU Evaluator Key</span>
            </div>
            <p class="text-sm text-gray-700 dark:text-slate-300 leading-relaxed font-normal">
              ${q.explanation}
            </p>
          </div>
        `;
      }
    }

    container.innerHTML = `
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-gray-200 dark:border-slate-800 shadow-sm p-6 sm:p-8">
        <!-- Question Metadata Bar -->
        <div class="flex flex-wrap items-center justify-between gap-2 pb-4 mb-6 border-b border-gray-100 dark:border-slate-800">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-orange-100 dark:bg-orange-950/50 text-orange-700 dark:text-orange-400">
              Q ${this.currentQuestionIndex + 1} of ${mcqs.length}
            </span>
            <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-300">
              ${q.difficulty} Level
            </span>
            <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-100 dark:bg-blue-950/50 text-blue-700 dark:text-blue-400">
              Topic: ${q.topic || 'General'}
            </span>
          </div>

          <div class="flex items-center gap-2 text-xs">
            <span class="px-2.5 py-1 rounded-full bg-purple-50 dark:bg-purple-950/40 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800 font-semibold">
              🎯 ${q.pyq_tag || 'LPU Past Paper Item'}
            </span>
            <span class="font-bold text-gray-500">1 Mark</span>
          </div>
        </div>

        <!-- Question Text -->
        <h4 class="text-lg sm:text-xl font-bold text-gray-900 dark:text-white leading-relaxed mb-6">
          ${q.question}
        </h4>

        <!-- Options List -->
        <div class="space-y-3">
          ${optionsHtml}
        </div>

        <!-- Explanation -->
        ${explanationHtml}

        <!-- Bottom Controls for this question -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-6 mt-8 border-t border-gray-100 dark:border-slate-800">
          <button onclick="ExamSimulator.toggleReview('${q.id}')"
                  class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold border border-purple-300 dark:border-purple-800 text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/30 transition-colors">
            ${this.questionStatus[q.id] === 'review' ? '★ Unmark Review' : '☆ Mark for Review'}
          </button>

          <div class="flex items-center gap-2">
            <button onclick="ExamSimulator.prevQuestion()"
                    ${this.currentQuestionIndex === 0 ? 'disabled' : ''}
                    class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-700 disabled:opacity-40 transition-colors">
              ← Previous
            </button>
            <button onclick="ExamSimulator.nextQuestion()"
                    ${this.currentQuestionIndex === mcqs.length - 1 ? 'disabled' : ''}
                    class="px-5 py-2 rounded-xl text-xs sm:text-sm font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-md shadow-orange-500/20 disabled:opacity-40 transition-colors">
              Next Question →
            </button>
          </div>
        </div>
      </div>
    `;

    this.renderQuestionPalette();
  },

  selectOption(qId, label) {
    this.userAnswers[qId] = label;
    if (this.questionStatus[qId] !== 'review') {
      this.questionStatus[qId] = 'answered';
    }
    this.renderCurrentQuestion();
    this.updatePaletteCounters();
  },

  toggleReview(qId) {
    if (this.questionStatus[qId] === 'review') {
      this.questionStatus[qId] = this.userAnswers[qId] ? 'answered' : 'unanswered';
    } else {
      this.questionStatus[qId] = 'review';
    }
    this.renderCurrentQuestion();
    this.updatePaletteCounters();
  },

  nextQuestion() {
    const mcqs = this.currentPaper.sections.section_a.questions || [];
    if (this.currentQuestionIndex < mcqs.length - 1) {
      this.currentQuestionIndex++;
      const nextQ = mcqs[this.currentQuestionIndex];
      if (this.questionStatus[nextQ.id] === 'unvisited') {
        this.questionStatus[nextQ.id] = 'unanswered';
      }
      this.renderCurrentQuestion();
    }
  },

  prevQuestion() {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
      this.renderCurrentQuestion();
    }
  },

  goToQuestion(idx) {
    const mcqs = this.currentPaper.sections.section_a.questions || [];
    if (idx >= 0 && idx < mcqs.length) {
      this.currentQuestionIndex = idx;
      const targetQ = mcqs[idx];
      if (this.questionStatus[targetQ.id] === 'unvisited') {
        this.questionStatus[targetQ.id] = 'unanswered';
      }
      this.renderCurrentQuestion();
    }
  },

  renderSubjectiveSections() {
    const shortContainer = document.getElementById('short-questions-list');
    const longContainer = document.getElementById('long-questions-list');
    const isPro = this.hasPaperAccess();

    // Render Section B (Short Answers)
    if (shortContainer) {
      const shortQs = this.currentPaper.sections.section_b.questions || [];
      if (shortQs.length === 0) {
        shortContainer.innerHTML = '<p class="text-sm text-gray-500">No subjective questions in CA pattern.</p>';
      } else {
        shortContainer.innerHTML = shortQs.map((q, i) => {
          const isLocked = q.is_locked && !isPro;
          return `
            <div class="bg-white dark:bg-slate-900 rounded-2xl border border-gray-200 dark:border-slate-800 p-6 shadow-sm">
              <div class="flex items-center justify-between pb-3 mb-4 border-b border-gray-100 dark:border-slate-800">
                <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-blue-100 dark:bg-blue-950/50 text-blue-700 dark:text-blue-400">
                  Question ${q.q_number || i + 1} • Section B
                </span>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-purple-600 dark:text-purple-400 font-semibold">${q.pyq_tag || 'LPU PYQ'}</span>
                  <span class="text-sm font-bold text-gray-700 dark:text-slate-300">[${q.marks || 5} Marks]</span>
                </div>
              </div>

              <h4 class="text-base sm:text-lg font-bold text-gray-900 dark:text-white mb-4">
                ${q.question}
              </h4>

              <div class="text-xs text-gray-500 dark:text-slate-400 mb-4">
                Bloom's Taxonomy: <span class="font-semibold text-gray-700 dark:text-slate-200">${q.bloom_level || 'Understanding'}</span> | Outcome: <span class="font-semibold text-gray-700 dark:text-slate-200">${q.course_outcome || 'CO1'}</span>
              </div>

              ${isLocked ? `
                <div class="paywall-blur-box border border-amber-300 dark:border-amber-700/60 rounded-xl overflow-hidden mt-3">
                  <div class="paywall-blur-content p-4 bg-amber-50 dark:bg-amber-950/20 text-xs">
                    <p><strong>1. Core Definition:</strong></p>
                    <p>Comprehensive structured model answer with comparison matrix, formula derivations, and edge cases.</p>
                  </div>
                  <div class="paywall-overlay">
                    <div class="flex items-center gap-2.5 mb-1.5">
                      <img src="/static/images/official_paywall_qr.jpg" alt="Official Paytm UPI QR" class="w-10 h-10 rounded-lg border-2 border-sky-400 bg-white p-0.5 shrink-0">
                      <span class="text-xs font-bold text-amber-500">🔒 5-Mark LPU Model Answer & Rubric Locked</span>
                    </div>
                    <button onclick="PaywallManager.openCheckoutModal('mock_test_29', '${this.currentPaper ? this.currentPaper.subject_code : ''}')" class="px-4 py-1.5 bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold rounded-lg shadow-sm">
                      Scan QR & Verify UTR (₹29) →
                    </button>
                  </div>
                </div>
              ` : `
                <div class="mt-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60 text-sm">
                  <h6 class="font-bold text-xs uppercase tracking-wider text-orange-600 dark:text-orange-400 mb-2">Ideal LPU Model Answer:</h6>
                  <div class="prose dark:prose-invert max-w-none text-gray-800 dark:text-slate-200 text-xs sm:text-sm whitespace-pre-wrap">${q.model_answer}</div>
                  
                  <div class="mt-4 pt-3 border-t border-gray-200 dark:border-slate-700 text-xs text-gray-600 dark:text-slate-400">
                    <strong class="text-slate-700 dark:text-slate-300">Official Marking Scheme Rubric:</strong><br>
                    <pre class="font-sans whitespace-pre-wrap mt-1">${q.marking_rubric}</pre>
                  </div>
                </div>
              `}
            </div>
          `;
        }).join('');
      }
    }

    // Render Section C (Long Answers)
    if (longContainer) {
      const longQs = this.currentPaper.sections.section_c.questions || [];
      if (longQs.length === 0) {
        longContainer.innerHTML = '<p class="text-sm text-gray-500">No long questions in this pattern.</p>';
      } else {
        longContainer.innerHTML = longQs.map((q, i) => {
          const isLocked = q.is_locked && !isPro;
          return `
            <div class="bg-white dark:bg-slate-900 rounded-2xl border border-gray-200 dark:border-slate-800 p-6 shadow-sm">
              <div class="flex items-center justify-between pb-3 mb-4 border-b border-gray-100 dark:border-slate-800">
                <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-100 dark:bg-purple-950/50 text-purple-700 dark:text-purple-400">
                  Question ${q.q_number || i + 1} • Section C (Internal Choice)
                </span>
                <span class="text-sm font-bold text-gray-700 dark:text-slate-300">[${q.marks || 10} Marks]</span>
              </div>

              <div class="space-y-3 mb-4">
                <div class="p-3 rounded-xl bg-orange-50/50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-800/40">
                  <span class="font-bold text-xs text-orange-600 dark:text-orange-400">OPTION A:</span>
                  <p class="font-semibold text-gray-900 dark:text-white text-sm sm:text-base mt-1">${q.option_a}</p>
                </div>
                
                <div class="text-center font-bold text-xs text-gray-400 dark:text-slate-500 tracking-widest uppercase">--- OR ---</div>

                <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60">
                  <span class="font-bold text-xs text-slate-500">OPTION B:</span>
                  <p class="font-semibold text-gray-900 dark:text-white text-sm sm:text-base mt-1">${q.option_b}</p>
                </div>
              </div>

              ${isLocked ? `
                <div class="paywall-blur-box border border-amber-300 dark:border-amber-700/60 rounded-xl overflow-hidden mt-4">
                  <div class="paywall-blur-content p-5 bg-amber-50 dark:bg-amber-950/20 text-xs">
                    <p><strong>Comprehensive 10-Mark Solution Blueprint:</strong></p>
                    <p>Part I: Architectural Overview & System Design (3M) ...</p>
                    <p>Part II: Algorithmic Logic & Pseudocode (3M) ...</p>
                    <p>Part III: Complexity Analysis & Space-Time Trade-offs (2M) ...</p>
                  </div>
                  <div class="paywall-overlay">
                    <span class="text-xs font-bold text-amber-500 mb-1">🔒 Full 10-Mark Comprehensive Solution Locked</span>
                    <p class="text-xs text-gray-600 dark:text-slate-400 mb-3 max-w-sm">
                      Get full multi-tier architecture diagrams, Python/C++ code implementations, and evaluator rubrics.
                    </p>
                    <button onclick="PaywallManager.openCheckoutModal('semester_pro', '${this.currentPaper ? this.currentPaper.subject_code : ''}')" class="px-5 py-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white text-xs font-bold rounded-lg shadow-md">
                      Unlock All 10M Solutions with Verto Pro →
                    </button>
                  </div>
                </div>
              ` : `
                <div class="mt-4 p-5 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/60 text-sm">
                  <h6 class="font-bold text-xs uppercase tracking-wider text-orange-600 dark:text-orange-400 mb-2">Option A Comprehensive 10-Mark Solution:</h6>
                  <div class="prose dark:prose-invert max-w-none text-gray-800 dark:text-slate-200 text-xs sm:text-sm whitespace-pre-wrap">${q.model_answer}</div>
                  
                  <div class="mt-4 pt-3 border-t border-gray-200 dark:border-slate-700 text-xs text-gray-600 dark:text-slate-400">
                    <strong class="text-slate-700 dark:text-slate-300">LPU Step-by-Step Marking Rubric:</strong><br>
                    <pre class="font-sans whitespace-pre-wrap mt-1">${q.marking_rubric}</pre>
                  </div>
                </div>
              `}
            </div>
          `;
        }).join('');
      }
    }
  },

  startTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    const timerDisplay = document.getElementById('exam-timer');
    if (!timerDisplay) return;

    this.timerInterval = setInterval(() => {
      if (this.secondsRemaining <= 0) {
        clearInterval(this.timerInterval);
        alert('Time is up! Submitting your exam automatically.');
        this.submitExam();
        return;
      }
      this.secondsRemaining--;
      const hours = Math.floor(this.secondsRemaining / 3600);
      const minutes = Math.floor((this.secondsRemaining % 3600) / 60);
      const seconds = this.secondsRemaining % 60;

      const formatted = hours > 0 
        ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
        : `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

      timerDisplay.textContent = formatted;

      // Color warning when less than 5 mins
      if (this.secondsRemaining < 300) {
        timerDisplay.classList.add('text-red-500', 'animate-pulse');
      } else {
        timerDisplay.classList.remove('text-red-500', 'animate-pulse');
      }
    }, 1000);
  },

  setupControls() {
    // Mode Switcher (Practice vs Test)
    const modeBtn = document.getElementById('sim-mode-toggle');
    if (modeBtn) {
      modeBtn.addEventListener('click', () => {
        this.isPracticeMode = !this.isPracticeMode;
        modeBtn.innerHTML = this.isPracticeMode
          ? `<span>💡 Practice Mode (Instant Explanations)</span>`
          : `<span>⏱️ Timed Test Mode (Exam Conditions)</span>`;
        this.renderCurrentQuestion();
      });
    }

    // Submit Exam Button
    const submitBtn = document.getElementById('submit-exam-btn');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => this.confirmSubmit());
    }

    // Export PDF Button
    const exportBtn = document.getElementById('export-pdf-btn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => this.exportPrintable());
    }
  },

  confirmSubmit() {
    let answered = 0;
    const mcqs = this.currentPaper.sections.section_a.questions || [];
    mcqs.forEach(q => {
      if (this.userAnswers[q.id]) answered++;
    });

    const confirmMsg = `You have answered ${answered} out of ${mcqs.length} MCQs.\nAre you sure you want to finish and submit the examination?`;
    if (confirm(confirmMsg)) {
      this.submitExam();
    }
  },

  submitExam() {
    if (this.timerInterval) clearInterval(this.timerInterval);

    const mcqs = this.currentPaper.sections.section_a.questions || [];
    let correct = 0;
    let incorrect = 0;
    let unattempted = 0;

    mcqs.forEach(q => {
      const userAns = this.userAnswers[q.id];
      if (!userAns) {
        unattempted++;
      } else if (userAns === q.correct_option) {
        correct++;
      } else {
        incorrect++;
      }
    });

    const negMark = this.currentPaper.negative_marking ? (incorrect * 0.25) : 0.0;
    const score = Math.max(0.0, (correct * 1.0) - negMark);
    const totalPossible = mcqs.length;
    const percentage = ((score / totalPossible) * 100).toFixed(1);

    // Determine LPU Grade
    let grade = 'E';
    if (percentage >= 90) grade = 'O (Outstanding)';
    else if (percentage >= 80) grade = 'A+ (Excellent)';
    else if (percentage >= 70) grade = 'A (Very Good)';
    else if (percentage >= 60) grade = 'B+ (Good)';
    else if (percentage >= 50) grade = 'B (Above Average)';
    else if (percentage >= 40) grade = 'C (Average / Pass)';

    const stats = {
      totalPossible,
      correct,
      incorrect,
      unattempted,
      negMark,
      score,
      percentage,
      grade
    };

    // Send mock test results to backend so student profile & admin dashboard record it
    try {
      const u = window.AuthManager?.currentUser;
      const fullSummary = {
        ...stats,
        user_answers: this.userAnswers,
        completed_at: new Date().toISOString()
      };
      fetch('/api/mock-test/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: u?.id || null,
          user_name: u?.name || 'LPU Student',
          subject_code: this.currentPaper.subject_code || 'CSE101',
          subject_name: this.currentPaper.subject_name || 'Subject Test',
          exam_type: this.currentPaper.exam_title || 'Midterm Mock Test',
          score: score,
          total_marks: totalPossible,
          percentage: parseFloat(percentage),
          grade: grade,
          summary: fullSummary
        })
      });
      if (window.AuthManager) {
        window.AuthManager.recordActivity(
          'mock_test',
          `Mock Test: ${this.currentPaper.subject_code || 'Exam'} (${score}/${totalPossible} - ${grade})`,
          this.currentPaper.subject_code,
          fullSummary
        );
      }
    } catch (e) {
      console.warn("Failed to record mock test:", e);
    }

    // Show Scorecard Modal
    this.showScorecardModal(stats);
  },

  showScorecardModal(stats) {
    const modal = document.getElementById('scorecard-modal');
    const content = document.getElementById('scorecard-content');
    if (!modal || !content) return;

    content.innerHTML = `
      <div class="text-center pb-6 border-b border-gray-100 dark:border-slate-800">
        <span class="inline-flex px-3 py-1 rounded-full text-xs font-bold bg-orange-100 dark:bg-orange-950/50 text-orange-700 dark:text-orange-400 mb-2">
          ${this.currentPaper.exam_title} Performance Report
        </span>
        <h3 class="text-2xl font-black text-gray-900 dark:text-white">
          Score: <span class="text-orange-500">${stats.score}</span> / ${stats.totalPossible}
        </h3>
        <p class="text-sm font-semibold text-gray-500 dark:text-slate-400 mt-1">
          Percentage: <strong class="text-gray-900 dark:text-white">${stats.percentage}%</strong> • LPU Grade: <strong class="text-purple-600 dark:text-purple-400">${stats.grade}</strong>
        </p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 py-6">
        <div class="p-3 rounded-xl bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800 text-center">
          <span class="text-2xl font-black text-green-600 dark:text-green-400">${stats.correct}</span>
          <div class="text-xs font-semibold text-green-800 dark:text-green-300">Correct (+${stats.correct})</div>
        </div>

        <div class="p-3 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 text-center">
          <span class="text-2xl font-black text-red-600 dark:text-red-400">${stats.incorrect}</span>
          <div class="text-xs font-semibold text-red-800 dark:text-red-300">Wrong (-${stats.negMark})</div>
        </div>

        <div class="p-3 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-center">
          <span class="text-2xl font-black text-gray-600 dark:text-slate-300">${stats.unattempted}</span>
          <div class="text-xs font-semibold text-gray-500 dark:text-slate-400">Unattempted</div>
        </div>

        <div class="p-3 rounded-xl bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-800 text-center">
          <span class="text-2xl font-black text-purple-600 dark:text-purple-400">${stats.percentage}%</span>
          <div class="text-xs font-semibold text-purple-800 dark:text-purple-300">Accuracy</div>
        </div>
      </div>

      <div class="p-4 rounded-xl bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-800/40 text-xs text-gray-700 dark:text-slate-300 space-y-1 mb-6">
        <p class="font-bold text-orange-700 dark:text-orange-400">🎓 LPU Exam Setter Insight:</p>
        <p>You scored best in foundational definitions. Practice edge-case questions and operator precedence to ensure a 9+ CGPA in your upcoming End Term Examination.</p>
      </div>

      <div class="flex items-center gap-3">
        <button onclick="document.getElementById('scorecard-modal').close(); ExamSimulator.isPracticeMode = true; ExamSimulator.renderCurrentQuestion();"
                class="flex-1 py-3 bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 font-bold rounded-xl text-gray-700 dark:text-slate-300 text-xs sm:text-sm transition-colors">
          Review Explanations
        </button>
        <button onclick="ExamSimulator.exportPrintable()"
                class="flex-1 py-3 bg-orange-500 hover:bg-orange-600 font-bold rounded-xl text-white text-xs sm:text-sm shadow-md shadow-orange-500/20 transition-colors">
          🖨️ Export LPU Paper (PDF)
        </button>
      </div>
    `;

    modal.showModal();
  },

  async exportPrintable() {
    if (!this.currentPaper) return;

    try {
      const res = await fetch('/api/export-printable', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          paper: this.currentPaper,
          show_solutions: this.hasPaperAccess()
        })
      });

      const html = await res.text();
      const printWindow = window.open('', '_blank');
      printWindow.document.write(html);
      printWindow.document.close();
    } catch (e) {
      alert('Failed to generate printable PDF.');
    }
  },

  unlockPaperSolutions() {
    // When pro is activated, unmask all questions in memory and re-render
    if (!this.currentPaper) return;

    const mcqs = this.currentPaper.sections.section_a.questions || [];
    mcqs.forEach(q => {
      q.is_locked = false;
      if (q.hidden_correct_option) q.correct_option = q.hidden_correct_option;
      if (q.hidden_explanation) q.explanation = q.hidden_explanation;
    });

    const shortQs = this.currentPaper.sections.section_b.questions || [];
    shortQs.forEach(q => {
      q.is_locked = false;
      if (q.hidden_model_answer) q.model_answer = q.hidden_model_answer;
      if (q.hidden_marking_rubric) q.marking_rubric = q.hidden_marking_rubric;
    });

    const longQs = this.currentPaper.sections.section_c.questions || [];
    longQs.forEach(q => {
      q.is_locked = false;
      if (q.hidden_model_answer) q.model_answer = q.hidden_model_answer;
    });

    this.renderCurrentQuestion();
    this.renderSubjectiveSections();
  }
};

window.ExamSimulator = ExamSimulator;
