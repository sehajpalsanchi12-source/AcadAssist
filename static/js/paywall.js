/**
 * AcadAssist - Paywall, UPI Payment Gateway (7719730804@ptyes) & Subscription Manager
 */

const PaywallManager = {
  TOKEN_KEY: 'acad_user_pro_token',
  USER_DATA_KEY: 'acad_user_data',
  UPI_DESTINATION: '7719730804@ptyes',

  currentPlan: 'free',
  isPro: false,
  userData: {
    name: 'LPU Student',
    regNo: '12200001',
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
    const token = localStorage.getItem(this.TOKEN_KEY) || localStorage.getItem('lpu_verto_pro_token');
    const data = localStorage.getItem(this.USER_DATA_KEY);
    if (token) this.userData.token = token;
    if (data) {
      try {
        const parsed = JSON.parse(data);
        this.userData = { ...this.userData, ...parsed };
      } catch (e) {}
    }
    // Also sync with AuthManager if logged in
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      this.userData.name = u.name;
      this.userData.regNo = u.lpu_reg_no || this.userData.regNo;
      this.userData.phone = u.phone || this.userData.phone;
    }
  },

  async verifyStatus() {
    const token = this.userData.token || (window.AuthManager?.currentUser?.session_token);
    if (!token) {
      this.isPro = false;
      this.currentPlan = 'free';
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
    }
  },

  updateUI() {
    const badge = document.getElementById('user-plan-badge');
    const upgradeNavBtn = document.getElementById('nav-upgrade-btn');
    const proBanner = document.getElementById('pro-active-banner');

    if (this.isPro) {
      if (badge) {
        badge.innerHTML = `<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-sm shadow-pink-500/20">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          ACTIVE MOCK PASS
        </span>`;
      }
      if (upgradeNavBtn) upgradeNavBtn.classList.add('hidden');
      if (proBanner) proBanner.classList.remove('hidden');
    } else {
      if (badge) {
        badge.innerHTML = `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-slate-300 border border-gray-200 dark:border-slate-700">
          Mock Test Pass: ₹49
        </span>`;
      }
      if (upgradeNavBtn) upgradeNavBtn.classList.remove('hidden');
      if (proBanner) proBanner.classList.add('hidden');
    }
  },

  setupListeners() {
    // Open Paywall Modal Buttons
    document.querySelectorAll('[data-open-paywall]').forEach(btn => {
      btn.addEventListener('click', () => {
        const plan = btn.getAttribute('data-plan') || 'midterm_mock_49';
        const subj = btn.getAttribute('data-subject') || null;
        this.openCheckoutModal(plan, subj);
      });
    });

    // Close Modal
    const modal = document.getElementById('paywall-modal');
    const closeBtn = document.getElementById('close-paywall-modal');
    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.close());
    }

    // Coupon Apply Button
    const applyCouponBtn = document.getElementById('apply-coupon-btn');
    if (applyCouponBtn) {
      applyCouponBtn.addEventListener('click', () => this.applyCoupon());
    }

    // Payment Form Submit
    const payForm = document.getElementById('checkout-form');
    if (payForm) {
      payForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.processPayment();
      });
    }
  },

  openCheckoutModal(planId = 'midterm_mock_49', subjectCode = null) {
    const modal = document.getElementById('paywall-modal');
    if (!modal) return;

    const planTitle = document.getElementById('checkout-plan-title');
    const planPrice = document.getElementById('checkout-plan-price');
    const planInput = document.getElementById('checkout-plan-id');
    const subjInput = document.getElementById('checkout-subject-code');
    const qrImage = document.getElementById('checkout-upi-qr');
    const upiLink = document.getElementById('checkout-upi-app-link');

    let price = 49;
    let title = 'Midterm Mode / Subject Mock Test Pass (₹49)';
    if (planId === 'educode_99') {
      price = 99;
      title = 'EduCode Completion Support Pass (₹99)';
    } else if (planId === 'neobrowser_99') {
      price = 99;
      title = 'NeoBrowser Completion Support Pass (₹99)';
    } else if (planId === 'rush24') {
      price = 29;
      title = 'Exam Night Rush Pass (₹29)';
    } else if (planId === 'semester_pro') {
      price = 199;
      title = 'AcadAssist All-Access Semester Pro (₹199)';
    }

    if (subjectCode) {
      title += ` • ${subjectCode}`;
    }

    if (planInput) planInput.value = planId;
    if (subjInput) subjInput.value = subjectCode || 'ALL';
    if (planTitle) planTitle.textContent = title;
    if (planPrice) planPrice.textContent = `₹${price}`;

    // Generate dynamic QR Code for 7719730804@ptyes
    const upiUri = `upi://pay?pa=${this.UPI_DESTINATION}&pn=AcadAssist&am=${price}.00&cu=INR&tn=${encodeURIComponent(title.slice(0, 30))}`;
    if (qrImage) {
      qrImage.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=6&data=${encodeURIComponent(upiUri)}`;
    }
    if (upiLink) {
      upiLink.href = upiUri;
    }

    // Autofill user details
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      const nameInp = document.getElementById('checkout-student-name');
      const regInp = document.getElementById('checkout-reg-no');
      const phoneInp = document.getElementById('checkout-phone');
      if (nameInp) nameInp.value = u.name;
      if (regInp && u.lpu_reg_no) regInp.value = u.lpu_reg_no;
      if (phoneInp && u.phone) phoneInp.value = u.phone;
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
    const planId = document.getElementById('checkout-plan-id')?.value || 'midterm_mock_49';
    const subjectCode = document.getElementById('checkout-subject-code')?.value || 'ALL';
    const coupon = document.getElementById('coupon-code-input')?.value.trim() || null;
    const nameInput = document.getElementById('checkout-student-name')?.value.trim() || 'LPU Student';
    const regInput = document.getElementById('checkout-reg-no')?.value.trim() || '12000000';
    const phoneInput = document.getElementById('checkout-phone')?.value.trim() || '';
    const utrInput = document.getElementById('checkout-utr-input')?.value.trim() || null;
    const method = document.querySelector('input[name="payment_method"]:checked')?.value || 'upi';

    const userId = window.AuthManager?.currentUser?.id || null;

    const submitBtn = document.getElementById('pay-submit-btn');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg> Verifying with AcadAssist Desk (${this.UPI_DESTINATION})...`;
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
          user_id: userId,
          subject_code: subjectCode
        })
      });

      const data = await res.json();
      if (data.success) {
        // Save Pro Token
        this.userData.token = data.token;
        this.userData.name = nameInput;
        this.userData.regNo = regInput;
        this.isPro = true;
        this.currentPlan = planId;

        localStorage.setItem(this.TOKEN_KEY, data.token);
        localStorage.setItem('lpu_verto_pro_token', data.token);
        localStorage.setItem(this.USER_DATA_KEY, JSON.stringify(this.userData));

        // Refresh AuthManager if logged in
        if (window.AuthManager) {
          await window.AuthManager.fetchMe();
          window.AuthManager.renderNavUser();
        }

        // Show Success View
        this.showSuccessView(data);
        this.updateUI();

        // Refresh current paper if active
        if (window.ExamSimulator && window.ExamSimulator.currentPaper) {
          window.ExamSimulator.unlockPaperSolutions();
        }
      } else {
        alert(data.message || 'Payment simulation failed.');
      }
    } catch (e) {
      alert('Error during checkout process.');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `Verify UTR & Activate Access →`;
      }
    }
  },

  showSuccessView(data) {
    const modalContent = document.getElementById('checkout-modal-content');
    if (!modalContent) return;

    modalContent.innerHTML = `
      <div class="text-center py-6 animate-fade-in-up">
        <div class="w-16 h-16 bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">🎉 Payment Recorded & Access Active!</h3>
        <p class="text-sm text-gray-600 dark:text-slate-300 mb-4">You now have full access to <strong>${data.plan}</strong>. All LPU Mock Tests, MCQs, and 10-mark solutions are UNLOCKED.</p>
        
        <div class="bg-gray-50 dark:bg-slate-800 p-4 rounded-xl border border-gray-200 dark:border-slate-700 text-left text-xs space-y-1.5 mb-6">
          <div class="flex justify-between"><span class="text-gray-500">Transaction ID:</span> <span class="font-mono font-semibold">${data.transaction_id}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">UTR / Ref No:</span> <span class="font-mono font-bold text-pink-600 dark:text-pink-400">${data.utr_ref}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Paid to UPI:</span> <span class="font-mono font-bold">${this.UPI_DESTINATION}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Amount:</span> <span class="font-bold text-green-600">₹${data.amount_paid}</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Status:</span> <span class="font-bold text-emerald-500">VERIFIED & ACTIVE</span></div>
        </div>

        <button onclick="document.getElementById('paywall-modal').close()" class="w-full py-3 bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white font-bold rounded-xl shadow-lg shadow-pink-500/30 transition-all">
          Start Practicing Midterm Mock Tests →
        </button>
      </div>
    `;
  }
};

window.PaywallManager = PaywallManager;
document.addEventListener('DOMContentLoaded', () => PaywallManager.init());
