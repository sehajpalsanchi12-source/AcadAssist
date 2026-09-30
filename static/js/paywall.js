/**
 * AcadAssist - Paywall, UPI Payment Gateway (7719730804@ptyes) & Subscription Manager
 * Enforces QR code display and strict payment verification before unlocking next pages.
 */

const PaywallManager = {
  TOKEN_KEY: 'acad_user_pro_token',
  USER_DATA_KEY: 'acad_user_data',
  UPI_DESTINATION: '7719730804@ptyes',
  OFFICIAL_QR_URL: '/static/images/official_paywall_qr.jpg',

  currentPlan: 'free',
  isPro: false,
  targetAction: null,
  _pollInterval: null,
  userData: {
    name: '',
    regNo: '',
    phone: '',
    token: null
  },

  async init() {
    this.loadLocalData();
    await this.verifyStatus();
    this.updateUI();
    this.setupListeners();
  },

  loadLocalData() {
    // Strictly isolate user data: Only associate user data if AuthManager has an authenticated user
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      this.userData.name = u.name || '';
      this.userData.regNo = u.lpu_reg_no || '';
      this.userData.phone = u.phone || '';
      this.userData.token = u.session_token || localStorage.getItem('lpu_verto_pro_token');
    } else {
      this.userData = { name: '', regNo: '', phone: '', token: null };
    }
  },

  async verifyStatus() {
    this.loadLocalData();
    const token = this.userData.token || (window.AuthManager?.currentUser?.session_token);
    if (!token) {
      this.isPro = false;
      this.currentPlan = 'free';
      this.updateUI();
      return;
    }

    try {
      const res = await fetch(`/api/paywall/verify?token=${encodeURIComponent(token)}`);
      const data = await res.json();
      if (data.is_pro) {
        this.isPro = true;
        this.currentPlan = data.plan_id;
      } else {
        this.isPro = false;
        this.currentPlan = 'free';
      }
    } catch (e) {
      console.warn("Could not verify paywall token:", e);
      this.isPro = false;
      this.currentPlan = 'free';
    }
    this.updateUI();
  },

  updateUI() {
    const badge = document.getElementById('user-plan-badge');
    const upgradeNavBtn = document.getElementById('nav-upgrade-btn');
    const proBanner = document.getElementById('pro-active-banner');

    if (this.isPro) {
      if (badge) {
        badge.innerHTML = `<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-sm shadow-pink-500/20">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          ACTIVE PRO PASS
        </span>`;
      }
      if (upgradeNavBtn) upgradeNavBtn.classList.add('hidden');
      if (proBanner) proBanner.classList.remove('hidden');
    } else {
      if (badge) {
        badge.innerHTML = `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-300 border border-gray-200 dark:border-slate-700">
          Mock: ₹29 • Subject: ₹49
        </span>`;
      }
      if (upgradeNavBtn) upgradeNavBtn.classList.remove('hidden');
      if (proBanner) proBanner.classList.add('hidden');
    }
  },

  setupListeners() {
    document.querySelectorAll('[data-open-paywall]').forEach(btn => {
      btn.addEventListener('click', () => {
        const plan = btn.getAttribute('data-plan') || 'mock_test_29';
        const subj = btn.getAttribute('data-subject') || null;
        this.openCheckoutModal(plan, subj);
      });
    });

    const modal = document.getElementById('paywall-modal');
    const closeBtn = document.getElementById('close-paywall-modal');
    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.close());
    }

    const applyCouponBtn = document.getElementById('apply-coupon-btn');
    if (applyCouponBtn) {
      applyCouponBtn.addEventListener('click', () => this.applyCoupon());
    }

    const payForm = document.getElementById('checkout-form');
    if (payForm) {
      payForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.processPayment();
      });
    }
  },

  switchModalPlan(planId) {
    const currentSubj = document.getElementById('checkout-subject-code')?.value || 'ALL';
    this.openCheckoutModal(planId, currentSubj === 'ALL' ? null : currentSubj);
  },

  openCheckoutModal(planId = 'mock_test_29', subjectCode = null, targetAction = null) {
    const modal = document.getElementById('paywall-modal');
    if (!modal) return;

    this.targetAction = targetAction || {
      planId: planId,
      subjectCode: subjectCode,
      type: planId === 'mock_test_29' ? 'mock_test' : (planId === 'subject_pass_49' ? 'subject' : 'general')
    };

    const planTitle = document.getElementById('checkout-plan-title');
    const planPrice = document.getElementById('checkout-plan-price');
    const planInput = document.getElementById('checkout-plan-id');
    const subjInput = document.getElementById('checkout-subject-code');
    const qrImage = document.getElementById('checkout-upi-qr');
    const upiLink = document.getElementById('checkout-upi-app-link');
    const errBox = document.getElementById('checkout-verification-error');

    if (errBox) { errBox.classList.add('hidden'); errBox.textContent = ''; }

    let price = 29;
    let title = 'Authentic LPU Mock Test Simulator Pass (₹29)';
    if (planId === 'subject_pass_49' || planId === 'midterm_mock_49') {
      price = 49;
      title = 'Single Subject Complete Master Pack (₹49)';
    } else if (planId === 'educode_99') {
      price = 99;
      title = 'EduCode Completion Support Pass (₹99)';
    } else if (planId === 'neobrowser_99') {
      price = 99;
      title = 'NeoBrowser Completion Support Pass (₹99)';
    } else if (planId === 'rush24') {
      price = 29;
      title = 'Exam Night Rush Pass (₹29)';
    } else if (planId === 'semester_pro') {
      price = 99;
      title = 'AcadAssist All-Access Semester Pro (₹99)';
    }

    if (subjectCode && subjectCode !== 'ALL') {
      title += ` • ${subjectCode}`;
    }

    if (planInput) planInput.value = planId;
    if (subjInput) subjInput.value = subjectCode || 'ALL';
    if (planTitle) planTitle.textContent = title;
    if (planPrice) planPrice.textContent = `₹${price}`;

    // Update Pill Buttons
    const mockPill = document.getElementById('modal-tab-mock-29');
    const subjPill = document.getElementById('modal-tab-subject-49');
    if (mockPill && subjPill) {
      if (planId === 'mock_test_29' || planId === 'rush24') {
        mockPill.className = 'py-2.5 px-3 rounded-xl font-extrabold text-xs transition-all bg-white dark:bg-slate-900 text-pink-600 dark:text-pink-400 shadow-sm flex items-center justify-center gap-1.5 border border-pink-200 dark:border-pink-800/60';
        subjPill.className = 'py-2.5 px-3 rounded-xl font-bold text-xs transition-all text-gray-600 dark:text-slate-400 hover:text-gray-900 flex items-center justify-center gap-1.5';
      } else {
        subjPill.className = 'py-2.5 px-3 rounded-xl font-extrabold text-xs transition-all bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm flex items-center justify-center gap-1.5 border border-blue-200 dark:border-blue-800/60';
        mockPill.className = 'py-2.5 px-3 rounded-xl font-bold text-xs transition-all text-gray-600 dark:text-slate-400 hover:text-gray-900 flex items-center justify-center gap-1.5';
      }
    }

    // Set official user-uploaded QR code image
    if (qrImage) {
      qrImage.src = this.OFFICIAL_QR_URL;
    }
    if (upiLink) {
      upiLink.href = `upi://pay?pa=${this.UPI_DESTINATION}&pn=AcadAssist&am=${price}.00&cu=INR&tn=${encodeURIComponent(title.slice(0, 30))}`;
    }

    // Autofill user details only if authenticated, otherwise keep cleanly empty
    const nameInp = document.getElementById('checkout-student-name');
    const regInp = document.getElementById('checkout-reg-no');
    const phoneInp = document.getElementById('checkout-phone');
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      if (nameInp) nameInp.value = u.name || '';
      if (regInp) regInp.value = u.lpu_reg_no || '';
      if (phoneInp) phoneInp.value = u.phone || '';
    } else {
      if (nameInp) nameInp.value = '';
      if (regInp) regInp.value = '';
      if (phoneInp) phoneInp.value = '';
    }

    // Reset coupon & UTR
    const couponInput = document.getElementById('coupon-code-input');
    const couponMsg = document.getElementById('coupon-message');
    const utrInput = document.getElementById('checkout-utr-input');
    if (couponInput) couponInput.value = '';
    if (couponMsg) couponMsg.textContent = '';
    if (utrInput) utrInput.value = '';

    modal.showModal();
  },

  copyUpiId() {
    navigator.clipboard.writeText(this.UPI_DESTINATION);
    const feedback = document.getElementById('upi-copy-feedback');
    if (feedback) {
      feedback.textContent = 'Copied to clipboard!';
      setTimeout(() => feedback.textContent = '', 2000);
    }
  },

  async applyCoupon() {
    const input = document.getElementById('coupon-code-input');
    const msg = document.getElementById('coupon-message');
    const planInput = document.getElementById('checkout-plan-id');
    const priceDisplay = document.getElementById('checkout-plan-price');

    const code = input ? input.value.trim() : '';
    const planId = planInput ? planInput.value : 'midterm_mock_49';

    if (!code) {
      if (msg) msg.textContent = 'Please enter a coupon code.';
      return;
    }

    try {
      const res = await fetch('/api/paywall/coupon', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, plan_id: planId })
      });
      const data = await res.json();
      if (data.valid) {
        msg.className = 'text-xs text-green-600 dark:text-green-400 font-semibold mt-1';
        msg.textContent = `🎉 ${data.code} applied! ${data.description}. Final Price: ₹${data.final_price}`;
        if (priceDisplay) priceDisplay.textContent = `₹${data.final_price}`;
      } else {
        msg.className = 'text-xs text-red-500 font-semibold mt-1';
        msg.textContent = data.message || 'Invalid coupon code.';
      }
    } catch (e) {
      if (msg) msg.textContent = 'Failed to validate coupon.';
    }
  },

  async processPayment() {
    const errorBox = document.getElementById('checkout-verification-error');
    if (errorBox) { errorBox.classList.add('hidden'); errorBox.textContent = ''; }

    const planId = document.getElementById('checkout-plan-id')?.value || 'midterm_mock_49';
    const subjectCode = document.getElementById('checkout-subject-code')?.value || 'ALL';
    const coupon = document.getElementById('coupon-code-input')?.value.trim() || null;
    const nameInput = document.getElementById('checkout-student-name')?.value.trim();
    const regInput = document.getElementById('checkout-reg-no')?.value.trim();
    const phoneInput = document.getElementById('checkout-phone')?.value.trim();
    const utrInput = document.getElementById('checkout-utr-input')?.value.trim();
    const method = document.querySelector('input[name="payment_method"]:checked')?.value || 'upi';

    // Required details validation
    if (!nameInput) {
      this.showCheckoutError('Please enter your Full Name.');
      return;
    }
    if (!regInput) {
      this.showCheckoutError('Please enter your LPU Registration Number.');
      return;
    }

    // UTR is optional — if not provided, admin will verify from Paytm dashboard
    // Only enforce if coupon reduces price to zero (skip payment entirely)

    const submitBtn = document.getElementById('pay-submit-btn');
    const origHtml = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
        <span>Verifying Payment with UPI Switch (${this.UPI_DESTINATION})...</span>
      `;
    }

    try {
      const res = await fetch('/api/paywall/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan_id: planId,
          payment_method: method,
          coupon_code: coupon,
          user_name: nameInput,
          reg_no: regInput,
          phone: phoneInput,
          utr_ref: utrInput,
          user_id: window.AuthManager?.currentUser?.id || null,
          subject_code: subjectCode
        })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        this.showCheckoutError(data.detail || data.message || 'Payment submission failed. Please check your UTR and try again.');
        return;
      }

      if (data.verified === true && data.token) {
        // Coupon / free / test UTR — instant access
        this.userData.token = data.token;
        this.userData.name = nameInput;
        this.userData.regNo = regInput;
        this.isPro = true;
        this.currentPlan = planId;

        localStorage.setItem(this.TOKEN_KEY, data.token);
        localStorage.setItem('lpu_verto_pro_token', data.token);
        localStorage.setItem(this.USER_DATA_KEY, JSON.stringify(this.userData));

        if (window.AuthManager) {
          await window.AuthManager.fetchMe();
          window.AuthManager.renderNavUser();
        }

        this.updateUI();
        this.showVerifiedSuccessView(data, subjectCode, planId);

      } else if (data.pending === true) {
        // Real UPI payment — awaiting admin verification
        // Automatically open WhatsApp with complete payment details to 7719730804
        const waDetails = 
          `*AcadAssist Payment Verification Request*\n` +
          `👤 *Student Name:* ${nameInput}\n` +
          `🎓 *LPU Reg No:* ${regInput}\n` +
          `📱 *Student Mobile:* ${phoneInput || 'N/A'}\n` +
          `📦 *Plan:* ${data.plan || planId}\n` +
          `💰 *Amount:* ₹${data.amount_paid}\n` +
          `🆔 *Tx ID:* ${data.transaction_id}\n` +
          `🔢 *UTR / Reference:* ${data.utr_ref || 'Self-Verification (Check Paytm)'}\n` +
          `📚 *Subject:* ${subjectCode || 'General'}\n` +
          `⏰ *Date/Time:* ${new Date().toLocaleString()}\n\n` +
          `Please check Paytm and approve this transaction in the AcadAssist Admin Dashboard to unlock my access. Thank you!`;

        const waUrl = `https://wa.me/917719730804?text=${encodeURIComponent(waDetails)}`;
        try {
          window.open(waUrl, '_blank');
        } catch (err) {
          console.warn("Auto-popup blocked, user can click button directly:", err);
        }

        this.showPendingVerificationView(data, subjectCode, planId, waUrl);

      } else {
        this.showCheckoutError(data.message || 'Payment could not be processed. Please contact support.');
      }

    } catch (e) {
      this.showCheckoutError('Network error while verifying payment with server.');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = origHtml;
      }
    }
  },

  showCheckoutError(msg) {
    const errorBox = document.getElementById('checkout-verification-error');
    if (errorBox) {
      errorBox.textContent = msg;
      errorBox.classList.remove('hidden');
    } else {
      alert(msg);
    }
  },

  showVerifiedSuccessView(data, subjectCode, planId) {
    const modal = document.getElementById('paywall-modal');
    if (!modal) return;

    modal.innerHTML = `
      <div class="p-6 sm:p-8 space-y-5 text-center animate-fade-in-up max-w-lg mx-auto">
        <div class="w-16 h-16 bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 rounded-full flex items-center justify-center mx-auto shadow-lg shadow-emerald-500/20">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        </div>

        <div>
          <span class="inline-block px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-emerald-500 text-white shadow-sm mb-2">
            ✓ PAYMENT VERIFIED & APPROVED
          </span>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white">Access Unlocked! 🎉</h3>
          <p class="text-xs text-gray-600 dark:text-slate-300 mt-1">
            Your transaction has been approved by Admin. You now have full access to <strong>${data.plan}</strong>.
          </p>
        </div>

        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-2xl border border-gray-200 dark:border-slate-700 text-left text-xs space-y-2 font-mono">
          <div class="flex justify-between"><span class="text-gray-400">Transaction ID:</span> <span class="font-bold text-gray-900 dark:text-white">${data.transaction_id}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">UTR / Ref No:</span> <span class="font-bold text-pink-600 dark:text-pink-400">${data.utr_ref}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Paid to UPI:</span> <span class="font-bold text-gray-700 dark:text-slate-300">${this.UPI_DESTINATION}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Amount Paid:</span> <span class="font-bold text-emerald-600">₹${data.amount_paid}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Status:</span> <span class="font-bold text-emerald-500">VERIFIED & LIVE</span></div>
        </div>

        <button onclick="PaywallManager.unlockAndNavigateNextPage('${planId}', '${subjectCode}')" class="w-full py-4 bg-gradient-to-r from-emerald-500 via-teal-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white font-black text-sm rounded-2xl shadow-xl shadow-emerald-500/25 transition-all flex items-center justify-center gap-2">
          <span>🚀 Continue to Unlocked Page →</span>
        </button>
      </div>
    `;
  },

  unlockAndNavigateNextPage(planId, subjectCode) {
    const modal = document.getElementById('paywall-modal');
    if (modal) modal.close();

    // 1. If currently in the Exam Simulator, unlock all hidden solutions immediately
    if (window.ExamSimulator) {
      window.ExamSimulator.unlockPaperSolutions();
    }

    // 2. Navigate to target unlocked section based on action
    const target = this.targetAction || {};

    if (target.type === 'mock_test' || planId === 'mock_test_29' || planId === 'rush24') {
      const subj = (subjectCode && subjectCode !== 'ALL') ? subjectCode : (target.subjectCode || 'MTH166');
      if (typeof window.startSubjectMockTest === 'function') {
        window.startSubjectMockTest(subj, subj);
      } else if (typeof window.switchTab === 'function') {
        window.switchTab('tab-simulator');
      }
    } else if (target.type === 'download_ppt' && target.subjectCode) {
      window.location.href = `/api/subject/${target.subjectCode}/download-pptx`;
    } else if (target.type === 'subject' || planId === 'subject_pass_49') {
      const subj = (subjectCode && subjectCode !== 'ALL') ? subjectCode : (target.subjectCode || 'MTH166');
      if (typeof window.openPYQForSubject === 'function') {
        window.openPYQForSubject(subj);
      } else if (typeof window.switchTab === 'function') {
        window.switchTab('tab-preloaded');
      }
    } else {
      if (typeof window.switchTab === 'function') {
        window.switchTab('tab-simulator');
      }
    }

    // Reset modal content for next time
    setTimeout(() => {
      window.location.reload();
    }, 1200);
  },

  showPendingVerificationView(txData, subjectCode, planId, waUrl = null) {
    const modal = document.getElementById('paywall-modal');
    if (!modal) return;
    if (this._pollInterval) clearInterval(this._pollInterval);
    const txId = txData.transaction_id || '';
    const utrRef = txData.utr_ref || 'N/A';
    const amount = txData.amount_paid || 0;
    const finalWaUrl = waUrl || `https://wa.me/917719730804?text=${encodeURIComponent(`Hi AcadAssist! I paid ₹${amount} via UPI. UTR: ${utrRef} (TxID: ${txId}). Please verify my payment!`)}`;

    modal.innerHTML = `
      <div class="p-6 sm:p-8 space-y-5 text-center animate-fade-in-up max-w-lg mx-auto">
        <div class="w-16 h-16 bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 rounded-full flex items-center justify-center mx-auto shadow-lg shadow-amber-500/20">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <div>
          <span class="inline-block px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-amber-500 text-white shadow-sm mb-2">⏳ PENDING ADMIN VERIFICATION</span>
          <h3 class="text-xl font-black text-gray-900 dark:text-white">Payment Details Submitted! 📩</h3>
          <p class="text-xs text-gray-600 dark:text-slate-300 mt-2">
            Your payment is recorded. Admin will verify the ₹${amount} payment in Paytm/UPI and approve your access.
          </p>
          <div class="mt-2 p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-[11px] text-emerald-800 dark:text-emerald-300 flex items-center justify-center gap-1.5 font-medium">
            <span>📲</span> WhatsApp message with payment details sent automatically to <strong>7719730804</strong>!
          </div>
        </div>
        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-2xl border border-gray-200 dark:border-slate-700 text-left text-xs space-y-2 font-mono">
          <div class="flex justify-between"><span class="text-gray-400">Transaction ID:</span> <span class="font-bold text-gray-900 dark:text-white">${txId}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">UTR / Ref:</span> <span class="font-bold text-pink-600 dark:text-pink-400">${utrRef}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Paytm / UPI:</span> <span class="font-bold text-gray-700 dark:text-slate-300">7719730804@ptyes</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Amount:</span> <span class="font-bold text-emerald-600">₹${amount}</span></div>
          <div class="flex justify-between"><span class="text-gray-400">Status:</span> <span id="pay-status-badge" class="font-bold text-amber-500">PENDING ADMIN APPROVAL</span></div>
        </div>
        <div class="space-y-2 pt-1">
          <a href="${finalWaUrl}" target="_blank" class="block w-full py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-2xl shadow-md shadow-emerald-500/20 transition-all text-center flex items-center justify-center gap-2">
            <span>💬 Message Admin on WhatsApp (+91 7719730804)</span>
          </a>
          <button onclick="PaywallManager.pollPaymentStatus('${txId}', '${subjectCode}', '${planId}')" class="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-bold text-sm rounded-2xl shadow transition-all flex items-center justify-center gap-2">
            🔄 Check Approval Status Now
          </button>
          <p class="text-[10px] text-gray-400">Auto-polling every 12 seconds... Access will unlock the instant admin approves!</p>
        </div>
      </div>
    `;
    this._pollInterval = setInterval(() => {
      PaywallManager.pollPaymentStatus(txId, subjectCode, planId);
    }, 12000);
  },

  async pollPaymentStatus(txId, subjectCode, planId) {
    try {
      const res = await fetch(`/api/paywall/status/${encodeURIComponent(txId)}`);
      const data = await res.json();
      const badge = document.getElementById('pay-status-badge');
      if (data.is_approved && data.token) {
        clearInterval(this._pollInterval);
        this._pollInterval = null;
        // Grant access ONLY when admin approved!
        this.userData.token = data.token;
        this.isPro = true;
        this.currentPlan = planId;
        localStorage.setItem(this.TOKEN_KEY, data.token);
        localStorage.setItem('lpu_verto_pro_token', data.token);
        localStorage.setItem(this.USER_DATA_KEY, JSON.stringify(this.userData));
        if (window.AuthManager) {
          await window.AuthManager.fetchMe();
          window.AuthManager.renderNavUser();
        }
        this.updateUI();
        this.showVerifiedSuccessView({
          transaction_id: txId,
          utr_ref: data.utr_ref,
          plan: data.plan_name,
          amount_paid: data.amount_paid
        }, subjectCode, planId);
      } else if (badge) {
        if (data.status === 'rejected') {
          badge.textContent = 'REJECTED — Contact Admin on WhatsApp';
          badge.className = 'font-bold text-red-500';
          clearInterval(this._pollInterval);
        } else {
          badge.textContent = 'PENDING ADMIN APPROVAL';
        }
      }
    } catch (e) { /* silent poll */ }
  }
};

window.PaywallManager = PaywallManager;
document.addEventListener('DOMContentLoaded', () => PaywallManager.init());
