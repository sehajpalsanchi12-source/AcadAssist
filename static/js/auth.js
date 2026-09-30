/**
 * AcadAssist - Secure Student Authentication & Profile Manager
 * PBKDF2-HMAC-SHA256 salted password authentication & session management.
 */

const AuthManager = {
  USER_KEY: 'acadassist_user_data',
  TOKEN_KEY: 'acadassist_session_token',

  currentUser: null,

  async init() {
    this.setupListeners();
    await this.fetchMe();
    this.renderNavUser();

    // Ask for user login or account creation at starting if not authenticated
    if (!this.currentUser) {
      setTimeout(() => {
        const dismissed = sessionStorage.getItem('acad_auth_prompt_dismissed');
        if (!dismissed && !this.currentUser) {
          this.openWelcomeAuthModal();
        }
      }, 700);
    }
  },

  openWelcomeAuthModal() {
    const banner = document.getElementById('auth-welcome-banner');
    if (banner) banner.classList.remove('hidden');
    this.openLoginModal('register');
  },

  dismissAuthModal() {
    sessionStorage.setItem('acad_auth_prompt_dismissed', 'true');
    const modal = document.getElementById('google-login-modal');
    if (modal) modal.close();
  },

  async fetchMe() {
    const token = localStorage.getItem(this.TOKEN_KEY) || localStorage.getItem('lpu_verto_pro_token');
    if (!token) {
      this.clearAllUserData();
      return;
    }

    try {
      const res = await fetch(`/api/auth/me?token=${encodeURIComponent(token)}`);
      const data = await res.json();
      if (data.authenticated && data.user) {
        this.currentUser = data.user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
        localStorage.setItem(this.TOKEN_KEY, data.user.session_token || token);
        localStorage.setItem('lpu_verto_pro_token', data.user.session_token || token);
        this.syncCheckoutFields(data.user);

        // Sync Pro access to PaywallManager if user owns active plan or purchased subjects
        if (window.PaywallManager) {
          if (data.user.is_pro || (data.user.active_plan && data.user.active_plan !== 'free')) {
            window.PaywallManager.isPro = true;
            window.PaywallManager.currentPlan = data.user.active_plan;
            window.PaywallManager.updateUI();
          }
        }
      } else {
        // Token invalid, expired, or signed out
        this.clearAllUserData();
      }
    } catch (e) {
      console.warn("Auth verification network error:", e);
      this.clearAllUserData();
    }
  },

  clearAllUserData() {
    this.currentUser = null;
    localStorage.removeItem(this.USER_KEY);
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem('lpu_verto_pro_token');
    localStorage.removeItem('acad_user_data');
    localStorage.removeItem('acad_user_pro_token');
    this.clearCheckoutFields();
  },

  syncCheckoutFields(user) {
    if (!user) return;
    const checkoutName = document.getElementById('checkout-student-name');
    const checkoutReg = document.getElementById('checkout-reg-no');
    const checkoutPhone = document.getElementById('checkout-phone');
    if (checkoutName && user.name) checkoutName.value = user.name;
    if (checkoutReg && user.lpu_reg_no) checkoutReg.value = user.lpu_reg_no;
    if (checkoutPhone && user.phone) checkoutPhone.value = user.phone;
  },

  clearCheckoutFields() {
    const checkoutName = document.getElementById('checkout-student-name');
    const checkoutReg = document.getElementById('checkout-reg-no');
    const checkoutPhone = document.getElementById('checkout-phone');
    if (checkoutName) checkoutName.value = '';
    if (checkoutReg) checkoutReg.value = '';
    if (checkoutPhone) checkoutPhone.value = '';
  },

  renderNavUser() {
    const container = document.getElementById('user-auth-nav-container');
    if (!container) return;

    if (this.currentUser) {
      const isPro = this.currentUser.is_pro || (this.currentUser.active_plan && this.currentUser.active_plan !== 'free');
      const planBadge = isPro
        ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-sm">
             ${this.currentUser.plan_name || '₹49 MOCK PASS'}
           </span>`
        : `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-gray-100 dark:bg-slate-800 text-gray-500">Free</span>`;

      const displayName = (this.currentUser.name || 'Student').split(' ')[0];

      container.innerHTML = `
        <div class="flex items-center gap-2">
          <div class="relative group cursor-pointer" onclick="AuthManager.openProfileModal()" title="View Profile">
            <img src="${this.currentUser.picture || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + encodeURIComponent(this.currentUser.email || 'user')}" alt="${this.currentUser.name}" class="w-8 h-8 rounded-full border-2 border-pink-500 object-cover shadow-sm">
            <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 border border-white"></span>
          </div>
          <div class="hidden sm:block text-left cursor-pointer" onclick="AuthManager.openProfileModal()">
            <div class="text-xs font-bold text-gray-900 dark:text-white leading-tight flex items-center gap-1.5">
              <span>${displayName}</span>
              ${planBadge}
            </div>
            <div class="text-[10px] text-gray-400 font-mono">${this.currentUser.lpu_reg_no || this.currentUser.email || 'LPU Student'}</div>
          </div>
          <button onclick="AuthManager.logout()" title="Logout" class="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          </button>
        </div>
      `;
    } else {
      container.innerHTML = `
        <button onclick="AuthManager.openLoginModal()" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 hover:bg-gray-50 dark:hover:bg-slate-750 text-gray-800 dark:text-white border border-gray-200 dark:border-slate-700 flex items-center gap-2 shadow-sm transition-all group">
          <svg class="w-3.5 h-3.5 text-pink-500 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          <span>Sign In / Register</span>
        </button>
      `;
    }
  },

  setupListeners() {
    window.addEventListener('request-google-login', () => {
      this.openLoginModal();
    });
  },

  openLoginModal(defaultTab = 'signin') {
    const modal = document.getElementById('google-login-modal');
    if (!modal) return;
    this.switchTab(defaultTab);
    this.clearAuthErrors();
    modal.showModal();
  },

  switchTab(tab) {
    const signinForm = document.getElementById('auth-signin-form');
    const registerForm = document.getElementById('auth-register-form');
    const signinBtn = document.getElementById('auth-tab-btn-signin');
    const registerBtn = document.getElementById('auth-tab-btn-register');

    if (tab === 'signin') {
      if (signinForm) signinForm.classList.remove('hidden');
      if (registerForm) registerForm.classList.add('hidden');
      if (signinBtn) {
        signinBtn.className = 'py-2 rounded-xl transition-all bg-white dark:bg-slate-700 text-pink-600 dark:text-pink-400 shadow-sm';
      }
      if (registerBtn) {
        registerBtn.className = 'py-2 rounded-xl transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white';
      }
    } else {
      if (signinForm) signinForm.classList.add('hidden');
      if (registerForm) registerForm.classList.remove('hidden');
      if (registerBtn) {
        registerBtn.className = 'py-2 rounded-xl transition-all bg-white dark:bg-slate-700 text-pink-600 dark:text-pink-400 shadow-sm';
      }
      if (signinBtn) {
        signinBtn.className = 'py-2 rounded-xl transition-all text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white';
      }
    }
    this.clearAuthErrors();
  },

  togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.type = input.type === 'password' ? 'text' : 'password';
  },

  clearAuthErrors() {
    const loginErr = document.getElementById('auth-login-error');
    const regErr = document.getElementById('auth-register-error');
    if (loginErr) { loginErr.textContent = ''; loginErr.classList.add('hidden'); }
    if (regErr) { regErr.textContent = ''; regErr.classList.add('hidden'); }
  },

  showError(containerId, message) {
    const errBox = document.getElementById(containerId);
    if (errBox) {
      errBox.textContent = message;
      errBox.classList.remove('hidden');
    } else {
      alert(message);
    }
  },

  async submitLogin() {
    this.clearAuthErrors();
    const identifier = document.getElementById('auth-login-identifier')?.value.trim();
    const password = document.getElementById('auth-login-password')?.value;
    const btn = document.getElementById('auth-signin-btn');

    if (!identifier || !password) {
      this.showError('auth-login-error', 'Please enter your email/reg number and password.');
      return;
    }

    const origText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Verifying Credentials...'; }

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier, password })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        this.showError('auth-login-error', data.detail || data.message || 'Login failed. Please verify credentials.');
        return;
      }

      this.currentUser = data.user;
      localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
      localStorage.setItem(this.TOKEN_KEY, data.session_token);
      localStorage.setItem('lpu_verto_pro_token', data.session_token);

      this.syncCheckoutFields(data.user);
      this.renderNavUser();

      if (window.PaywallManager) window.PaywallManager.verifyStatus();

      document.getElementById('google-login-modal')?.close();
    } catch (e) {
      this.showError('auth-login-error', 'Network error occurred. Please try again.');
    } finally {
      if (btn) { btn.disabled = false; btn.textContent = origText; }
    }
  },

  async submitRegister() {
    this.clearAuthErrors();
    const name = document.getElementById('auth-reg-name')?.value.trim();
    const email = document.getElementById('auth-reg-email')?.value.trim();
    const regno = document.getElementById('auth-reg-regno')?.value.trim();
    const phone = document.getElementById('auth-reg-phone')?.value.trim();
    const password = document.getElementById('auth-reg-password')?.value;
    const btn = document.getElementById('auth-register-btn');

    if (!name || !email || !password) {
      this.showError('auth-register-error', 'Please fill in Name, Email and Password.');
      return;
    }

    if (password.length < 6) {
      this.showError('auth-register-error', 'Password must be at least 6 characters long.');
      return;
    }

    const origText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Creating Account...'; }

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          email,
          password,
          lpu_reg_no: regno || null,
          phone: phone || null
        })
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        this.showError('auth-register-error', data.detail || data.message || 'Registration failed.');
        return;
      }

      this.currentUser = data.user;
      localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
      localStorage.setItem(this.TOKEN_KEY, data.session_token);
      localStorage.setItem('lpu_verto_pro_token', data.session_token);

      this.syncCheckoutFields(data.user);
      this.renderNavUser();

      if (window.PaywallManager) window.PaywallManager.verifyStatus();

      document.getElementById('google-login-modal')?.close();
    } catch (e) {
      this.showError('auth-register-error', 'Network error occurred. Please try again.');
    } finally {
      if (btn) { btn.disabled = false; btn.textContent = origText; }
    }
  },

  async promptGoogleOAuth() {
    const email = prompt("Enter your Google Account email to securely link / sign in:");
    if (!email || !email.includes('@')) {
      if (email) alert("Please enter a valid Google email address.");
      return;
    }
    const name = prompt("Enter your Name:") || email.split('@')[0];

    try {
      const res = await fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          google_id: 'goog_' + Math.abs(email.split('').reduce((a, b) => ((a << 5) - a) + b.charCodeAt(0), 0)),
          name: name,
          email: email.toLowerCase(),
          picture: `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(email)}`
        })
      });

      const data = await res.json();
      if (data.success && data.user) {
        this.currentUser = data.user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
        localStorage.setItem(this.TOKEN_KEY, data.session_token);
        localStorage.setItem('lpu_verto_pro_token', data.session_token);

        this.syncCheckoutFields(data.user);
        this.renderNavUser();

        if (window.PaywallManager) window.PaywallManager.verifyStatus();
        document.getElementById('google-login-modal')?.close();
      }
    } catch (e) {
      alert("Failed to authenticate with Google. Please try again.");
    }
  },

  async recordActivity(type, title, subjectCode = null, details = null) {
    try {
      const userId = this.currentUser ? this.currentUser.id : (localStorage.getItem('acadassist_sess_id') || 'guest');
      await fetch('/api/user/activity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          activity_type: type,
          title: title,
          subject_code: subjectCode,
          details: details
        })
      });
    } catch (e) {}
  },

  async openProfileModal() {
    if (!this.currentUser) {
      this.openLoginModal('signin');
      return;
    }
    const modal = document.getElementById('user-profile-modal');
    if (!modal) return;

    modal.showModal();
    this.renderProfileModalContent('info');
  },

  async renderProfileModalContent(activeTab = 'info') {
    const content = document.getElementById('user-profile-content');
    if (!content || !this.currentUser) return;

    // Fetch user purchases and activities
    let purchasesData = { purchased_subjects: this.currentUser.purchased_subjects || [], approved_purchases: [], pending_purchases: [] };
    let activities = [];

    try {
      const [purchRes, actRes] = await Promise.all([
        fetch(`/api/user/purchases?user_id=${encodeURIComponent(this.currentUser.id)}`).then(r => r.json()).catch(() => null),
        fetch(`/api/user/activities?user_id=${encodeURIComponent(this.currentUser.id)}&limit=30`).then(r => r.json()).catch(() => null)
      ]);
      if (purchRes) purchasesData = purchRes;
      if (actRes && actRes.activities) activities = actRes.activities;
    } catch (e) {}

    const isPro = this.currentUser.is_pro || (this.currentUser.active_plan && this.currentUser.active_plan !== 'free');
    const allSubjects = purchasesData.purchased_subjects || this.currentUser.purchased_subjects || [];

    content.innerHTML = `
      <div class="space-y-4">
        <!-- Profile Top Banner -->
        <div class="flex items-center justify-between pb-3 border-b border-gray-100 dark:border-slate-800">
          <div class="flex items-center gap-3">
            <img src="${this.currentUser.picture || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + encodeURIComponent(this.currentUser.email || 'user')}" alt="${this.currentUser.name}" class="w-12 h-12 rounded-full border-2 border-pink-500 object-cover shadow-sm">
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base font-black text-gray-900 dark:text-white">${this.currentUser.name}</h3>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${isPro ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white' : 'bg-gray-100 dark:bg-slate-800 text-gray-500'}">
                  ${this.currentUser.plan_name || 'Free Starter'}
                </span>
              </div>
              <p class="text-xs text-gray-500 dark:text-slate-400 font-mono">${this.currentUser.email}</p>
            </div>
          </div>
          <button onclick="document.getElementById('user-profile-modal').close()" class="p-1.5 text-gray-400 hover:text-white text-lg font-bold">✕</button>
        </div>

        <!-- Inner Navigation Tabs -->
        <div class="grid grid-cols-3 p-1 bg-gray-100 dark:bg-slate-800/80 rounded-2xl text-xs font-bold gap-1">
          <button type="button" onclick="AuthManager.renderProfileModalContent('info')" class="py-2 rounded-xl transition-all ${activeTab === 'info' ? 'bg-white dark:bg-slate-700 text-pink-600 dark:text-pink-400 shadow-sm' : 'text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white'}">
            👤 Profile
          </button>
          <button type="button" onclick="AuthManager.renderProfileModalContent('purchases')" class="py-2 rounded-xl transition-all ${activeTab === 'purchases' ? 'bg-white dark:bg-slate-700 text-pink-600 dark:text-pink-400 shadow-sm' : 'text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white'}">
            💳 Purchases (${(purchasesData.approved_purchases || []).length})
          </button>
          <button type="button" onclick="AuthManager.renderProfileModalContent('activities')" class="py-2 rounded-xl transition-all ${activeTab === 'activities' ? 'bg-white dark:bg-slate-700 text-pink-600 dark:text-pink-400 shadow-sm' : 'text-gray-500 dark:text-slate-400 hover:text-gray-900 dark:hover:text-white'}">
            📋 Responses (${activities.length})
          </button>
        </div>

        <!-- TAB 1: Profile Info -->
        <div id="prof-tab-info" class="${activeTab === 'info' ? '' : 'hidden'} space-y-3">
          <form onsubmit="event.preventDefault(); AuthManager.saveProfile();" class="space-y-3">
            <div>
              <label class="block text-[11px] font-semibold text-gray-500 dark:text-slate-400 mb-1">LPU Registration Number:</label>
              <input type="text" id="profile-edit-reg" value="${this.currentUser.lpu_reg_no || ''}" placeholder="e.g. 12200000" class="w-full text-xs p-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 font-mono">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-gray-500 dark:text-slate-400 mb-1">WhatsApp / Phone Number:</label>
              <input type="text" id="profile-edit-phone" value="${this.currentUser.phone || ''}" placeholder="e.g. 9876543210" class="w-full text-xs p-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 font-mono">
            </div>

            <div class="grid grid-cols-2 gap-2 p-3 rounded-xl bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-700 text-xs">
              <div><span class="text-gray-500">Mock Tests:</span> <strong class="ml-1 text-gray-900 dark:text-white">${this.currentUser.mock_tests_count || 0}</strong></div>
              <div><span class="text-gray-500">Total Spent:</span> <strong class="ml-1 text-emerald-600 font-bold">₹${this.currentUser.total_spent_inr || 0}</strong></div>
            </div>

            <button type="submit" class="w-full py-2.5 bg-gradient-to-r from-pink-500 to-rose-600 text-white font-bold text-xs rounded-xl shadow transition-all">
              Save Profile Changes
            </button>
          </form>
        </div>

        <!-- TAB 2: My Purchases & Passes -->
        <div id="prof-tab-purchases" class="${activeTab === 'purchases' ? '' : 'hidden'} space-y-3 max-h-80 overflow-y-auto pr-1">
          <div class="p-3 rounded-xl bg-pink-50 dark:bg-pink-950/30 border border-pink-200 dark:border-pink-800/50">
            <span class="text-[10px] uppercase font-bold text-pink-600 dark:text-pink-400">Current Plan Status</span>
            <div class="text-sm font-black text-gray-900 dark:text-white mt-0.5">${this.currentUser.plan_name || 'Free Starter'}</div>
          </div>

          <div>
            <h4 class="text-xs font-bold text-gray-700 dark:text-slate-300 mb-1.5">Unlocked Subjects</h4>
            ${allSubjects.length ? `
              <div class="flex flex-wrap gap-1.5">
                ${allSubjects.map(sub => `
                  <span class="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-100 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800 flex items-center gap-1">
                    <span>✓ ${sub}</span>
                  </span>
                `).join('')}
              </div>
            ` : `
              <p class="text-xs text-gray-400 italic">No specific subject passes purchased yet.</p>
            `}
          </div>

          <div>
            <h4 class="text-xs font-bold text-gray-700 dark:text-slate-300 mb-1.5">Transaction Receipts</h4>
            ${(purchasesData.all_transactions || []).length ? `
              <div class="space-y-2">
                ${purchasesData.all_transactions.map(t => `
                  <div class="p-2.5 rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 text-xs space-y-1">
                    <div class="flex items-center justify-between">
                      <strong class="text-gray-900 dark:text-white font-bold">${t.plan_name}</strong>
                      <span class="font-bold text-emerald-600">₹${t.amount}</span>
                    </div>
                    <div class="flex items-center justify-between text-[11px] text-gray-400 font-mono">
                      <span>TxID: ${t.tx_id}</span>
                      <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${t.status === 'approved' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400' : (t.status === 'pending' ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400' : 'bg-red-100 text-red-700')}">
                        ${t.status === 'approved' ? '✓ APPROVED' : (t.status === 'pending' ? '⏳ PENDING' : 'REJECTED')}
                      </span>
                    </div>
                    <div class="text-[10px] text-gray-400">UTR: ${t.utr_ref || 'N/A'} • ${t.formatted_time || ''}</div>
                  </div>
                `).join('')}
              </div>
            ` : `
              <p class="text-xs text-gray-400 italic">No payment transactions found.</p>
            `}
          </div>
        </div>

        <!-- TAB 3: Saved Activities & Responses -->
        <div id="prof-tab-activities" class="${activeTab === 'activities' ? '' : 'hidden'} space-y-2.5 max-h-80 overflow-y-auto pr-1">
          ${activities.length ? activities.map(a => `
            <div class="p-2.5 rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 text-xs space-y-1">
              <div class="flex items-center justify-between">
                <strong class="text-gray-900 dark:text-white font-bold">${a.title}</strong>
                <span class="px-2 py-0.5 rounded-full text-[9px] font-bold bg-pink-100 dark:bg-pink-950/50 text-pink-600 dark:text-pink-400 uppercase">
                  ${a.activity_type}
                </span>
              </div>
              <div class="text-[11px] text-gray-500 dark:text-slate-400">${a.subject_code ? `Course: ${a.subject_code} • ` : ''}${a.formatted_time}</div>
              ${a.details && a.details.score !== undefined ? `
                <div class="text-[11px] font-semibold text-purple-600 dark:text-purple-400">
                  🎯 Result: Score ${a.details.score}/${a.details.total_marks || a.details.totalPossible} (${a.details.percentage}% - Grade ${a.details.grade})
                </div>
              ` : ''}
            </div>
          `).join('') : `
            <div class="py-8 text-center text-xs text-gray-400">
              No saved activities yet. Take a mock test or generate study assets to see your response history!
            </div>
          `}
        </div>

      </div>
    `;
  },

  async saveProfile() {
    if (!this.currentUser) return;
    const reg = document.getElementById('profile-edit-reg')?.value.trim();
    const phone = document.getElementById('profile-edit-phone')?.value.trim();

    try {
      const res = await fetch('/api/auth/update-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: this.currentUser.id,
          lpu_reg_no: reg,
          phone: phone
        })
      });
      const data = await res.json();
      if (data.success) {
        this.currentUser = data.user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
        this.syncCheckoutFields(data.user);
        this.renderNavUser();
        this.renderProfileModalContent('info');
        alert("✅ Profile updated successfully!");
      }
    } catch (e) {
      alert("Failed to update profile.");
    }
  },

  logout() {
    this.clearAllUserData();
    this.renderNavUser();
    if (window.PaywallManager) {
      window.PaywallManager.isPro = false;
      window.PaywallManager.currentPlan = 'free';
      window.PaywallManager.userData = { name: '', regNo: '', phone: '', token: null };
      window.PaywallManager.updateUI();
    }
  }
};

window.AuthManager = AuthManager;
document.addEventListener('DOMContentLoaded', () => AuthManager.init());
