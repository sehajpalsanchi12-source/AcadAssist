/* ================= AcadAssist — Interactivity & Animations ================= */

const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const WA = "https://wa.me/918053122848?text=";

/* ---------- Data ---------- */
const SERVICES = [
  { emoji: "🌐", price: "From ₹999", title: "Website Making", desc: "Portfolios, full-stack web apps, landing pages & cloud deploy." },
  { emoji: "💻", price: "From ₹799", title: "Tech Projects", desc: "Minor/Major/Capstone, AI/ML, Web, App + Viva preparation." },
  { emoji: "📑", price: "From ₹299", title: "Project Reports", desc: "IEEE Blackbooks, SRS, Synopses with < 10% plagiarism." },
  { emoji: "📄", price: "From ₹199", title: "ATS Resume & CV", desc: "90+ ATS score, recruiter-ready tech CV & LinkedIn boost." },
  { emoji: "📊", price: "From ₹149", title: "PPT Slide Decks", desc: "Project defense slides, seminar decks with speaker notes." },
  { emoji: "🎓", price: "From ₹399", title: "Research Thesis", desc: "B.Tech/M.Tech/Ph.D. literature review, methodology & IEEE format." },
  { emoji: "⚙️", price: "From ₹399", title: "Automations & Bots", desc: "Python scripts, web scraping, data pipelines & task bots." },
  { emoji: "🧩", price: "From ₹99", title: "Custom Services", desc: "Urgent bug fixes, assignment solving, EduCode & 1-on-1 help." },
];

const SUBJECTS = [
  { code: "CSE101", name: "Computer Programming" },
  { code: "CSE201", name: "Data Structures & Algorithms" },
  { code: "CSE305", name: "Operating Systems" },
  { code: "CSE307", name: "Database Management Systems" },
  { code: "CSE401", name: "Computer Networks" },
  { code: "CSE451", name: "Machine Learning" },
  { code: "MTH166", name: "Engineering Mathematics-II" },
  { code: "PHY109", name: "Quantum Mechanics & Optics" },
  { code: "PHY110", name: "Physics for Engineers" },
  { code: "ECE131", name: "Analog Electronics" },
  { code: "ECE201", name: "Digital System Design" },
  { code: "HUM201", name: "Professional Ethics" },
  { code: "MEC201", name: "Engineering Mechanics" },
  { code: "CHE111", name: "Engineering Chemistry" },
  { code: "CSE210", name: "Object Oriented Programming (Java)" },
  { code: "CSE340", name: "Design & Analysis of Algorithms" },
  { code: "CSE460", name: "Artificial Intelligence" },
  { code: "CSE470", name: "Cloud Computing" },
  { code: "IT201", name: "Software Engineering" },
  { code: "MTH266", name: "Numerical Analysis" },
];

const YEARS = ["2024", "2023", "2022", "2021"];
const PAPERS = ["End-Term Exam", "Mid-Term Exam", "Continuous Assessment", "Pop Quiz"];

/* =====================================================
   1. Navbar / scroll progress / back-to-top
===================================================== */
const navbar = $("#navbar");
const progress = $("#scrollProgress");
const toTop = $("#toTop");

function onScroll() {
  const y = window.scrollY;
  navbar.classList.toggle("scrolled", y > 40);
  const h = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = (h > 0 ? (y / h) * 100 : 0) + "%";
  toTop.classList.toggle("show", y > 600);
}
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

/* Mobile nav */
const navToggle = $("#navToggle");
const navLinks = $("#navLinks");
navToggle.addEventListener("click", () => {
  navToggle.classList.toggle("open");
  navLinks.classList.toggle("open");
});
$$("#navLinks a").forEach((a) =>
  a.addEventListener("click", () => {
    navToggle.classList.remove("open");
    navLinks.classList.remove("open");
  })
);

/* =====================================================
   2. Cursor glow
===================================================== */
const glow = $("#cursorGlow");
window.addEventListener(
  "pointermove",
  (e) => {
    glow.style.left = e.clientX + "px";
    glow.style.top = e.clientY + "px";
  },
  { passive: true }
);

/* =====================================================
   3. Reveal on scroll
===================================================== */
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add("visible");
        io.unobserve(en.target);
      }
    });
  },
  { threshold: 0.12 }
);
function observeReveals() {
  $$(".reveal").forEach((el) => io.observe(el));
}

/* =====================================================
   4. Animated counters
===================================================== */
const counterIO = new IntersectionObserver(
  (entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target;
      counterIO.unobserve(el);
      const target = +el.dataset.count;
      const suffix = el.dataset.suffix || "";
      const dur = 1600;
      const t0 = performance.now();
      (function tick(now) {
        const p = Math.min((now - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    });
  },
  { threshold: 0.5 }
);
$$(".stat-num").forEach((el) => counterIO.observe(el));

/* =====================================================
   5. Typewriter
===================================================== */
const words = ["Academic Work", "Notes", "MCQs", "Slides", "LPU Exam Prep"];
const tw = $("#typewriter");
let wi = 0, ci = 0, deleting = false;
function typeLoop() {
  const word = words[wi];
  tw.textContent = word.slice(0, ci);
  let delay = deleting ? 45 : 95;
  if (!deleting && ci === word.length) {
    delay = 1800;
    deleting = true;
  } else if (deleting && ci === 0) {
    deleting = false;
    wi = (wi + 1) % words.length;
    delay = 420;
  } else {
    ci += deleting ? -1 : 1;
  }
  setTimeout(typeLoop, delay);
}
typeLoop();

/* =====================================================
   6. Hero particles (canvas)
===================================================== */
(function particles() {
  const canvas = $("#particles");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let w, h, pts = [];

  function resize() {
    w = canvas.width = canvas.offsetWidth;
    h = canvas.height = canvas.offsetHeight;
    const n = Math.min(90, Math.floor((w * h) / 16000));
    pts = Array.from({ length: n }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      r: Math.random() * 1.8 + 0.6,
      hue: Math.random() > 0.5 ? 262 : 189,
    }));
  }
  resize();
  window.addEventListener("resize", resize);

  function frame() {
    ctx.clearRect(0, 0, w, h);
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${p.hue}, 85%, 65%, 0.75)`;
      ctx.fill();

      for (let j = i + 1; j < pts.length; j++) {
        const q = pts[j];
        const dx = p.x - q.x, dy = p.y - q.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < 13000) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `hsla(260, 80%, 70%, ${0.16 * (1 - d2 / 13000)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(frame);
  }
  if (!reduced) frame();
})();

/* =====================================================
   7. 3D tilt cards + magnetic buttons
===================================================== */
$$("[data-tilt]").forEach((card) => {
  card.addEventListener("pointermove", (e) => {
    const r = card.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width;
    const py = (e.clientY - r.top) / r.height;
    card.style.setProperty("--mx", px * 100 + "%");
    card.style.setProperty("--my", py * 100 + "%");
    card.style.transform = `perspective(800px) rotateY(${(px - 0.5) * 10}deg) rotateX(${(0.5 - py) * 10}deg) translateY(-6px)`;
  });
  card.addEventListener("pointerleave", () => {
    card.style.transform = "";
  });
});

$$(".magnetic").forEach((btn) => {
  btn.addEventListener("pointermove", (e) => {
    const r = btn.getBoundingClientRect();
    btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.15}px, ${(e.clientY - r.top - r.height / 2) * 0.25 - 3}px)`;
  });
  btn.addEventListener("pointerleave", () => (btn.style.transform = ""));
});

/* =====================================================
   8. Services grid
===================================================== */
$("#servicesGrid").innerHTML = SERVICES.map(
  (s, i) => `
  <a class="svc reveal delay-${i % 4}" href="${WA}${encodeURIComponent("Hi AcadAssist, I need: " + s.title)}" target="_blank" rel="noopener">
    <div class="svc-emoji">${s.emoji}</div>
    <div class="svc-price">${s.price}</div>
    <h4>${s.title}</h4>
    <p>${s.desc}</p>
    <span class="svc-link">Inquire on WhatsApp →</span>
  </a>`
).join("");

/* =====================================================
   9. PYQ Bank
===================================================== */
const courseSelect = $("#courseSelect");
const pyqResults = $("#pyqResults");

courseSelect.innerHTML = SUBJECTS.map((s) => `<option value="${s.code}">${s.code} — ${s.name}</option>`).join("");

function renderPapers(code) {
  const subj = SUBJECTS.find((s) => s.code === code) || SUBJECTS[0];
  const list = [];
  YEARS.forEach((y) => {
    PAPERS.slice(0, 3).forEach((p, k) => {
      list.push({ y, p, sem: k % 2 ? "Mid Semester" : "End Semester" });
    });
  });
  pyqResults.innerHTML = list
    .map(
      (it, i) => `
    <div class="paper" style="animation-delay:${i * 45}ms">
      <h5>${subj.code} — ${it.p}</h5>
      <span>${it.y} • ${it.sem}</span>
      <span>With marking rubric &amp; model solutions</span>
      <span class="tag">PYQ Repeat: ${55 + ((i * 7) % 40)}%</span>
    </div>`
    )
    .join("");
}
courseSelect.addEventListener("change", () => renderPapers(courseSelect.value));
renderPapers(SUBJECTS[0].code);

/* =====================================================
   10. Study Studio generator
===================================================== */
const studioTabs = $("#studioTabs");
const outputCard = $("#outputCard");
const studioLoader = $("#studioLoader");
const generateBtn = $("#generateBtn");
let activeTab = "notes";

studioTabs.addEventListener("click", (e) => {
  const btn = e.target.closest(".tab");
  if (!btn) return;
  $$(".tab", studioTabs).forEach((t) => t.classList.remove("active"));
  btn.classList.add("active");
  activeTab = btn.dataset.tab;
  generate();
});

const TEMPLATES = {
  notes: (c, u) => `
    <h4>📝 ${c} — ${u} Comprehensive Notes</h4>
    <ul>
      <li><b>Key Concepts:</b> definitions, formulas &amp; derivations aligned to LPU syllabus</li>
      <li><b>Diagrams:</b> labelled figures with exam-point annotations</li>
      <li><b>Solved Examples:</b> previous year numericals with steps</li>
      <li><b>Exam Focus:</b> 5-mark &amp; 10-mark likely questions flagged</li>
    </ul>`,
  cheatsheet: (c, u) => `
    <h4>⚡ ${c} — ${u} One-Night Cheat Sheet</h4>
    <ul>
      <li>All formulas on a single page (printable A4)</li>
      <li>20 must-know definitions with 1-line answers</li>
      <li>Quick-recall mnemonics for theory units</li>
      <li>Last-minute 10-min revision ladder</li>
    </ul>`,
  slides: (c, u) => `
    <h4>📊 ${c} — ${u} Slide Deck</h4>
    <ul>
      <li>18–22 slides with speaker notes</li>
      <li>Animations for procedures &amp; flowcharts</li>
      <li>Title + agenda + summary + Q&A slides</li>
      <li>Editable PPTX export ready</li>
    </ul>`,
  roadmap: (c, u) => `
    <h4>🗺️ ${c} — ${u} Week-by-Week Roadmap</h4>
    <ul>
      <li>Week 1: Foundations + Unit overview</li>
      <li>Week 2: Core theory + practice set A</li>
      <li>Week 3: Problem solving + PYQ drilling</li>
      <li>Week 4: Revision mock + 9+ CGPA strategy</li>
    </ul>`,
};

function generate() {
  const course = $("#studioCourse").value;
  const unit = $("#studioUnit").value;
  studioLoader.hidden = false;
  outputCard.style.display = "none";
  setTimeout(() => {
    studioLoader.hidden = true;
    outputCard.style.display = "block";
    outputCard.style.animation = "none";
    void outputCard.offsetWidth;
    outputCard.style.animation = "";
    outputCard.innerHTML = TEMPLATES[activeTab](course.split(" — ")[0], unit);
    if (activeTab === "slides") {
      const btn = document.createElement("button");
      btn.className = "launch-deck";
      btn.type = "button";
      btn.innerHTML = "▶ Launch Interactive Deck";
      btn.addEventListener("click", () => openDeck(course, unit));
      outputCard.appendChild(btn);
    }
  }, 1400);
}
generateBtn.addEventListener("click", generate);

/* =====================================================
   11. Exam Simulator
===================================================== */
let QUESTIONS = [
  {
    q: "Which data structure follows Last-In-First-Out (LIFO) principle?",
    opts: ["Queue", "Stack", "Linked List", "Binary Tree"],
    a: 1,
  },
  {
    q: "Time complexity of binary search on a sorted array of n elements?",
    opts: ["O(n)", "O(n log n)", "O(log n)", "O(1)"],
    a: 2,
  },
  {
    q: "Which keyword is used to inherit a class in Java?",
    opts: ["implements", "inherits", "extends", "super"],
    a: 2,
  },
  {
    q: "In C, which of the following is a valid identifier?",
    opts: ["2name", "int", "my_var", "float$"],
    a: 2,
  },
  {
    q: "What does SQL stand for?",
    opts: ["Structured Query Language", "Simple Query Language", "Sequential Query Logic", "Standard Question Language"],
    a: 0,
  },
  {
    q: "Which scheduling algorithm can cause starvation of long jobs?",
    opts: ["Round Robin", "FCFS", "Shortest Job First", "Multilevel Queue"],
    a: 2,
  },
  {
    q: "The default port number of HTTP is:",
    opts: ["21", "80", "443", "8080"],
    a: 1,
  },
  {
    q: "Which of these is NOT an OOP principle?",
    opts: ["Encapsulation", "Inheritance", "Compilation", "Polymorphism"],
    a: 2,
  },
];

let qIndex = 0;
let answers = Array(QUESTIONS.length).fill(null);
let review = Array(QUESTIONS.length).fill(false);
let visited = Array(QUESTIONS.length).fill(false);
let submitted = false;

const qText = $("#qText");
const qOptions = $("#qOptions");
const qSection = $("#qSection");
const palette = $("#palette");

function renderQuestion() {
  visited[qIndex] = true;
  const q = QUESTIONS[qIndex];
  qSection.textContent =
    qIndex < 6
      ? "SECTION A — MCQ (1 Mark Each)"
      : qIndex < 7
      ? "SECTION B — Conceptual (5 Marks)"
      : "SECTION C — Problem Solving (10 Marks)";
  qText.textContent = `Q${qIndex + 1}. ${q.q}`;
  qOptions.innerHTML = q.opts
    .map(
      (o, i) => `
    <div class="opt ${answers[qIndex] === i ? "selected" : ""}" data-i="${i}" role="button" tabindex="0">
      <span class="key">${"ABCD"[i]}</span><span>${o}</span>
    </div>`
    )
    .join("");
  renderPalette();
  updateTally();
}

function renderPalette() {
  palette.innerHTML = QUESTIONS.map((_, i) => {
    let cls = "";
    if (i === qIndex) cls = "current";
    if (answers[i] !== null) cls = "answered";
    if (review[i]) cls = "review";
    if (review[i] && answers[i] !== null) cls = "review";
    return `<button class="pal-btn ${cls}" data-q="${i}">${i + 1}</button>`;
  }).join("");
}

function updateTally() {
  const answered = answers.filter((a) => a !== null).length;
  $("#tAnswered").textContent = answered;
  $("#tUnanswered").textContent = QUESTIONS.length - answered;
  $("#tReview").textContent = review.filter(Boolean).length;
  $("#tUnvisited").textContent = visited.filter((v) => !v).length;
}

qOptions.addEventListener("click", (e) => {
  const opt = e.target.closest(".opt");
  if (!opt || submitted) return;
  answers[qIndex] = +opt.dataset.i;
  renderQuestion();
});
qOptions.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    const opt = e.target.closest(".opt");
    if (opt) {
      e.preventDefault();
      opt.click();
    }
  }
});

palette.addEventListener("click", (e) => {
  const b = e.target.closest(".pal-btn");
  if (!b) return;
  qIndex = +b.dataset.q;
  renderQuestion();
});

$("#nextBtn").addEventListener("click", () => {
  qIndex = (qIndex + 1) % QUESTIONS.length;
  renderQuestion();
});
$("#prevBtn").addEventListener("click", () => {
  qIndex = (qIndex - 1 + QUESTIONS.length) % QUESTIONS.length;
  renderQuestion();
});
$("#markBtn").addEventListener("click", () => {
  review[qIndex] = !review[qIndex];
  renderPalette();
  updateTally();
});

$("#submitExam").addEventListener("click", () => {
  if (submitted) return;
  submitted = true;
  const correct = QUESTIONS.reduce((n, q, i) => n + (answers[i] === q.a ? 1 : 0), 0);
  // show correctness on current question
  const opts = $$(".opt", qOptions);
  opts.forEach((o, i) => {
    if (i === QUESTIONS[qIndex].a) o.classList.add("correct");
    else if (answers[qIndex] === i) o.classList.add("wrong");
  });
  const box = $("#examResult");
  box.hidden = false;
  box.innerHTML = `<b>${correct} / ${QUESTIONS.length}</b>MCQ score — ${Math.round((correct / QUESTIONS.length) * 15)} / 15 marks in Section A.`;
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

/* Timer — 15:00 countdown */
let secondsLeft = 15 * 60;
const timerEl = $("#timerValue");
const timerBox = $("#examTimer");
setInterval(() => {
  if (submitted || secondsLeft <= 0) return;
  secondsLeft--;
  const m = String(Math.floor(secondsLeft / 60)).padStart(2, "0");
  const s = String(secondsLeft % 60).padStart(2, "0");
  timerEl.textContent = `${m}:${s}`;
  if (secondsLeft <= 60) timerBox.classList.add("danger");
  if (secondsLeft === 0) $("#submitExam").click();
}, 1000);

function resetExam() {
  answers = Array(QUESTIONS.length).fill(null);
  review = Array(QUESTIONS.length).fill(false);
  visited = Array(QUESTIONS.length).fill(false);
  qIndex = 0;
  submitted = false;
  secondsLeft = 15 * 60;
  timerBox.classList.remove("danger");
  $("#examResult").hidden = true;
  renderQuestion();
}

/* =====================================================
   11b. AI question generation
===================================================== */
const AI_PROVIDERS = {
  groq: { kind: "openai", url: "https://api.groq.com/openai/v1/chat/completions", model: "llama-3.3-70b-versatile" },
  gemini: { kind: "gemini", url: "https://generativelanguage.googleapis.com/v1beta/models", model: "gemini-2.0-flash" },
  openai: { kind: "openai", url: "https://api.openai.com/v1/chat/completions", model: "gpt-4o-mini" },
  openrouter: { kind: "openai", url: "https://openrouter.ai/api/v1/chat/completions", model: "meta-llama/llama-3.3-70b-instruct:free" },
  custom: { kind: "openai", url: "", model: "" },
};

const aiCfg = JSON.parse(localStorage.getItem("aa_ai_cfg") || "null") || { provider: "groq", key: "", model: "", baseUrl: "" };
const aiStatus = $("#aiStatus");

function setAiStatus(msg, cls) {
  aiStatus.hidden = false;
  aiStatus.className = "ai-status " + (cls || "");
  aiStatus.innerHTML = cls === "working" ? `<span class="spinner"></span>${msg}` : msg;
}

function syncAiForm() {
  $("#aiProvider").value = aiCfg.provider;
  $("#aiKey").value = aiCfg.key;
  $("#aiModel").value = aiCfg.model || "";
  $("#aiBaseUrl").value = aiCfg.baseUrl || "";
  $("#aiCustomWrap").hidden = aiCfg.provider !== "custom";
}
syncAiForm();

$("#aiSettingsToggle").addEventListener("click", () => {
  const box = $("#aiSettings");
  box.hidden = !box.hidden;
});
$("#aiProvider").addEventListener("change", (e) => {
  $("#aiCustomWrap").hidden = e.target.value !== "custom";
});
$("#aiSave").addEventListener("click", () => {
  aiCfg.provider = $("#aiProvider").value;
  aiCfg.key = $("#aiKey").value.trim();
  aiCfg.model = $("#aiModel").value.trim();
  aiCfg.baseUrl = $("#aiBaseUrl").value.trim();
  localStorage.setItem("aa_ai_cfg", JSON.stringify(aiCfg));
  setAiStatus("✅ Settings saved in this browser.", "ok");
});

function buildPrompt() {
  const subject = $("#aiSubject").value.trim() || "General engineering fundamentals";
  const notes = $("#aiNotes").value.trim();
  const count = Math.min(15, Math.max(3, +$("#aiCount").value || 8));
  const diff = $("#aiDiff").value;
  return `You are an exam question author for Lovely Professional University (LPU).\n` +
    `Create exactly ${count} multiple-choice questions on: ${subject}.\n` +
    `Difficulty: ${diff}.${notes ? ` Base them on these notes:\n---\n${notes}\n---` : ""}\n` +
    `Rules: each question has ONE correct answer, 4 plausible options, university exam style.\n` +
    `Return ONLY valid JSON (no markdown fences) in this exact shape:\n` +
    `{"questions":[{"q":"question text","opts":["a","b","c","d"],"a":0}]}`;
}

function extractJson(text) {
  const cleaned = text.replace(/```json|```/g, "").trim();
  const start = cleaned.indexOf("{");
  const end = cleaned.lastIndexOf("}");
  if (start === -1 || end === -1) throw new Error("No JSON found in model response");
  return JSON.parse(cleaned.slice(start, end + 1));
}

function validateQuestions(raw) {
  const arr = Array.isArray(raw) ? raw : raw.questions;
  if (!Array.isArray(arr) || !arr.length) throw new Error("Model returned no questions");
  const clean = arr
    .filter((q) => q && typeof q.q === "string" && Array.isArray(q.opts) && q.opts.length >= 2)
    .slice(0, 15)
    .map((q) => ({
      q: q.q.trim(),
      opts: q.opts.slice(0, 4).map((o) => String(o)),
      a: Math.min(3, Math.max(0, +q.a || 0)),
    }));
  clean.forEach((q) => { while (q.opts.length < 4) q.opts.push("—"); });
  if (!clean.length) throw new Error("Questions failed validation");
  return clean;
}

async function callAI(prompt) {
  const provider = aiCfg.provider;
  const p = AI_PROVIDERS[provider];
  const key = aiCfg.key;
  if (!key) throw new Error("No API key — open ⚙ API Settings and paste your key first.");
  const model = aiCfg.model || p.model;

  if (p.kind === "gemini") {
    const url = `${aiCfg.baseUrl || p.url}/${model}:generateContent?key=${encodeURIComponent(key)}`;
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { responseMimeType: "application/json", temperature: 0.7 },
      }),
    });
    if (!res.ok) throw new Error(`Gemini API ${res.status}: ${(await res.text()).slice(0, 160)}`);
    const data = await res.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || "";
  }

  const url = provider === "custom" ? aiCfg.baseUrl.replace(/\/$/, "") + "/chat/completions" : p.url;
  if (!url.startsWith("http")) throw new Error("Custom Base URL missing in settings.");
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model,
      temperature: 0.7,
      messages: [
        { role: "system", content: "You output only strict JSON. No markdown, no commentary." },
        { role: "user", content: prompt },
      ],
    }),
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${(await res.text()).slice(0, 160)}`);
  const data = await res.json();
  return data.choices?.[0]?.message?.content || "";
}

$("#aiGenerate").addEventListener("click", async () => {
  const btn = $("#aiGenerate");
  const subject = $("#aiSubject").value.trim();
  if (!subject) {
    setAiStatus("⚠ Enter a subject or topic first (e.g. CSE101 Unit 3: Trees).", "err");
    return;
  }
  btn.disabled = true;
  btn.style.opacity = 0.6;
  setAiStatus("Generating questions… this takes a few seconds.", "working");
  try {
    const text = await callAI(buildPrompt());
    const parsed = validateQuestions(extractJson(text));
    QUESTIONS = parsed;
    resetExam();
    $("#examCourse").innerHTML = `${subject}<span class="src-badge">🤖 AI-GENERATED</span>`;
    setAiStatus(`✅ Loaded ${parsed.length} AI questions — timer reset, answer below!`, "ok");
    $("#examApp").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    setAiStatus(`❌ ${err.message}`, "err");
  } finally {
    btn.disabled = false;
    btn.style.opacity = 1;
  }
});
const searchInput = $("#searchInput");
const searchResults = $("#searchResults");
const POPULAR = ["MTH166", "PHY109", "CSE101", "ECE131", "CSE201"];

$("#popularChips").innerHTML = POPULAR.map(
  (c) => `<button class="chip" data-code="${c}">${c}</button>`
).join("");

$("#popularChips").addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  searchInput.value = chip.dataset.code;
  doSearch();
});

function doSearch() {
  const q = searchInput.value.trim().toLowerCase();
  if (!q) {
    searchResults.innerHTML = `<p class="muted">Type a subject code or name above to browse course resources…</p>`;
    return;
  }
  const hits = SUBJECTS.filter(
    (s) => s.code.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)
  );
  if (!hits.length) {
    searchResults.innerHTML = `<p class="muted">No match for "<b>${searchInput.value}</b>" — try MTH166, CSE101, Physics…</p>`;
    return;
  }
  searchResults.innerHTML = hits
    .map(
      (s, i) => `
    <div class="res-card" style="animation-delay:${i * 50}ms">
      <div>
        <span class="res-code">${s.code}</span>
        <span class="res-name"> — ${s.name}</span>
      </div>
      <a class="btn btn-ghost" href="${WA}${encodeURIComponent("Hi AcadAssist, I need notes for " + s.code + " — " + s.name)}" target="_blank" rel="noopener">Get Notes →</a>
    </div>`
    )
    .join("");
}
searchInput.addEventListener("input", doSearch);

/* Copy UPI ID */
$("#copyUpi").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText("mk9817223@okicici");
    $("#copyUpi").textContent = "Copied ✓";
    setTimeout(() => ($("#copyUpi").textContent = "Copy"), 1800);
  } catch {
    $("#copyUpi").textContent = "mk9817223@okicici";
  }
});

/* Payment form */
$("#payForm").addEventListener("submit", (e) => {
  e.preventDefault();
  $("#paySuccess").hidden = false;
  e.target.reset();
});

/* =====================================================
   13b. Interactive slide deck with diagrams
===================================================== */
const deckEl = $("#deck");
const deckStage = $("#deckStage");
let deckSlides = [];
let deckIdx = 0;

const DIAGRAMS = {
  flow: `
    <div class="diagram-wrap">
      <svg class="diagram-svg" viewBox="0 0 920 150" role="img" aria-label="Program execution flowchart">
        <defs>
          <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#22d3ee" />
          </marker>
        </defs>
        <g class="flow-node" data-t="Source Code" data-d="You write the program in C/C++, Python or Java — a human-readable text file (.c, .py). LPU CSE101 labs start here.">
          <rect x="4" y="45" width="140" height="60" rx="12" />
          <text x="74" y="72" text-anchor="middle">Source Code</text>
          <text x="74" y="91" text-anchor="middle" style="font-size:10px;fill:#9a97b5">.c / .py file</text>
        </g>
        <path class="flow-arrow" d="M150 75 H196" marker-end="url(#ah)" style="animation-delay:.1s" />
        <g class="flow-node" data-t="Compiler / Interpreter" data-d="Translates source into machine-readable form. Compilers (C, C++) build the whole file at once; interpreters (Python) run line by line. A frequent 5-mark question!">
          <rect x="202" y="45" width="160" height="60" rx="12" />
          <text x="282" y="72" text-anchor="middle">Compiler</text>
          <text x="282" y="91" text-anchor="middle" style="font-size:10px;fill:#9a97b5">syntax check + translate</text>
        </g>
        <path class="flow-arrow" d="M368 75 H414" marker-end="url(#ah)" style="animation-delay:.5s" />
        <g class="flow-node" data-t="Object Code" data-d="The compiler emits intermediate object code (.o / .obj) — machine instructions, but with unresolved external references (e.g. printf).">
          <rect x="420" y="45" width="140" height="60" rx="12" />
          <text x="490" y="72" text-anchor="middle">Object Code</text>
          <text x="490" y="91" text-anchor="middle" style="font-size:10px;fill:#9a97b5">.o / .obj</text>
        </g>
        <path class="flow-arrow" d="M566 75 H612" marker-end="url(#ah)" style="animation-delay:.9s" />
        <g class="flow-node" data-t="Linker" data-d="Combines your object code with library files (stdio.h functions) into one executable. 'Undefined reference' errors come from a failed link step.">
          <rect x="618" y="45" width="120" height="60" rx="12" />
          <text x="678" y="72" text-anchor="middle">Linker</text>
          <text x="678" y="91" text-anchor="middle" style="font-size:10px;fill:#9a97b5">merge libs</text>
        </g>
        <path class="flow-arrow" d="M744 75 H790" marker-end="url(#ah)" style="animation-delay:1.3s" />
        <g class="flow-node" data-t="Executable" data-d="The final binary (a.out / .exe). The OS loader loads it into RAM and the CPU begins the fetch–decode–execute cycle.">
          <rect x="796" y="45" width="120" height="60" rx="12" />
          <text x="856" y="72" text-anchor="middle">Executable</text>
          <text x="856" y="91" text-anchor="middle" style="font-size:10px;fill:#9a97b5">a.out / .exe</text>
        </g>
        <text x="460" y="140" text-anchor="middle" class="flow-label">click any block to inspect its role ↗</text>
      </svg>
      <div class="diagram-info" data-default="🖱️ Click a block above to see what each stage does — this pipeline is a repeat 5-mark question in CSE101."><b>Execution pipeline</b> — click a block to explore.</div>
    </div>`,

  pyramid: `
    <div class="diagram-wrap">
      <svg class="diagram-svg" viewBox="0 0 660 330" role="img" aria-label="Memory hierarchy pyramid">
        <g class="pyr-layer" data-t="Registers" data-d="Tiny (32–64 bit) storage inside the CPU. Fastest of all — hold the current instruction operands. Accessed in &lt;1 ns.">
          <polygon points="290,20 370,20 416,70 244,70" fill="rgba(34,211,238,.85)" />
          <text x="330" y="52" text-anchor="middle">Registers</text>
        </g>
        <g class="pyr-layer" data-t="L1 / L2 Cache" data-d="SRAM sitting on/near the CPU. Holds hot data from RAM. L1 ≈ 1 ns, L2 ≈ 4 ns. Cache-hit ratio is a favourite exam numerical.">
          <polygon points="236,76 424,76 470,126 190,126" fill="rgba(103,232,249,.8)" />
          <text x="330" y="106" text-anchor="middle">L1 / L2 Cache</text>
        </g>
        <g class="pyr-layer" data-t="RAM (Main Memory)" data-d="DRAM that stores running programs &amp; variables. Volatile — contents vanish on power-off. ~100 ns access; 8–16 GB typical.">
          <polygon points="184,132 476,132 522,182 138,182" fill="rgba(167,139,250,.85)" />
          <text x="330" y="162" text-anchor="middle">RAM (Main Memory)</text>
        </g>
        <g class="pyr-layer" data-t="SSD Storage" data-d="Non-volatile flash storage for OS, files &amp; programs. ~100× slower than RAM but 1000× faster than HDD. Page faults fetch data from here.">
          <polygon points="132,188 528,188 574,238 86,238" fill="rgba(244,114,182,.8)" />
          <text x="330" y="218" text-anchor="middle">SSD Storage</text>
        </g>
        <g class="pyr-layer" data-t="HDD / Archive" data-d="Slowest, cheapest, highest capacity — magnetic disks &amp; backups. Storage pyramid trade-off: speed ↓ as capacity ↑ and cost-per-GB ↓.">
          <polygon points="80,244 580,244 626,294 34,294" fill="rgba(251,191,36,.85)" />
          <text x="330" y="274" text-anchor="middle">HDD / Archive</text>
        </g>
        <text x="330" y="322" text-anchor="middle" class="flow-label">fastest &amp; costliest ↑  ·  slowest &amp; cheapest ↓  — hover a layer</text>
        <text x="20" y="165" transform="rotate(-90 20 165)" class="flow-label" text-anchor="middle">FASTER →</text>
        <text x="640" y="165" transform="rotate(90 640 165)" class="flow-label" text-anchor="middle">BIGGER →</text>
      </svg>
      <div class="diagram-info" data-default="🖱️ Hover any layer — memory hierarchy is guaranteed MCQ material for MTH/PHY/CSE papers."><b>Memory hierarchy</b> — hover a layer to explore.</div>
    </div>`,

  layers: `
    <div class="diagram-wrap">
      <svg class="diagram-svg" viewBox="0 0 700 270" role="img" aria-label="Layered system architecture">
        <g class="layer-block" data-t="Application Software" data-d="User-facing programs: browsers, editors, your LPU lab apps. They never touch hardware directly — they ask the OS instead (system calls).">
          <rect x="60" y="20" width="580" height="62" rx="14" fill="rgba(139,92,246,.85)" />
          <text x="350" y="57" text-anchor="middle">Application Software</text>
        </g>
        <path d="M350 88 V112" stroke="#22d3ee" stroke-width="2.5" marker-end="url(#ah2)" />
        <defs>
          <marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#22d3ee" />
          </marker>
        </defs>
        <g class="layer-block" data-t="Operating System" data-d="The resource manager: process scheduling, memory allocation, file system, device drivers. Abstraction between apps and bare metal — deadlock &amp; scheduling are 10-mark favourites.">
          <rect x="60" y="116" width="580" height="62" rx="14" fill="rgba(34,211,238,.85)" />
          <text x="350" y="153" text-anchor="middle">Operating System</text>
        </g>
        <path d="M350 184 V208" stroke="#22d3ee" stroke-width="2.5" marker-end="url(#ah2)" />
        <g class="layer-block" data-t="Hardware" data-d="Physical layer: CPU, RAM, disk, I/O devices. Machine instructions execute here — fetch, decode, execute cycle.">
          <rect x="60" y="212" width="580" height="52" rx="14" fill="rgba(244,114,182,.85)" />
          <text x="350" y="243" text-anchor="middle">Hardware (CPU · RAM · I/O)</text>
        </g>
        <text x="350" y="96" class="flow-label" text-anchor="middle" style="font-size:10px">system calls ↓</text>
        <text x="350" y="200" class="flow-label" text-anchor="middle" style="font-size:10px">interrupts ↑</text>
      </svg>
      <div class="diagram-info" data-default="🖱️ Click each layer — abstraction is the single most-explained concept across CSE &amp; IT papers."><b>System layers</b> — click each block.</div>
    </div>`,
};

function buildDeck(course, unit) {
  const code = course.split(" — ")[0];
  const name = course.split(" — ")[1] || course;
  return [
    `<div class="slide-kicker">Interactive Study Deck · LPU-aligned</div>
     <div class="slide-hero-mark">⚡</div>
     <h2 class="slide-h">${name}</h2>
     <p class="slide-sub">${code} · ${unit} — visually-structured revision with clickable diagrams, exam flags and model-answer cues.</p>
     <div class="slide-cta"><span class="btn btn-ghost btn-small">Press → to begin</span></div>`,

    `<div class="slide-kicker">Slide 2 · Learning Objectives</div>
     <h3 class="slide-h">What you'll master</h3>
     <ul class="slide-bullets">
       <li><b>✦ Core concepts</b> — definitions, formulas and derivations mapped to the LPU syllabus</li>
       <li><b>✦ Diagrams</b> — the labelled figures examiners award marks for</li>
       <li><b>✦ PYQ patterns</b> — which topics repeat across 2021–2024 papers</li>
       <li><b>✦ 5M &amp; 10M answers</b> — structured points that hit the marking rubric</li>
     </ul>`,

    `<div class="slide-kicker">Slide 3 · Core Diagram</div>
     <h3 class="slide-h">Program Execution Pipeline</h3>
     ${DIAGRAMS.flow}`,

    `<div class="slide-kicker">Slide 4 · Core Diagram</div>
     <h3 class="slide-h">Memory Hierarchy</h3>
     ${DIAGRAMS.pyramid}`,

    `<div class="slide-kicker">Slide 5 · Compare</div>
     <h3 class="slide-h">Compiler vs Interpreter</h3>
     <div class="compare">
       <div class="compare-col">
         <h5>⚙️ Compiler (C / C++)</h5>
         <ul>
           <li>Translates the ENTIRE program at once</li>
           <li>Produces a separate object/executable file</li>
           <li>Faster execution — translation done once</li>
           <li>Error list shown together after compilation</li>
         </ul>
         <div class="meter"><span style="--w:88%"></span></div>
       </div>
       <div class="compare-col">
         <h5>🐍 Interpreter (Python)</h5>
         <ul>
           <li>Translates ONE line at a time, executing as it goes</li>
           <li>No separate executable produced</li>
           <li>Slower execution — re-translated every run</li>
           <li>Stops at the FIRST error encountered</li>
         </ul>
         <div class="meter"><span style="--w:62%"></span></div>
       </div>
     </div>
     <div class="diagram-info"><b>Exam tip:</b> “Compiler vs Interpreter” appeared as a 5-mark question in multiple 2022–2024 papers — quote one difference per line, then add the speed/efficiency table.</div>`,

    `<div class="slide-kicker">Slide 6 · Core Diagram</div>
     <h3 class="slide-h">Layered System Architecture</h3>
     ${DIAGRAMS.layers}`,

    `<div class="slide-kicker">Slide 7 · Exam Focus</div>
     <h3 class="slide-h">Where the marks are</h3>
     <div class="slide-grid2">
       <div class="slide-stat"><b>15</b><span>MCQs · 1 mark each</span></div>
       <div class="slide-stat"><b>4</b><span>5-mark conceptual</span></div>
       <div class="slide-stat"><b>2</b><span>10-mark long</span></div>
       <div class="slide-stat"><b>60</b><span>Total marks</span></div>
     </div>
     <div class="diagram-info"><b>Strategy:</b> finish Section A in 20 min → 5-mark answers in 150–250 words with one labelled diagram each → reserve full 25 min for Section C problem-solving.</div>`,

    `<div class="slide-kicker">Slide 8 · Wrap-up</div>
     <h3 class="slide-h">Your revision checklist ✅</h3>
     <ul class="slide-bullets">
       <li>✓ Re-read this deck once tonight — active recall beats re-reading notes</li>
       <li>✓ Attempt the Exam Simulator with fresh AI-generated questions</li>
       <li>✓ Memorise the two diagram slides — draw them in the exam for bonus clarity</li>
       <li>✓ Grab the ₹29 Night Pass for full model answers before tomorrow's paper</li>
     </ul>
     <div class="slide-cta">
       <button class="launch-deck" type="button" onclick="document.querySelector('#deckClose').click();document.querySelector('#exam').scrollIntoView({behavior:'smooth'})">▶ Try the Exam Simulator</button>
     </div>`,
  ];
}

function renderDeckSlide() {
  deckStage.innerHTML = `<div class="deck-slide active">${deckSlides[deckIdx]}</div>`;
  $("#deckCounter").textContent = `${deckIdx + 1} / ${deckSlides.length}`;
  $("#deckBar").style.width = ((deckIdx + 1) / deckSlides.length) * 100 + "%";
  $$(".deck-dot").forEach((d, i) => d.classList.toggle("on", i === deckIdx));
  $("#deckPrev").disabled = deckIdx === 0;
  $("#deckNext").textContent = deckIdx === deckSlides.length - 1 ? "Finish ✓" : "Next →";
}

function openDeck(course, unit) {
  deckSlides = buildDeck(course, unit);
  deckIdx = 0;
  $("#deckTitle").textContent = `${course.split(" — ")[0]} · ${unit}`;
  $("#deckDots").innerHTML = deckSlides
    .map((_, i) => `<button class="deck-dot ${i === 0 ? "on" : ""}" data-i="${i}" aria-label="Slide ${i + 1}"></button>`)
    .join("");
  deckEl.hidden = false;
  document.body.classList.add("deck-open");
  renderDeckSlide();
}

function closeDeck() {
  deckEl.hidden = true;
  document.body.classList.remove("deck-open");
}

function deckGo(delta) {
  const next = deckIdx + delta;
  if (next < 0) return;
  if (next >= deckSlides.length) return closeDeck();
  deckIdx = next;
  renderDeckSlide();
}

$("#deckNext").addEventListener("click", () => deckGo(1));
$("#deckPrev").addEventListener("click", () => deckGo(-1));
$("#deckClose").addEventListener("click", closeDeck);
$("#deckDots").addEventListener("click", (e) => {
  const d = e.target.closest(".deck-dot");
  if (!d) return;
  deckIdx = +d.dataset.i;
  renderDeckSlide();
});

/* diagram element interaction (delegated — slides re-render each time) */
deckStage.addEventListener("click", (e) => {
  const node = e.target.closest(".flow-node, .pyr-layer, .layer-block");
  if (!node) return;
  const svg = node.closest("svg");
  svg.querySelectorAll(".sel").forEach((n) => n.classList.remove("sel"));
  node.classList.add("sel");
  const info = node.closest(".diagram-wrap").querySelector(".diagram-info");
  info.innerHTML = `<b>${node.dataset.t}</b> — ${node.dataset.d}`;
});

/* keyboard navigation */
document.addEventListener("keydown", (e) => {
  if (deckEl.hidden) return;
  if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") { e.preventDefault(); deckGo(1); }
  else if (e.key === "ArrowLeft" || e.key === "PageUp") { e.preventDefault(); deckGo(-1); }
  else if (e.key === "Escape") closeDeck();
});

/* =====================================================
   14. Init reveals (after dynamic content injected)
===================================================== */
observeReveals();
$("#year").textContent = new Date().getFullYear();
