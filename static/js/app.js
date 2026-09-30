/**
 * LPU Verto AI Exam Prep - Main Application Logic & Study Asset Studio
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize Theme
  initTheme();

  // Initialize Paywall
  await PaywallManager.init();

  // Setup Tabs
  setupTabs();

  // Load Preloaded Subjects & Custom Subjects
  await loadSubjectsHub();

  // Load LPU Program Structure
  await loadPrograms();

  // Setup Form Handlers
  setupFormHandlers();

  // Setup Note Bank Search
  setupNoteBankSearch();

  // Setup Custom Subject Modal
  setupCustomSubjectModal();

  // Track live visitor analytics
  recordVisitHit();
});

// ── Visitor Analytics Tracker ─────────────────────────────────────────
function recordVisitHit() {
  try {
    let sessId = localStorage.getItem('acadassist_sess_id');
    if (!sessId) {
      sessId = 'sess_' + Math.random().toString(36).substring(2, 10) + '_' + Date.now().toString(36);
      localStorage.setItem('acadassist_sess_id', sessId);
    }
    const user = (window.AuthManager && window.AuthManager.currentUser) ? window.AuthManager.currentUser.name : null;
    fetch('/api/analytics/visit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessId,
        path: window.location.pathname || '/',
        user_id: user
      })
    }).catch(() => {});
  } catch (e) {}
}

// ── Theme Management ──────────────────────────────────────────────────
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const isDark = localStorage.getItem('theme') === 'dark' || 
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

  if (isDark) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
      const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
      localStorage.setItem('theme', current);
    });
  }
}

// ── Tab Management ────────────────────────────────────────────────────
function setupTabs() {
  const tabs = document.querySelectorAll('[data-tab-target]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.getAttribute('data-tab-target');
      switchTab(targetId);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.add('hidden');
  });
  document.querySelectorAll('[data-tab-target]').forEach(tab => {
    tab.classList.remove('border-orange-500', 'text-orange-600', 'dark:text-orange-400');
    tab.classList.add('border-transparent', 'text-gray-500', 'dark:text-slate-400');
  });

  const targetContent = document.getElementById(tabId);
  const activeTabBtn = document.querySelector(`[data-tab-target="${tabId}"]`);

  if (targetContent) targetContent.classList.remove('hidden');
  if (activeTabBtn) {
    activeTabBtn.classList.remove('border-transparent', 'text-gray-500', 'dark:text-slate-400');
    activeTabBtn.classList.add('border-orange-500', 'text-orange-600', 'dark:text-orange-400');
  }
}

// ── Preloaded LPU Subjects Hub (All 266+ Subjects Catalog) ──
let allAvailableSubjects = [];
window.allAvailableSubjects = allAvailableSubjects;
let activeSemesterFilter = 'all';
let activeSearchQuery = '';

async function loadSubjectsHub() {
  const hubContainer = document.getElementById('preloaded-subjects-grid');
  if (!hubContainer) return;

  try {
    const res = await fetch('/api/all-subjects');
    allAvailableSubjects = await res.json();
    window.allAvailableSubjects = allAvailableSubjects;
    renderFilteredSubjects();
    setupSubjectsSearch();
    populateStudioCourseDropdown(allAvailableSubjects);
    if (window.PYQManager && typeof window.PYQManager.loadAllCoursesDropdown === 'function') {
      window.PYQManager.loadAllCoursesDropdown();
    }
  } catch (e) {
    console.error("Failed to load all subjects:", e);
    // Fallback to preloaded
    try {
      const resFallback = await fetch('/api/preloaded-subjects');
      allAvailableSubjects = await resFallback.json();
      window.allAvailableSubjects = allAvailableSubjects;
      renderFilteredSubjects();
      populateStudioCourseDropdown(allAvailableSubjects);
    } catch (err) {
      hubContainer.innerHTML = '<div class="col-span-full py-12 text-center text-red-500">Failed to load subjects.</div>';
    }
  }
}

function setupSubjectsSearch() {
  const searchInput = document.getElementById('subjects-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      activeSearchQuery = e.target.value.toLowerCase().trim();
      renderFilteredSubjects();
    });
  }
}

window.filterSubjectsBySemester = function(sem) {
  activeSemesterFilter = sem;
  document.querySelectorAll('.sem-filter-pill').forEach(btn => {
    btn.classList.remove('bg-pink-500', 'text-white', 'shadow-sm', 'active');
    btn.classList.add('bg-gray-100', 'dark:bg-slate-800', 'text-gray-700', 'dark:text-slate-300');
  });
  const activeBtn = document.querySelector(`.sem-filter-pill[data-sem="${sem}"]`);
  if (activeBtn) {
    activeBtn.classList.remove('bg-gray-100', 'dark:bg-slate-800', 'text-gray-700', 'dark:text-slate-300');
    activeBtn.classList.add('bg-pink-500', 'text-white', 'shadow-sm', 'active');
  }
  renderFilteredSubjects();
};

function renderFilteredSubjects() {
  const hubContainer = document.getElementById('preloaded-subjects-grid');
  const countBadge = document.getElementById('subjects-count-badge');
  if (!hubContainer) return;

  let filtered = allAvailableSubjects;

  // Filter by semester
  if (activeSemesterFilter === 'priority') {
    const priorityCodes = ['MTH166', 'PHY109', 'PHY110', 'ECE131', 'CSE101', 'CSE205', 'INT108', 'MTH401', 'CSE408', 'PEA305', 'CHE110', 'CSE316', 'CSE306', 'CSE326'];
    filtered = filtered.filter(s => priorityCodes.includes(s.code.toUpperCase()));
  } else if (activeSemesterFilter !== 'all') {
    const semClean = activeSemesterFilter.toLowerCase().replace(' ', '');
    filtered = filtered.filter(s => (s.semester || '').toLowerCase().replace(' ', '').includes(semClean));
  }

  // Filter by search query
  if (activeSearchQuery) {
    filtered = filtered.filter(s => 
      s.code.toLowerCase().includes(activeSearchQuery) || 
      (s.name || '').toLowerCase().includes(activeSearchQuery) ||
      (s.description || '').toLowerCase().includes(activeSearchQuery)
    );
  }

  if (countBadge) {
    countBadge.innerText = `${filtered.length} Subjects Showing`;
  }

  if (filtered.length === 0) {
    hubContainer.innerHTML = `
      <div class="col-span-full py-16 text-center">
        <span class="text-4xl">🔍</span>
        <h4 class="text-base font-bold text-gray-700 dark:text-slate-300 mt-2">No subjects found</h4>
        <p class="text-xs text-gray-500 mt-1">Try clearing your search query or switching semester tab.</p>
        <button onclick="filterSubjectsBySemester('all'); document.getElementById('subjects-search-input').value='';" class="mt-3 px-4 py-1.5 rounded-xl bg-pink-500 text-white font-bold text-xs">Reset All Filters</button>
      </div>
    `;
    return;
  }

  hubContainer.innerHTML = filtered.map(s => {
    const isCustom = s.is_custom;
    const badgeColor = isCustom ? 'bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-400' : 'bg-pink-100 dark:bg-pink-950/60 text-pink-700 dark:text-pink-400';
    const badgeText = isCustom ? 'Custom Subject' : (s.badge || `${s.semester || 'LPU'} • Core`);

    return `
      <div class="rounded-3xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm hover:shadow-md hover:border-pink-400 transition-all flex flex-col justify-between space-y-4">
        <div>
          <div class="flex items-center justify-between gap-2 mb-2">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold ${badgeColor}">
              ${badgeText}
            </span>
            <span class="text-xs text-gray-500 font-semibold">${s.semester || 'Sem 1'} • ${s.credits || '4 Credits'}</span>
          </div>

          <h3 class="text-lg font-black text-gray-900 dark:text-white leading-tight">
            ${s.code} — ${s.name}
          </h3>
          <p class="text-xs text-gray-600 dark:text-slate-400 mt-2 line-clamp-2">
            ${s.description || 'Comprehensive syllabus modules, past year question bank, and verified LPU notes.'}
          </p>
        </div>

        <div class="space-y-2 pt-3 border-t border-gray-100 dark:border-slate-800">
          <!-- Dual Paywall Buttons: Mock Test ₹29 & Subject Pass ₹59 -->
          <div class="grid grid-cols-2 gap-2">
            <button onclick="startSubjectMockTest('${s.code}', '${s.name.replace(/'/g, "\\'")}', '${s.semester || 'Sem2'}')" class="py-2.5 px-2 rounded-xl bg-gradient-to-r from-pink-500 via-rose-500 to-orange-500 hover:from-pink-600 hover:to-orange-600 text-white font-extrabold text-[11px] shadow-sm transition-all flex items-center justify-center gap-1">
              <span>⚡ Mock Test (₹29)</span>
            </button>
            <button onclick="PaywallManager.openCheckoutModal('subject_pass_49', '${s.code}')" class="py-2.5 px-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-extrabold text-[11px] shadow-sm transition-all flex items-center justify-center gap-1">
              <span>📚 Subject Pass (₹59)</span>
            </button>
          </div>

          <!-- PYQ Question Papers Button -->
          <button onclick="openPYQForSubject('${s.code}')" class="w-full py-2 rounded-xl bg-pink-50 dark:bg-pink-950/40 hover:bg-pink-100 dark:hover:bg-pink-900/40 text-pink-600 dark:text-pink-400 font-bold text-xs border border-pink-200 dark:border-pink-800/60 transition-colors flex items-center justify-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>📂 View PYQs & Past Papers (2021-2024)</span>
          </button>

          <!-- Native PowerPoint (.pptx) & Slide Presenter -->
          <div class="grid grid-cols-2 gap-2">
            <button onclick="downloadSubjectPPT('${s.code}')" class="py-2 px-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-[11px] shadow-sm transition-all flex items-center justify-center gap-1 text-center">
              <span>📥 Download .pptx</span>
            </button>
            <button onclick="launchSubjectProjector('${s.code}')" class="py-2 px-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-[11px] transition-colors flex items-center justify-center gap-1">
              <span>🖥️ View Slides</span>
            </button>
          </div>

          <div class="text-[11px] font-bold text-gray-500 uppercase tracking-wider pt-1">Study Asset Studio:</div>
          
          <div class="grid grid-cols-2 gap-2 text-xs">
            <button onclick="triggerAssetGeneration('notes', '${s.code}', '${s.name.replace(/'/g, "\\'")}', '${s.semester || 'Sem2'}')" class="p-2 rounded-xl bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400 hover:bg-orange-100 dark:hover:bg-orange-900/50 font-bold text-left transition-colors flex items-center gap-1.5">
              <span>📖</span> Full Notes
            </button>
            <button onclick="triggerAssetGeneration('short_notes', '${s.code}', '${s.name.replace(/'/g, "\\'")}', '${s.semester || 'Sem2'}')" class="p-2 rounded-xl bg-amber-50 dark:bg-amber-950/30 text-amber-600 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-900/50 font-bold text-left transition-colors flex items-center gap-1.5">
              <span>⚡</span> Cram Notes
            </button>
            <button onclick="triggerAssetGeneration('slides', '${s.code}', '${s.name.replace(/'/g, "\\'")}', '${s.semester || 'Sem2'}')" class="p-2 rounded-xl bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 font-bold text-left transition-colors flex items-center gap-1.5">
              <span>🖥️</span> Slides Deck
            </button>
            <button onclick="triggerAssetGeneration('roadmap', '${s.code}', '${s.name.replace(/'/g, "\\'")}', '${s.semester || 'Sem2'}')" class="p-2 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 dark:hover:bg-emerald-900/50 font-bold text-left transition-colors flex items-center gap-1.5">
              <span>🗺️</span> 9+ CGPA Plan
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

window.openPYQForSubject = function(code) {
  switchTab('tab-pyq');
  if (window.PYQManager) {
    window.PYQManager.selectSubject(code);
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

window.downloadSubjectPPT = function(code) {
  const pm = window.PaywallManager;
  const hasAccess = pm && pm.hasSubjectAccess(code);

  if (!hasAccess) {
    if (pm) {
      pm.openCheckoutModal('subject_pass_49', code);
      return;
    }
  }
  window.location.href = `/api/subject/${code}/download-pptx`;
};

window.startSubjectMockTest = async function(subjectCode, subjectName, semester = 'Sem2') {
  const pm = window.PaywallManager;
  const hasAccess = pm && pm.hasMockAccess(subjectCode);

  if (!hasAccess) {
    // Open ₹29 Mock Test Paywall Modal with UPI 8053122848@ptyes
    if (pm) {
      pm.openCheckoutModal('mock_test_29', subjectCode);
      return;
    }
  }

  // Switch to simulator tab and automatically generate official LPU mock test
  switchTab('tab-simulator');
  const simLoader = document.getElementById('simulator-loader');
  if (simLoader) simLoader.classList.remove('hidden');

  try {
    const formData = new FormData();
    formData.append('subject_code', subjectCode);
    formData.append('subject_name', subjectName);
    formData.append('semester', semester);
    formData.append('exam_type', 'mte');
    formData.append('mcq_count', '30');
    formData.append('fetch_lpuverto_data', 'true');
    formData.append('token', localStorage.getItem('lpu_verto_pro_token') || '');

    const res = await fetch('/api/generate-exam', {
      method: 'POST',
      body: formData
    });
    const paper = await res.json();
    if (window.ExamSimulator) {
      window.ExamSimulator.init(paper);
    }
    if (window.AuthManager && paper) {
      window.AuthManager.recordActivity(
        'generated_exam',
        `Generated Exam: ${subjectCode} (${paper.exam_title || 'Mock Test'})`,
        subjectCode,
        { exam_title: paper.exam_title, total_marks: paper.total_marks }
      );
    }
  } catch (err) {
    alert("Failed to synthesize mock test for " + subjectCode);
  } finally {
    if (simLoader) simLoader.classList.add('hidden');
  }
};

// ── Multi-Asset Generation Logic & Study Studio Controller ──────────
window.currentLoadedSlideDeck = null;
window.currentStudioSubject = {
  code: 'CSE101',
  name: 'Computer Programming',
  sem: 'Sem2',
  unit: 'Unit1',
  assetType: 'notes'
};

function populateStudioCourseDropdown(subjects) {
  const dropdown = document.getElementById('studio-course-select');
  if (!dropdown || !subjects || !subjects.length) return;

  const currentVal = dropdown.value || window.currentStudioSubject.code;
  dropdown.innerHTML = subjects.map(s => {
    const sName = (s.name || s.title || 'Course Material').replace(/"/g, '&quot;');
    return `<option value="${s.code}" data-name="${sName}" data-sem="${s.semester || 'Sem2'}">${s.code} — ${s.name || s.title || 'Course Material'}</option>`;
  }).join('');

  if (currentVal) dropdown.value = currentVal;
}

window.onStudioCourseChange = function(code) {
  if (!code) return;
  const match = (window.allAvailableSubjects || []).find(s => s.code.toUpperCase() === code.toUpperCase());
  const name = match ? (match.name || match.title || 'Course Material') : 'Course Material';
  const sem = match ? (match.semester || 'Sem2') : 'Sem2';

  window.currentStudioSubject.code = code.toUpperCase();
  window.currentStudioSubject.name = name;
  window.currentStudioSubject.sem = sem;

  updateStudioUI();
  triggerCurrentAssetGeneration(window.currentStudioSubject.assetType || 'notes');
};

window.onStudioUnitChange = function(unit) {
  window.currentStudioSubject.unit = unit || 'Unit1';
  updateStudioUI();
  triggerCurrentAssetGeneration(window.currentStudioSubject.assetType || 'notes');
};

function updateStudioUI() {
  const s = window.currentStudioSubject;
  const titleDisplay = document.getElementById('asset-studio-subject-title');
  const badgeDisplay = document.getElementById('studio-active-badge');
  const courseDropdown = document.getElementById('studio-course-select');
  const unitDropdown = document.getElementById('studio-unit-select');

  if (titleDisplay) titleDisplay.textContent = `${s.code} — ${s.name} (${s.unit})`;
  if (badgeDisplay) badgeDisplay.textContent = s.code;
  if (courseDropdown && courseDropdown.value !== s.code) courseDropdown.value = s.code;
  if (unitDropdown && unitDropdown.value !== s.unit) unitDropdown.value = s.unit;
}

window.triggerCurrentAssetGeneration = function(assetType) {
  window.currentStudioSubject.assetType = assetType;

  // Update button active states
  const btnNotes = document.getElementById('btn-studio-notes');
  const btnCram = document.getElementById('btn-studio-cram');
  const btnSlides = document.getElementById('btn-studio-slides');
  const btnRoadmap = document.getElementById('btn-studio-roadmap');

  const allBtns = [
    { el: btnNotes, type: 'notes', activeClass: 'bg-orange-500 text-white hover:bg-orange-600' },
    { el: btnCram, type: 'short_notes', activeClass: 'bg-amber-500 text-white hover:bg-amber-600' },
    { el: btnSlides, type: 'slides', activeClass: 'bg-blue-600 text-white hover:bg-blue-700' },
    { el: btnRoadmap, type: 'roadmap', activeClass: 'bg-emerald-600 text-white hover:bg-emerald-700' }
  ];

  allBtns.forEach(b => {
    if (!b.el) return;
    if (b.type === assetType) {
      b.el.className = `px-3.5 py-2 rounded-xl text-xs font-black shadow-sm transition-all flex items-center gap-1.5 ${b.activeClass}`;
    } else {
      b.el.className = `px-3.5 py-2 rounded-xl text-xs font-bold bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-slate-300 hover:bg-gray-200 dark:hover:bg-slate-700 transition-all flex items-center gap-1.5`;
    }
  });

  const s = window.currentStudioSubject;
  triggerAssetGeneration(assetType, s.code, s.name, s.sem, s.unit);
};

window.launchSubjectFromStudioToExam = function() {
  const code = window.currentStudioSubject ? window.currentStudioSubject.code : 'CSE101';
  loadSubjectIntoExamGenerator(code);
};

window.launchSubjectFromStudioToPYQ = function() {
  const code = window.currentStudioSubject ? window.currentStudioSubject.code : 'CSE101';
  openPYQForSubject(code);
};

window.triggerAssetGeneration = async function(assetType, code, name, sem = 'Sem2', unit = 'Unit1') {
  const pm = window.PaywallManager;
  const hasAccess = pm && pm.hasSubjectAccess(code);

  if (!hasAccess) {
    if (pm) {
      pm.openCheckoutModal('subject_pass_49', code);
      return;
    }
  }

  // Update current studio state
  window.currentStudioSubject = {
    code: code.toUpperCase(),
    name: name,
    sem: sem,
    unit: unit,
    assetType: assetType
  };
  updateStudioUI();

  // Switch to Asset Viewer Tab/Section
  switchTab('tab-asset-studio');

  const loader = document.getElementById('asset-studio-loader');
  const outputContainer = document.getElementById('asset-studio-output');
  if (loader) loader.classList.remove('hidden');
  if (outputContainer) outputContainer.innerHTML = '';

  try {
    const formData = new FormData();
    formData.append('asset_type', assetType);
    formData.append('subject_code', code);
    formData.append('subject_name', name);
    formData.append('semester', sem);
    formData.append('unit', unit);
    if (PaywallManager.userData.token) {
      formData.append('token', PaywallManager.userData.token);
    }

    const res = await fetch('/api/generate-asset', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error('Asset generation failed.');
    const data = await res.json();
    if (window.AuthManager) {
      window.AuthManager.recordActivity(
        `generated_${assetType}`,
        `${assetType.replace('_', ' ').toUpperCase()}: ${code} (${unit})`,
        code,
        { asset_type: assetType, subject_name: name, unit: unit }
      );
    }

    renderStudyAsset(data);
  } catch (e) {
    if (outputContainer) {
      outputContainer.innerHTML = `<div class="p-6 text-center text-red-500 font-semibold bg-white dark:bg-slate-900 rounded-2xl border border-red-200">Failed to generate study asset: ${e.message}</div>`;
    }
  } finally {
    if (loader) loader.classList.add('hidden');
  }
};

function renderStudyAsset(data) {
  const container = document.getElementById('asset-studio-output');
  if (!container) return;

  const type = data.asset_type;

  if (type === 'notes') {
    // Render Full Notes
    const sectionsHtml = (data.sections || []).map(sec => `
      <div class="mb-8 p-6 sm:p-8 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-xl font-extrabold text-gray-900 dark:text-white mb-4 pb-2 border-b border-gray-100 dark:border-slate-800">
          ${sec.heading}
        </h3>
        ${sec.diagram_image ? `
          <div class="my-5 p-3 rounded-2xl bg-slate-900/5 dark:bg-slate-800/60 border border-gray-200 dark:border-slate-700 text-center">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-gray-200 dark:border-slate-700 text-[11px] font-bold text-gray-500 dark:text-slate-400">
              <span class="flex items-center gap-1.5 text-orange-600 dark:text-orange-400">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                AI Architectural Concept Diagram (Image)
              </span>
              <span class="text-[10px] text-gray-400">High-Resolution Vector Format</span>
            </div>
            <img src="${sec.diagram_image}" alt="${sec.heading} Diagram" class="mx-auto w-full max-h-72 object-contain rounded-xl shadow-sm bg-slate-900" />
          </div>
        ` : ''}
        <div class="prose dark:prose-invert max-w-none text-sm text-gray-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
          ${sec.content}
        </div>
      </div>
    `).join('');

    container.innerHTML = `
      <div id="printable-study-material" class="space-y-6 animate-fade-in-up">
        <div class="flex items-center justify-between bg-orange-50 dark:bg-orange-950/30 p-4 rounded-2xl border border-orange-200 dark:border-orange-800">
          <div>
            <span class="text-xs font-bold text-orange-600 dark:text-orange-400 uppercase tracking-wider">Comprehensive Study Notes</span>
            <h2 class="text-lg font-black text-gray-900 dark:text-white">${data.subject_code} — ${data.subject_name}</h2>
          </div>
          <span class="px-3 py-1 bg-white dark:bg-slate-800 rounded-full text-xs font-semibold text-gray-600 dark:text-slate-300">
            ${data.total_read_time || '7 min read'}
          </span>
        </div>
        ${sectionsHtml}
      </div>
    `;

  } else if (type === 'short_notes') {
    // Render Short Cram Notes & Flashcards
    const cheatsHtml = (data.cheat_sheet || []).map(c => `
      <div class="p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/60">
        <span class="text-xs font-black uppercase text-amber-800 dark:text-amber-400 tracking-wide">${c.topic}</span>
        <p class="text-xs sm:text-sm font-semibold text-gray-800 dark:text-slate-200 mt-1">${c.summary}</p>
      </div>
    `).join('');

    const flashcardsHtml = (data.flashcards || []).map(f => `
      <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm space-y-2">
        <div class="flex justify-between items-center text-[10px] text-purple-600 dark:text-purple-400 font-bold uppercase">
          <span>Card #${f.id}</span>
          <span>${f.exam_tag || 'LPU Flashcard'}</span>
        </div>
        <p class="font-bold text-sm text-gray-900 dark:text-white">Q: ${f.question}</p>
        <p class="text-xs text-gray-600 dark:text-slate-300 pt-1 border-t border-gray-100 dark:border-slate-800">Ans: ${f.answer}</p>
      </div>
    `).join('');

    const formulasHtml = (data.high_yield_formulas || []).map(f => `
      <li class="font-mono text-xs sm:text-sm text-slate-800 dark:text-slate-200">${f}</li>
    `).join('');

    container.innerHTML = `
      <div id="printable-study-material" class="space-y-6 animate-fade-in-up">
        <div class="bg-amber-50 dark:bg-amber-950/30 p-4 rounded-2xl border border-amber-200 dark:border-amber-800 flex items-center justify-between">
          <div>
            <span class="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider">Revision Cheat Sheet & Flashcards</span>
            <h2 class="text-lg font-black text-gray-900 dark:text-white">${data.subject_code} • ${data.unit}</h2>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${cheatsHtml}
        </div>

        <div class="p-6 rounded-2xl bg-slate-900 text-white shadow-sm space-y-3">
          <h4 class="font-black text-sm text-orange-400 uppercase tracking-wider">Top LPU Formulas & Examination Rules:</h4>
          <ul class="space-y-2">
            ${formulasHtml}
          </ul>
        </div>

        <div class="space-y-3">
          <h4 class="font-black text-base text-gray-900 dark:text-white">High-Yield LPU Flashcards:</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            ${flashcardsHtml}
          </div>
        </div>
      </div>
    `;

  } else if (type === 'slides') {
    // Render Slides Deck
    window.currentLoadedSlideDeck = data;
    const slides = data.slides || [];

    const slidesListHtml = slides.map((s, idx) => `
      <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm space-y-3">
        <div class="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-slate-800">
          <span class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase">Slide ${s.slide_number}</span>
          <span class="text-xs text-gray-400">${data.subject_code}</span>
        </div>
        <h4 class="text-lg font-black text-gray-900 dark:text-white">${s.title}</h4>
        ${s.subtitle ? `<p class="text-xs text-gray-500 font-semibold">${s.subtitle}</p>` : ''}
        
        <ul class="list-disc pl-5 space-y-1 text-xs text-gray-700 dark:text-slate-300">
          ${(s.bullets || []).map(b => `<li>${b}</li>`).join('')}
        </ul>

        ${s.code_or_diagram ? `<pre class="p-3 bg-slate-950 text-sky-400 rounded-xl text-xs overflow-x-auto font-mono mt-2">${s.code_or_diagram}</pre>` : ''}

        ${s.speaker_notes ? `<div class="p-2.5 bg-orange-50/50 dark:bg-orange-950/20 border-l-2 border-orange-500 text-[11px] text-gray-600 dark:text-slate-400">🎙️ <strong>Speaker Note:</strong> ${s.speaker_notes}</div>` : ''}
      </div>
    `).join('');

    container.innerHTML = `
      <div id="printable-study-material" class="space-y-6 animate-fade-in-up">
        <div class="bg-blue-50 dark:bg-blue-950/30 p-4 rounded-2xl border border-blue-200 dark:border-blue-800 flex flex-wrap items-center justify-between gap-4">
          <div>
            <span class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Presentation Slide Deck</span>
            <h2 class="text-lg font-black text-gray-900 dark:text-white">${data.subject_code} — ${data.subject_name}</h2>
          </div>
          <div class="flex items-center gap-2">
            <a href="/api/subject/${data.subject_code}/download-pptx" download="${data.subject_code}_presentation.pptx" class="px-4 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5">
              <span>📥 Download .pptx Deck</span>
            </a>
            <button onclick="launchSlideProjector()" class="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5">
              <span>⛶ Launch Projector Mode</span>
            </button>
          </div>
        </div>

        <div class="space-y-4">
          ${slidesListHtml}
        </div>
      </div>
    `;

  } else if (type === 'roadmap') {
    const tracks = data.study_tracks || [];
    const units = data.units || [];
    const strategy = data.exam_strategy || null;
    const aiGenerated = data.ai_generated === true;

    // Exam Strategy section
    const strategyHtml = strategy ? `
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        ${[
          { icon: '📝', label: 'CA Strategy', val: strategy.ca_tip },
          { icon: '📋', label: 'MTE Strategy', val: strategy.mte_tip },
          { icon: '🎯', label: 'ETE Strategy', val: strategy.ete_tip },
          { icon: '⚠️', label: 'Negative Marking', val: strategy.negative_marking_tip }
        ].map(s => `
          <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700">
            <div class="text-[10px] font-black uppercase text-gray-400 mb-1">${s.icon} ${s.label}</div>
            <p class="text-xs text-gray-700 dark:text-slate-300 leading-relaxed">${s.val}</p>
          </div>
        `).join('')}
      </div>
    ` : '';

    // Units section with important questions
    const unitsHtml = units.map(u => {
      const mcqs = (u.important_questions?.mcq || []).map(q => `
        <div class="p-3 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/50">
          <p class="text-xs font-semibold text-gray-800 dark:text-white mb-2">❓ ${q.q}</p>
          <div class="grid grid-cols-2 gap-1 mb-2">
            ${(q.options||[]).map(o => `<span class="text-[11px] px-2 py-1 rounded-lg bg-white dark:bg-slate-800 text-gray-600 dark:text-slate-400">${o}</span>`).join('')}
          </div>
          <div class="flex items-start gap-2">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-500 text-white shrink-0">✓ ${q.answer}</span>
            <span class="text-[11px] text-gray-500 dark:text-slate-400">${q.explanation || ''}</span>
          </div>
        </div>
      `).join('');

      const fiveMarkHtml = (u.important_questions?.five_mark || []).map(q => `
        <div class="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/50">
          <div class="flex items-center gap-1.5 mb-1">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-amber-500 text-white">5 Marks</span>
          </div>
          <p class="text-xs font-semibold text-gray-800 dark:text-white mb-1.5">${q.q}</p>
          <p class="text-[11px] text-gray-500 dark:text-slate-400 leading-relaxed"><span class="font-bold text-amber-600 dark:text-amber-400">Answer outline:</span> ${q.answer_outline}</p>
        </div>
      `).join('');

      const tenMarkHtml = (u.important_questions?.ten_mark || []).map(q => `
        <div class="p-3 rounded-xl bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-900/50">
          <div class="flex items-center gap-1.5 mb-1">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-purple-600 text-white">10 Marks</span>
          </div>
          <p class="text-xs font-semibold text-gray-800 dark:text-white mb-1.5">${q.q}</p>
          <p class="text-[11px] text-gray-500 dark:text-slate-400 leading-relaxed"><span class="font-bold text-purple-600 dark:text-purple-400">Answer outline:</span> ${q.answer_outline}</p>
        </div>
      `).join('');

      const formulasHtml = (u.must_know_formulas || []).length > 0 ? `
        <div class="flex flex-wrap gap-2 pt-1">
          ${(u.must_know_formulas).map(f => `
            <span class="px-3 py-1 rounded-full text-[11px] font-mono bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-slate-300 border border-gray-200 dark:border-slate-700">📐 ${f}</span>
          `).join('')}
        </div>
      ` : '';

      return `
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm space-y-4">
          <div class="flex items-center gap-3">
            <span class="w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 font-black text-sm flex items-center justify-center shrink-0">${u.unit_no}</span>
            <div>
              <h4 class="font-black text-sm sm:text-base text-gray-900 dark:text-white">${u.unit_title || 'Unit ' + u.unit_no}</h4>
              <p class="text-[11px] text-gray-500 dark:text-slate-400">${(u.key_topics || []).join(' • ')}</p>
            </div>
          </div>
          ${formulasHtml}
          ${mcqs ? `<div class="space-y-2"><div class="text-[10px] font-black uppercase tracking-wider text-blue-600 dark:text-blue-400">🎯 High-Probability MCQs</div><div class="space-y-2">${mcqs}</div></div>` : ''}
          ${fiveMarkHtml ? `<div class="space-y-2"><div class="text-[10px] font-black uppercase tracking-wider text-amber-600 dark:text-amber-400">📝 5-Mark Questions</div><div class="space-y-2">${fiveMarkHtml}</div></div>` : ''}
          ${tenMarkHtml ? `<div class="space-y-2"><div class="text-[10px] font-black uppercase tracking-wider text-purple-600 dark:text-purple-400">📖 10-Mark Questions</div><div class="space-y-2">${tenMarkHtml}</div></div>` : ''}
        </div>
      `;
    }).join('');

    // Day-by-day schedule
    const daysHtml = (tracks[0]?.days || []).map(d => `
      <div class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400">${d.day}</span>
            <span class="text-xs text-gray-500 font-semibold">${d.hours} Hours Target</span>
          </div>
          <h4 class="font-bold text-sm sm:text-base text-gray-900 dark:text-white">${d.focus}</h4>
          <ul class="text-xs text-gray-600 dark:text-slate-400 space-y-0.5 pt-1">
            ${(d.tasks || []).map(t => `<li>• ${t}</li>`).join('')}
          </ul>
        </div>
        <div class="sm:text-right shrink-0 p-3 rounded-xl bg-gray-50 dark:bg-slate-800/80 border border-gray-100 dark:border-slate-700 text-xs">
          <span class="text-[10px] text-gray-400 font-bold uppercase block">Milestone Goal:</span>
          <span class="font-bold text-emerald-600 dark:text-emerald-400">${d.checkpoint}</span>
        </div>
      </div>
    `).join('');

    container.innerHTML = `
      <div id="printable-study-material" class="space-y-8 animate-fade-in-up">

        <!-- Header -->
        <div class="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30 p-5 rounded-2xl border border-emerald-200 dark:border-emerald-800 flex items-start justify-between gap-4">
          <div>
            <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">9+ CGPA Strategy Roadmap</span>
            <h2 class="text-lg font-black text-gray-900 dark:text-white mt-1">${data.target_goal || '9+ CGPA Master Plan'}</h2>
            <p class="text-xs text-gray-500 dark:text-slate-400 mt-1">Unit-wise study structure • High-yield important questions • 7-Day intensive schedule</p>
          </div>
          ${aiGenerated ? '<span class="px-3 py-1.5 rounded-full text-[11px] font-black bg-gradient-to-r from-purple-500 to-pink-500 text-white shrink-0">✨ AI Generated</span>' : '<span class="px-3 py-1 rounded-full text-[11px] font-bold bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-slate-300 shrink-0">📚 Subject-Specific</span>'}
        </div>

        <!-- Exam Strategy -->
        ${strategy ? `<div class="space-y-3"><h3 class="text-sm font-black text-gray-900 dark:text-white">🎓 LPU Exam Strategy</h3>${strategyHtml}</div>` : ''}

        <!-- Units with Important Questions -->
        ${units.length > 0 ? `
          <div class="space-y-4">
            <h3 class="text-sm font-black text-gray-900 dark:text-white">📚 Unit-wise Study Plan & Important Questions</h3>
            ${unitsHtml}
          </div>
        ` : ''}

        <!-- 7-Day Schedule -->
        <div class="space-y-3">
          <h3 class="text-sm font-black text-gray-900 dark:text-white">📅 ${tracks[0]?.track_name || '7-Day Intensive Sprint'}</h3>
          ${daysHtml}
        </div>

      </div>
    `;
}

window.launchSlideProjector = async function() {
  if (!window.currentLoadedSlideDeck) return;
  try {
    const res = await fetch('/api/export-slides', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(window.currentLoadedSlideDeck)
    });
    const html = await res.text();
    const win = window.open('', '_blank');
    if (win) {
      win.document.write(html);
      win.document.close();
    } else {
      alert('Please allow popups to launch fullscreen presentation projector.');
    }
  } catch (e) {
    alert('Failed to launch slide presentation.');
  }
};

window.launchSubjectProjector = async function(code) {
  const pm = window.PaywallManager;
  const hasAccess = pm && pm.hasSubjectAccess(code);

  if (!hasAccess) {
    if (pm) {
      pm.openCheckoutModal('subject_pass_49', code);
      return;
    }
  }

  try {
    const res = await fetch(`/api/subject/${code}/presentation`);
    if (!res.ok) throw new Error('Failed to fetch presentation slides');
    const deck = await res.json();
    window.currentLoadedSlideDeck = deck;

    const exportRes = await fetch('/api/export-slides', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(deck)
    });
    const html = await exportRes.text();
    const win = window.open('', '_blank');
    if (win) {
      win.document.write(html);
      win.document.close();
    } else {
      alert('Please allow popups to launch fullscreen presentation projector.');
    }
  } catch (e) {
    alert(`Could not launch presentation: ${e.message}`);
  }
};

window.loadSubjectIntoExamGenerator = function(code) {
  if (!code) {
    switchTab('tab-generate');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return;
  }
  const cleanCode = code.toUpperCase().trim();
  const subjSelect = document.getElementById('subject-select');
  if (subjSelect) {
    let found = false;
    for (let i = 0; i < subjSelect.options.length; i++) {
      if (subjSelect.options[i].value.toUpperCase() === cleanCode) {
        subjSelect.selectedIndex = i;
        subjSelect.dispatchEvent(new Event('change'));
        found = true;
        break;
      }
    }
    if (!found) {
      const match = (window.allAvailableSubjects || []).find(s => s.code.toUpperCase() === cleanCode);
      const title = match ? (match.name || match.title || 'Course Material') : 'Course Material';
      const opt = document.createElement('option');
      opt.value = cleanCode;
      opt.setAttribute('data-title', title);
      opt.textContent = `${cleanCode} — ${title}`;
      subjSelect.prepend(opt);
      subjSelect.selectedIndex = 0;
      subjSelect.dispatchEvent(new Event('change'));
    }
  }
  switchTab('tab-generate');
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// ── Custom Subject Modal Logic ────────────────────────────────────────
function setupCustomSubjectModal() {
  const modal = document.getElementById('custom-subject-modal');
  const openBtn = document.getElementById('open-custom-subject-btn');
  const closeBtn = document.getElementById('close-custom-subject-modal');
  const form = document.getElementById('custom-subject-form');

  if (openBtn && modal) {
    openBtn.addEventListener('click', () => modal.showModal());
  }
  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => modal.close());
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const code = document.getElementById('custom-code-input')?.value.trim();
      const name = document.getElementById('custom-name-input')?.value.trim();
      const sem = document.getElementById('custom-sem-input')?.value || 'Sem1';
      const credits = parseInt(document.getElementById('custom-credits-input')?.value || '4');
      const desc = document.getElementById('custom-desc-input')?.value.trim();
      const unitsRaw = document.getElementById('custom-units-input')?.value.trim();

      const units = unitsRaw ? unitsRaw.split('\n').map(u => u.trim()).filter(Boolean) : [
        "Unit 1: Fundamentals & Introduction",
        "Unit 2: Core Concepts & Applications",
        "Unit 3: Advanced Topics",
        "Unit 4: Case Studies & Projects"
      ];

      try {
        const res = await fetch('/api/custom-subject', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            code,
            name,
            semester: sem,
            credits,
            description: desc,
            units
          })
        });

        if (!res.ok) throw new Error('Failed to create custom course');
        modal.close();
        form.reset();
        await loadSubjectsHub();
        alert(`🎉 Custom Subject ${code} created successfully!`);
      } catch (err) {
        alert(err.message || 'Error creating custom subject.');
      }
    });
  }
}

// ── LPU Catalog Loading ───────────────────────────────────────────────
let currentStructure = null;

async function loadPrograms() {
  const select = document.getElementById('program-select');
  if (!select) return;

  try {
    const res = await fetch('/api/programs');
    const programs = await res.json();
    select.innerHTML = programs.map(p => 
      `<option value="${p.id}">${p.name}</option>`
    ).join('');

    select.addEventListener('change', () => loadStructure(select.value));
    // Load structure for default program
    await loadStructure(select.value || 'B. Tech. CSE');
  } catch (e) {
    console.error("Failed to load programs:", e);
  }
}

async function loadStructure(program) {
  const semSelect = document.getElementById('sem-select');

  try {
    const res = await fetch(`/api/structure?program=${encodeURIComponent(program)}`);
    currentStructure = await res.json();

    const semesters = Object.keys(currentStructure);
    if (semSelect) {
      semSelect.innerHTML = semesters.map(s => `<option value="${s}">${s.replace('Sem', 'Semester ')}</option>`).join('');
      semSelect.onchange = () => updateSubjectDropdown(semSelect.value);
      if (semesters.length > 0) {
        updateSubjectDropdown(semesters[0]);
      }
    }
  } catch (e) {
    console.error("Failed to load structure:", e);
  }
}

function updateSubjectDropdown(semester) {
  const subjSelect = document.getElementById('subject-select');
  if (!subjSelect || !currentStructure || !currentStructure[semester]) return;

  const subjects = currentStructure[semester];
  const entries = Object.entries(subjects);

  subjSelect.innerHTML = entries.map(([code, info]) => {
    const cleanCode = code.split('/').pop();
    const title = info.title || 'Course Material';
    return `<option value="${cleanCode}" data-title="${title}">${cleanCode} — ${title}</option>`;
  }).join('');

  subjSelect.onchange = () => updateUnitsDropdown(semester, subjSelect.value);
  if (entries.length > 0) {
    const firstCode = entries[0][0].split('/').pop();
    updateUnitsDropdown(semester, firstCode);
  }
}

function updateUnitsDropdown(semester, subjectCode) {
  const unitSelect = document.getElementById('unit-select');
  if (!unitSelect || !currentStructure || !currentStructure[semester]) return;

  const subjects = currentStructure[semester];
  let info = null;
  for (const [key, val] of Object.entries(subjects)) {
    if (key.endsWith(subjectCode) || key === subjectCode) {
      info = val;
      break;
    }
  }

  const units = (info && info.units && info.units.length > 0)
    ? info.units
    : ["Unit1", "Unit2", "Unit3", "Unit4", "Unit5", "Unit6"];

  unitSelect.innerHTML = units.map(u => `<option value="${u}">${u.replace('Unit', 'Unit ')}</option>`).join('');
}

// ── Form Handlers & File Drag Drop ────────────────────────────────────
function setupFormHandlers() {
  const dropZone = document.getElementById('file-drop-zone');
  const fileInput = document.getElementById('file-upload-input');
  const filePreview = document.getElementById('file-preview-card');
  const fileNameDisplay = document.getElementById('file-name-display');
  const removeFileBtn = document.getElementById('remove-file-btn');
  let selectedFile = null;

  if (dropZone && fileInput) {
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('border-orange-500', 'bg-orange-50/50', 'dark:bg-orange-950/20');
    });

    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('border-orange-500', 'bg-orange-50/50', 'dark:bg-orange-950/20');
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('border-orange-500', 'bg-orange-50/50', 'dark:bg-orange-950/20');
      if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        handleFileSelect(fileInput.files[0]);
      }
    });
  }

  function handleFileSelect(file) {
    selectedFile = file;
    if (filePreview && fileNameDisplay) {
      fileNameDisplay.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
      filePreview.classList.remove('hidden');
    }
  }

  if (removeFileBtn) {
    removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      selectedFile = null;
      if (fileInput) fileInput.value = '';
      if (filePreview) filePreview.classList.add('hidden');
    });
  }

  // Generate Exam Submission
  const generateForm = document.getElementById('generate-exam-form');
  const generateBtn = document.getElementById('generate-exam-btn');
  const loaderContainer = document.getElementById('generation-loader');

  if (generateForm) {
    generateForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const formData = new FormData();
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

      const textVal = document.getElementById('raw-notes-input')?.value.trim();
      if (textVal) formData.append('text_content', textVal);

      const prog = document.getElementById('program-select')?.value || 'B. Tech. CSE';
      const sem = document.getElementById('sem-select')?.value || 'Sem2';
      const subj = document.getElementById('subject-select')?.value || 'CSE101';
      const subjOpt = document.querySelector(`#subject-select option[value="${subj}"]`);
      const subjName = subjOpt ? subjOpt.getAttribute('data-title') : 'Subject Material';
      const unit = document.getElementById('unit-select')?.value || 'Unit1';
      const examType = document.querySelector('input[name="exam_type"]:checked')?.value || 'ete';
      const mcqCount = document.getElementById('mcq-count-input')?.value || 15;
      const diff = document.getElementById('difficulty-select')?.value || 'Mixed';
      const negMarking = document.getElementById('neg-marking-toggle')?.checked ?? true;

      formData.append('program', prog);
      formData.append('semester', sem);
      formData.append('subject_code', subj);
      formData.append('subject_name', subjName);
      formData.append('unit', unit);
      formData.append('exam_type', examType);
      formData.append('mcq_count', mcqCount);
      formData.append('short_count', examType === 'ca' ? 0 : 4);
      formData.append('long_count', examType === 'ca' ? 0 : 2);
      formData.append('difficulty', diff);
      formData.append('negative_marking', negMarking);
      formData.append('fetch_lpuverto_data', true);

      if (PaywallManager.userData.token) {
        formData.append('token', PaywallManager.userData.token);
      }

      // UI Loading state
      if (generateBtn) generateBtn.disabled = true;
      if (loaderContainer) loaderContainer.classList.remove('hidden');

      try {
        const res = await fetch('/api/generate-exam', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Failed to generate exam paper.');
        }

        const paperData = await res.json();
        
        // Load into Simulator
        ExamSimulator.init(paperData);

        // Switch to Simulator Tab
        switchTab('tab-simulator');

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

      } catch (err) {
        alert(err.message || 'Error occurred while generating paper.');
      } finally {
        if (generateBtn) generateBtn.disabled = false;
        if (loaderContainer) loaderContainer.classList.add('hidden');
      }
    });
  }
}

// ── Note Bank Live Search ─────────────────────────────────────────────
function setupNoteBankSearch() {
  const searchInput = document.getElementById('notebank-search-input');
  const resultsContainer = document.getElementById('notebank-results-list');
  let debounceTimeout = null;

  if (!searchInput || !resultsContainer) return;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    const query = searchInput.value.trim();
    if (query.length < 2) {
      resultsContainer.innerHTML = '<p class="text-sm text-gray-400 py-6 text-center">Type at least 2 characters to search LPU course notes...</p>';
      return;
    }

    debounceTimeout = setTimeout(async () => {
      resultsContainer.innerHTML = '<div class="py-6 text-center text-sm text-orange-500 font-medium">Searching AcadAssist course catalog...</div>';
      try {
        const prog = document.getElementById('program-select')?.value || 'B. Tech. CSE';
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&program=${encodeURIComponent(prog)}`);
        const items = await res.json();

        if (items.length === 0) {
          resultsContainer.innerHTML = '<p class="text-sm text-gray-500 py-6 text-center">No matching subjects found in course catalog.</p>';
          return;
        }

        resultsContainer.innerHTML = items.map(item => `
          <div class="p-4 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 shadow-sm flex items-center justify-between gap-4 hover:border-orange-400 transition-all">
            <div class="min-w-0 flex-1">
              <h5 class="font-bold text-gray-900 dark:text-white text-sm sm:text-base truncate">${item.title}</h5>
              <p class="text-xs text-gray-500 dark:text-slate-400 mt-0.5">${item.snippet || 'LPU Academic Course'}</p>
            </div>
            <button onclick="loadSubjectFromNoteBank('${item.title}')" class="shrink-0 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold rounded-lg shadow-sm transition-colors">
              Generate Paper →
            </button>
          </div>
        `).join('');
      } catch (e) {
        resultsContainer.innerHTML = '<p class="text-sm text-red-500 py-4 text-center">Failed to fetch search results.</p>';
      }
    }, 400);
  });
}

window.loadSubjectFromNoteBank = function(title) {
  const match = title.match(/([A-Z]{2,4}\d{3})/i);
  if (match) {
    const code = match[1].toUpperCase();
    loadSubjectIntoExamGenerator(code);
  }
};
