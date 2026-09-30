/**
 * AcadAssist - Academic & Tech Services Hub Manager
 * Services: Website Making, Projects, Reports, Resume, PPT, Thesis, Automations, Custom Services
 * All inquiries dispatch directly to WhatsApp (+91 7719730804) & persist in SQLite Admin DB
 */

const SERVICES_CATALOG = {
  'website': {
    id: 'website',
    name: 'Website Making & Web Development',
    badge: 'Full-Stack & Portfolios',
    icon: '🌐',
    startingPrice: '₹999',
    color: 'from-blue-500 to-indigo-600',
    border: 'border-blue-500/40',
    desc: 'Custom modern websites, student portfolios, full-stack web applications (React, Node, FastAPI), e-commerce stores, and cloud deployments.',
    features: ['Modern Responsive UI (Mobile + Desktop)', 'Free Cloud Hosting Setup (Vercel/Render)', 'Clean Source Code on GitHub', 'Custom Domain Configuration'],
    dynamicFields: [
      { id: 'site_type', label: 'Website Type', type: 'select', options: ['Student Portfolio / Tech Resume Website', 'Full-Stack Web App (DB + Auth + APIs)', 'Landing Page / Startup Showcase', 'E-Commerce / Online Storefront', 'Admin Dashboard / Internal Portal', 'Custom Web Architecture'] },
      { id: 'tech_stack', label: 'Preferred Tech Stack', type: 'select', options: ['React.js + Tailwind CSS', 'HTML5 + CSS3 + Vanilla JavaScript', 'Python (FastAPI / Flask / Django)', 'Node.js + Express + MongoDB/PostgreSQL', 'Next.js 14 / TypeScript', 'No Preference — Recommend Best'] },
      { id: 'pages_count', label: 'Number of Pages', type: 'select', options: ['1 Single Page (Interactive Landing / Portfolio)', '2 to 4 Pages', '5 to 10 Pages', '10+ Multi-Page Application'] },
      { id: 'hosting_needed', label: 'Deployment & Hosting Assistance?', type: 'select', options: ['Yes, deploy on free cloud (Vercel / Netlify / Render)', 'Yes, configure custom domain (.com / .in / .live)', 'No, deliver source code repository only'] }
    ]
  },
  'projects': {
    id: 'projects',
    name: 'Academic & Tech Projects',
    badge: 'Minor / Major / Capstone',
    icon: '💻',
    startingPrice: '₹799',
    color: 'from-emerald-500 to-teal-600',
    border: 'border-emerald-500/40',
    desc: 'Working end-to-end software projects for B.Tech CSE, IT & Engineering. Includes clean code, database, architecture diagrams, and complete viva preparation.',
    features: ['100% Working Code & Setup Guide', 'Complete Architecture & Flow Diagrams', 'Viva Q&A Prep Sheet Included', 'Live Screen-Share Demo if required'],
    dynamicFields: [
      { id: 'project_level', label: 'Project Category / Level', type: 'select', options: ['Minor Project (Sem 3 to 5)', 'Major Capstone Project (Sem 6 to 8)', 'Lab Course Mini-Project', 'Research / Innovation Prototype'] },
      { id: 'project_domain', label: 'Technology Domain', type: 'select', options: ['Artificial Intelligence / Machine Learning / Deep Learning', 'Web Development (MERN / Python / Java Full-Stack)', 'Mobile Application (Flutter / Android Kotlin)', 'Data Science, NLP & Computer Vision', 'Cloud & DevOps (Docker / Kubernetes / Microservices)', 'Cybersecurity & Cryptography', 'IoT / Robotics / Arduino', 'Core DSA & Algorithms (C++ / Java)'] },
      { id: 'viva_support', label: 'Viva Preparation & Walkthrough?', type: 'select', options: ['Yes, include Viva Q&A + Code logic explanation', 'Code & Readme documentation is sufficient'] }
    ]
  },
  'report': {
    id: 'report',
    name: 'Project Reports & Documentation',
    badge: 'IEEE / Blackbook',
    icon: '📑',
    startingPrice: '₹299',
    color: 'from-amber-500 to-orange-600',
    border: 'border-amber-500/40',
    desc: 'Plagiarism-free academic project reports, final Blackbook documentation, software requirement specifications (SRS), and research synopses.',
    features: ['Strict LPU / University Format', 'Plagiarism < 10% Guarantee', 'System Architecture & UML Diagrams', 'Ready-to-Print Word (.docx) & PDF'],
    dynamicFields: [
      { id: 'report_type', label: 'Document Type', type: 'select', options: ['Major Capstone Final Report', 'Minor Project Report', 'Project Synopsis / Proposal', 'Software Requirement Specification (SRS)', 'Summer Internship / Industrial Training Report', 'Research Paper Documentation'] },
      { id: 'page_count', label: 'Estimated Page Count', type: 'select', options: ['10 to 20 Pages (Synopsis / Mini-Report)', '20 to 45 Pages (Standard Project Report)', '45 to 80+ Pages (Complete University Blackbook)', '80+ Pages Extensive Dissertation'] },
      { id: 'formatting_style', label: 'Formatting Standard', type: 'select', options: ['LPU Standard Guidelines (Times New Roman, 1.5 spacing, 1-inch margins)', 'IEEE Standard Two-Column Format', 'Custom University Template'] }
    ]
  },
  'resume': {
    id: 'resume',
    name: 'Professional Resume & ATS CV',
    badge: 'High ATS Score',
    icon: '📄',
    startingPrice: '₹199',
    color: 'from-pink-500 to-rose-600',
    border: 'border-pink-500/40',
    desc: 'Engineered for 90+ ATS screen pass rates. Highlights your technical skills, DSA proficiencies, capstone projects, and achievements to catch recruiter eyes.',
    features: ['ATS-Keyword Optimized Formatting', 'Action-Oriented Metric Bullet Points', 'LaTeX / Word & PDF Formats', 'LinkedIn Profile Optimization Guide'],
    dynamicFields: [
      { id: 'target_role', label: 'Target Job / Internship Role', type: 'select', options: ['Software Development Engineer (SDE / Software Engineer)', 'Frontend / Full-Stack Developer', 'Data Analyst / Data Scientist', 'AI / Machine Learning Engineer', 'Core Engineering (Mechanical / Civil / ECE / EE)', 'Product / Project Management', 'Non-Tech / Consulting / Business Analyst'] },
      { id: 'experience_level', label: 'Experience Level', type: 'select', options: ['College Student / Fresher (Entry Level)', 'Internship Experienced (1 to 2 Internships)', '1 to 2+ Years Working Professional'] },
      { id: 'linkedin_boost', label: 'Include LinkedIn Profile Boost?', type: 'select', options: ['Yes, Resume + Headline, About & Experience optimization', 'Resume only (Word + Print-Ready PDF)'] }
    ]
  },
  'ppt': {
    id: 'ppt',
    name: 'PPT Presentations & Defense Decks',
    badge: 'Defense & Seminar',
    icon: '📊',
    startingPrice: '₹149',
    color: 'from-purple-500 to-violet-600',
    border: 'border-purple-500/40',
    desc: 'High-impact slide decks with sleek typography, custom architecture visuals, and presenter notes for project evaluations, viva defense, or seminars.',
    features: ['Clean Modern Executive Layouts', 'Custom Architecture & Data Visuals', 'Speaker Talking Points for Each Slide', 'Editable PowerPoint (.pptx) & PDF'],
    dynamicFields: [
      { id: 'slide_count', label: 'Number of Slides Needed', type: 'select', options: ['10 to 15 Slides (Standard Evaluation / Seminar)', '15 to 25 Slides (Major Project Defense)', '25 to 40 Slides (Comprehensive Workshop / Paper)', 'Custom Slide Count'] },
      { id: 'presentation_context', label: 'Presentation Context', type: 'select', options: ['Final Capstone / Minor Project Defense', 'Technical Seminar / Classroom Presentation', 'Research Conference Presentation', 'Startup / Hackathon Pitch Deck'] },
      { id: 'speaker_script', label: 'Include Speaker Talking Script?', type: 'select', options: ['Yes, include bullet talking points for each slide', 'Slides visual design only'] }
    ]
  },
  'thesis': {
    id: 'thesis',
    name: 'Research Thesis & Dissertations',
    badge: 'B.Tech / M.Tech / Ph.D.',
    icon: '🎓',
    startingPrice: '₹399',
    color: 'from-cyan-500 to-blue-600',
    border: 'border-cyan-500/40',
    desc: 'Rigorous research thesis support: literature review synthesis, research gaps, methodology formulation, data analysis, and citation formatting (IEEE/APA).',
    features: ['Scopus / IEEE Standard Alignment', 'In-Depth Literature Review & Gap Analysis', 'Plagiarism Control & Formal Tone', 'Complete BibTeX / Reference Indexing'],
    dynamicFields: [
      { id: 'degree_level', label: 'Degree & Program', type: 'select', options: ['B.Tech Honors / Capstone Thesis', 'M.Tech / M.S. Research Dissertation', 'Ph.D. Thesis Chapters / Literature Survey', 'MBA / Management Research Project'] },
      { id: 'scope_required', label: 'Scope of Assistance', type: 'select', options: ['Complete Thesis (Chapters 1 to 5)', 'Literature Review & State-of-the-Art Analysis', 'Research Methodology & Experimental Design', 'Results Interpretation & Discussion Chapter', 'Plagiarism Reduction & Rewriting', 'Journal Research Paper Formatting'] },
      { id: 'citation_format', label: 'Citation Standard', type: 'select', options: ['IEEE Format ([1], [2] bracketed)', 'APA 7th Edition (Author, Year)', 'Harvard Referencing', 'Elsevier / Springer Journal Style'] }
    ]
  },
  'automations': {
    id: 'automations',
    name: 'Automations, Bots & Web Scraping',
    badge: 'Python & Web Bots',
    icon: '⚙️',
    startingPrice: '₹399',
    color: 'from-amber-600 to-yellow-500',
    border: 'border-amber-500/40',
    desc: 'Custom Python automation scripts, web scrapers, data extraction pipelines, Telegram/WhatsApp bots, and automated spreadsheet workflows.',
    features: ['Python Source Code (.py) with Instructions', 'Automated Scheduling / Background Daemon', 'Anti-Bot & Proxy Handling for Scraping', 'Excel / CSV / Database Exporters'],
    dynamicFields: [
      { id: 'automation_type', label: 'Automation Category', type: 'select', options: ['Web Scraping & Data Extraction Pipeline', 'Telegram / Discord / WhatsApp Notification Bot', 'Excel / Google Sheets / CSV Workflow Automation', 'Browser Automation & Form Filler (Selenium / Playwright)', 'REST API Integration & Webhook Sync', 'Desktop Task Automation / File Processing Script'] },
      { id: 'execution_environment', label: 'Target Execution Setup', type: 'select', options: ['Local Python script with 1-click run file', 'Executable (.exe) standalone application', 'Cloud worker / Free continuous deployment'] }
    ]
  },
  'custom': {
    id: 'custom',
    name: 'Custom Services & Urgent Assistance',
    badge: 'On-Demand Help',
    icon: '🧩',
    startingPrice: '₹99',
    color: 'from-fuchsia-500 to-pink-600',
    border: 'border-fuchsia-500/40',
    desc: 'Any custom academic or technical task: urgent bug fixes, assignment solving, EduCode completion, NeoBrowser tasks, or personalized 1-on-1 guidance.',
    features: ['Direct 1-on-1 WhatsApp Communication', 'Urgent 12–24h Turnaround Available', 'Custom Tailored Solutions', 'Fair & Transparent Student Pricing'],
    dynamicFields: [
      { id: 'urgency_tier', label: 'Delivery Urgency', type: 'select', options: ['⚡ Super Urgent (< 24 Hours)', '⏱️ Urgent (24 to 48 Hours)', '📅 Standard (3 to 5 Days)', 'Flexible / Discuss on WhatsApp'] },
      { id: 'custom_type', label: 'Nature of Assistance', type: 'select', options: ['Code Debugging & Error Fixing', 'Assignment / Practical Problem Solving', 'EduCode / NeoBrowser Exam/Lab Prep', '1-on-1 Technical Consultation & Mentoring', 'Other Bespoke Academic Requirement'] }
    ]
  }
};

const ServicesHub = {
  activeServiceKey: 'website',
  WHATSAPP_NUMBER: '7719730804',

  init() {
    this.renderCatalog();
    this.selectService('website', false);
    this.setupListeners();
  },

  setupListeners() {
    // Form submits
    const tabForm = document.getElementById('services-hub-form');
    if (tabForm) {
      tabForm.addEventListener('submit', (e) => this.handleSubmit(e, 'tab'));
    }

    const modalForm = document.getElementById('service-order-form');
    if (modalForm) {
      modalForm.addEventListener('submit', (e) => this.handleSubmit(e, 'modal'));
    }
  },

  renderCatalog() {
    const grid = document.getElementById('services-catalog-grid');
    if (!grid) return;

    grid.innerHTML = Object.values(SERVICES_CATALOG).map(s => `
      <div id="service-card-${s.id}" onclick="ServicesHub.selectService('${s.id}', true)" class="service-catalog-card p-5 sm:p-6 rounded-3xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-orange-500/60 transition-all duration-300 shadow-sm hover:shadow-xl cursor-pointer group flex flex-col justify-between space-y-4 relative overflow-hidden">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-3xl sm:text-4xl p-2.5 rounded-2xl bg-gray-50 dark:bg-slate-800 border border-gray-100 dark:border-slate-700/60 group-hover:scale-110 transition-transform">
              ${s.icon}
            </span>
            <span class="px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-orange-500/10 text-orange-600 dark:text-orange-400 border border-orange-500/20">
              ${s.badge}
            </span>
          </div>

          <div>
            <h4 class="text-base sm:text-lg font-black text-gray-900 dark:text-white group-hover:text-orange-500 transition-colors">
              ${s.name}
            </h4>
            <p class="text-xs text-gray-500 dark:text-slate-400 mt-1 leading-relaxed">
              ${s.desc}
            </p>
          </div>

          <div class="space-y-1.5 pt-2 border-t border-gray-100 dark:border-slate-800 text-[11px] text-gray-600 dark:text-slate-300">
            ${s.features.slice(0, 3).map(f => `
              <div class="flex items-center gap-1.5">
                <span class="text-emerald-500 font-bold">✓</span>
                <span>${f}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="pt-3 border-t border-gray-100 dark:border-slate-800 flex items-center justify-between">
          <div>
            <span class="text-[10px] text-gray-400 uppercase font-semibold block">Starting At</span>
            <span class="text-base font-black text-emerald-600 dark:text-emerald-400">${s.startingPrice}</span>
          </div>
          <button type="button" class="px-4 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-bold text-xs shadow-sm shadow-orange-500/20 transition-all flex items-center gap-1 group-hover:translate-x-0.5">
            <span>Inquire Now →</span>
          </button>
        </div>
      </div>
    `).join('');
  },

  selectService(serviceKey, scrollToForm = true) {
    const s = SERVICES_CATALOG[serviceKey] || SERVICES_CATALOG['website'];
    this.activeServiceKey = s.id;

    // Highlight card
    document.querySelectorAll('.service-catalog-card').forEach(c => {
      c.classList.remove('ring-2', 'ring-orange-500', 'border-orange-500');
    });
    const activeCard = document.getElementById(`service-card-${s.id}`);
    if (activeCard) {
      activeCard.classList.add('ring-2', 'ring-orange-500', 'border-orange-500');
    }

    // Update Form Header & Dynamic Fields
    this.renderFormDynamicFields(s, 'tab');

    // Auto-fill logged in user info if available
    this.autofillUserData('tab');

    if (scrollToForm) {
      const formEl = document.getElementById('services-intake-module');
      if (formEl) {
        formEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  },

  renderFormDynamicFields(service, prefix = 'tab') {
    const titleEl = document.getElementById(`${prefix}-service-form-title`);
    const priceEl = document.getElementById(`${prefix}-service-price-badge`);
    const iconEl = document.getElementById(`${prefix}-service-icon-badge`);
    const categoryInput = document.getElementById(`${prefix}-service-category`);
    const dynamicContainer = document.getElementById(`${prefix}-dynamic-fields-container`);

    if (titleEl) titleEl.textContent = service.name;
    if (priceEl) priceEl.textContent = `Starting at ${service.startingPrice}`;
    if (iconEl) iconEl.textContent = service.icon;
    if (categoryInput) categoryInput.value = service.name;

    if (!dynamicContainer) return;

    if (!service.dynamicFields || !service.dynamicFields.length) {
      dynamicContainer.innerHTML = '';
      return;
    }

    dynamicContainer.innerHTML = `
      <div class="col-span-full mb-1">
        <span class="text-[11px] font-black uppercase tracking-wider text-orange-500 flex items-center gap-1.5">
          <span>⚙️</span>
          <span>${service.name} Custom Specifications</span>
        </span>
      </div>
      ${service.dynamicFields.map(field => `
        <div class="col-span-1">
          <label class="block text-xs font-bold text-gray-700 dark:text-slate-300 mb-1.5">
            ${field.label}
          </label>
          <select id="${prefix}-spec-${field.id}" data-spec-label="${field.label}" class="w-full text-xs p-3 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-900 dark:text-white focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500">
            ${field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
          </select>
        </div>
      `).join('')}
    `;
  },

  autofillUserData(prefix = 'tab') {
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      const nameInput = document.getElementById(`${prefix}-service-name`);
      const phoneInput = document.getElementById(`${prefix}-service-phone`);
      const emailInput = document.getElementById(`${prefix}-service-email`);
      const regInput = document.getElementById(`${prefix}-service-regno`);

      if (nameInput && !nameInput.value && u.name) nameInput.value = u.name;
      if (phoneInput && !phoneInput.value && u.phone) phoneInput.value = u.phone;
      if (emailInput && !emailInput.value && u.email) emailInput.value = u.email;
      if (regInput && !regInput.value && (u.lpu_reg_no || u.registration_number)) {
        regInput.value = u.lpu_reg_no || u.registration_number;
      }
    }
  },

  openModalForService(serviceKey = 'website') {
    const s = SERVICES_CATALOG[serviceKey] || SERVICES_CATALOG['website'];
    const modal = document.getElementById('service-order-modal');
    if (!modal) return;

    this.activeServiceKey = s.id;
    this.renderFormDynamicFields(s, 'modal');
    this.autofillUserData('modal');
    modal.showModal();
  },

  async handleSubmit(e, prefix = 'tab') {
    e.preventDefault();

    const s = SERVICES_CATALOG[this.activeServiceKey] || SERVICES_CATALOG['website'];
    const category = document.getElementById(`${prefix}-service-category`)?.value || s.name;
    const name = document.getElementById(`${prefix}-service-name`)?.value.trim();
    const phone = document.getElementById(`${prefix}-service-phone`)?.value.trim();
    const email = document.getElementById(`${prefix}-service-email`)?.value.trim() || '';
    const regNo = document.getElementById(`${prefix}-service-regno`)?.value.trim() || '';
    const topic = document.getElementById(`${prefix}-service-topic`)?.value.trim() || '';
    const deadline = document.getElementById(`${prefix}-service-deadline`)?.value || '';
    const urgency = document.getElementById(`${prefix}-service-urgency`)?.value || 'Standard';
    const budget = document.getElementById(`${prefix}-service-budget`)?.value.trim() || '';
    const details = document.getElementById(`${prefix}-service-details`)?.value.trim() || '';
    const links = document.getElementById(`${prefix}-service-links`)?.value.trim() || '';

    if (!name || !phone || !details) {
      alert("Please fill in your name, WhatsApp number, and requirements description.");
      return;
    }

    // Collect dynamic specifications
    const specs = [];
    const customSpecs = {};
    if (s.dynamicFields) {
      s.dynamicFields.forEach(f => {
        const input = document.getElementById(`${prefix}-spec-${f.id}`);
        if (input) {
          const val = input.value;
          specs.push({ label: f.label, value: val });
          customSpecs[f.id] = val;
        }
      });
    }

    const submitBtn = document.getElementById(`${prefix}-service-submit-btn`);
    const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>⏳ Recording & Launching WhatsApp...</span>`;
    }

    try {
      // 1. Post to Backend API
      const res = await fetch('/api/services/inquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_category: category,
          student_name: name,
          phone: phone,
          email: email,
          subject_or_topic: topic || `${category} Inquiry`,
          details: details + (links ? `\nReference Links: ${links}` : ''),
          deadline: deadline,
          budget: budget,
          reg_no: regNo,
          urgency: urgency,
          custom_specs: customSpecs
        })
      });

      const data = await res.json();
      const inqId = data.id || 'INQ-' + Date.now().toString().slice(-6);

      // 2. Build Structured WhatsApp Message
      const waMsgLines = [
        `🚀 *NEW ACADASSIST SERVICE INQUIRY* 🚀`,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `🛠️ *Service:* ${category}`,
        `👤 *Student Name:* ${name}`,
        `📱 *WhatsApp:* ${phone}`,
        regNo ? `🎓 *LPU Reg No:* ${regNo}` : null,
        email ? `📧 *Email:* ${email}` : null,
        topic ? `📚 *Course / Topic:* ${topic}` : null,
        `📅 *Expected Deadline:* ${deadline || 'Flexible'} (${urgency})`,
        budget ? `💰 *Target Budget:* ₹${budget}` : null,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `⚙️ *Service Specifications:*`,
        ...specs.map(item => `• *${item.label}:* ${item.value}`),
        `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `📝 *Project Requirements:*`,
        `${details}`,
        links ? `\n🔗 *Drive / GitHub Links:*\n${links}` : null,
        `━━━━━━━━━━━━━━━━━━━━━━━━━━`,
        `📍 *Ref ID:* ${inqId}`,
        `✨ *Sent via AcadAssist Portal (Direct to WhatsApp 7719730804)*`
      ].filter(Boolean);

      const fullWaMessage = waMsgLines.join('\n');
      const waUrl = `https://wa.me/91${this.WHATSAPP_NUMBER}?text=${encodeURIComponent(fullWaMessage)}`;

      // 3. Open WhatsApp directly
      window.open(waUrl, '_blank');

      // 4. Close modal if modal was used
      if (prefix === 'modal') {
        document.getElementById('service-order-modal')?.close();
      }

      // 5. Show Confirmation dialog
      this.showSuccessDialog(name, category, this.WHATSAPP_NUMBER, waUrl, inqId);

      // Reset requirements text if submitted on tab
      const detailsInput = document.getElementById(`${prefix}-service-details`);
      if (detailsInput) detailsInput.value = '';

    } catch (err) {
      console.error("Service inquiry error:", err);
      // Fallback: still open WhatsApp directly
      const fallbackUrl = `https://wa.me/91${this.WHATSAPP_NUMBER}?text=Hi%20AcadAssist!%20I%20want%20to%20inquire%20about%20${encodeURIComponent(category)}.%20My%20name%20is%20${encodeURIComponent(name)}%20(${phone}).%20Details:%20${encodeURIComponent(details)}`;
      window.open(fallbackUrl, '_blank');
      alert(`⚠️ Your request was recorded. Opening WhatsApp directly on +91 ${this.WHATSAPP_NUMBER}.`);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
    }
  },

  showSuccessDialog(name, serviceName, phone, waUrl, inqId) {
    const existing = document.getElementById('service-success-modal');
    if (existing) existing.remove();

    const dialog = document.createElement('dialog');
    dialog.id = 'service-success-modal';
    dialog.className = 'p-0 rounded-3xl bg-white dark:bg-slate-900 text-gray-900 dark:text-white shadow-2xl border border-gray-200 dark:border-slate-800 max-w-md w-full backdrop:bg-black/60 backdrop:backdrop-blur-sm';
    dialog.innerHTML = `
      <div class="p-6 sm:p-8 space-y-5 text-center">
        <div class="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto text-3xl shadow-lg shadow-emerald-500/20">
          🚀
        </div>

        <div>
          <span class="px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
            Inquiry Dispatched Successfully!
          </span>
          <h3 class="text-xl font-black text-gray-900 dark:text-white mt-2">
            Order Sent to WhatsApp
          </h3>
          <p class="text-xs text-gray-600 dark:text-slate-300 mt-1">
            Thank you, <strong>${name}</strong>! Your inquiry for <strong>${serviceName}</strong> has been saved and opened directly in WhatsApp with our support team at <strong>+91 ${phone}</strong>.
          </p>
        </div>

        <div class="p-3 rounded-2xl bg-gray-50 dark:bg-slate-800 text-left font-mono text-xs space-y-1 border border-gray-200 dark:border-slate-700">
          <div class="flex justify-between text-gray-500 dark:text-slate-400"><span>Tracking ID:</span> <span class="font-bold text-gray-900 dark:text-white">${inqId}</span></div>
          <div class="flex justify-between text-gray-500 dark:text-slate-400"><span>WhatsApp Desk:</span> <span class="font-bold text-emerald-500">+91 ${phone}</span></div>
          <div class="flex justify-between text-gray-500 dark:text-slate-400"><span>Response Time:</span> <span class="font-bold text-pink-500">&lt; 15 mins</span></div>
        </div>

        <div class="space-y-2 pt-2">
          <a href="${waUrl}" target="_blank" class="block w-full py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/25 transition-all text-center">
            📲 Continue WhatsApp Chat (+91 ${phone}) →
          </a>
          <button onclick="document.getElementById('service-success-modal').close()" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-gray-700 dark:text-slate-300 font-semibold text-xs rounded-xl transition-colors">
            Close &amp; Return to Portal
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);
    dialog.showModal();
  }
};

// Backward compatibility alias for any existing buttons
const ServiceInquiryManager = {
  openInquiryModal(serviceName = 'Handwritten Work', defaultPrice = '₹15/page') {
    // Map string names to keys if possible
    const sLower = serviceName.toLowerCase();
    let key = 'custom';
    if (sLower.includes('web')) key = 'website';
    else if (sLower.includes('project') || sLower.includes('code')) key = 'projects';
    else if (sLower.includes('report') || sLower.includes('typed')) key = 'report';
    else if (sLower.includes('resume') || sLower.includes('cv')) key = 'resume';
    else if (sLower.includes('ppt') || sLower.includes('presentation')) key = 'ppt';
    else if (sLower.includes('thesis') || sLower.includes('dissertation')) key = 'thesis';
    else if (sLower.includes('auto') || sLower.includes('bot') || sLower.includes('scrap')) key = 'automations';

    ServicesHub.openModalForService(key);
  },

  submitInquiry(e) {
    ServicesHub.handleSubmit(e, 'modal');
  }
};

window.ServicesHub = ServicesHub;
window.ServiceInquiryManager = ServiceInquiryManager;

document.addEventListener('DOMContentLoaded', () => {
  ServicesHub.init();
});
