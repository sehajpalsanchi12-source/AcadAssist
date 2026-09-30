/**
 * AcadAssist - Google Authentication & Student Profile Manager
 */

const AuthManager = {
  USER_KEY: 'acadassist_user_data',
  TOKEN_KEY: 'acadassist_session_token',

  currentUser: null,

  async init() {
    this.loadSession();
    await this.fetchMe();
    this.renderNavUser();
    this.setupListeners();
  },

  loadSession() {
    try {
      const stored = localStorage.getItem(this.USER_KEY);
      if (stored) {
        this.currentUser = JSON.parse(stored);
      }
    } catch (e) {
      this.currentUser = null;
    }
  },

  async fetchMe() {
    const token = localStorage.getItem(this.TOKEN_KEY);
    if (!token) return;

    try {
      const res = await fetch(`/api/auth/me?token=${encodeURIComponent(token)}`);
      const data = await res.json();
      if (data.authenticated && data.user) {
        this.currentUser = data.user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
        if (data.user.session_token) {
          localStorage.setItem('lpu_verto_pro_token', data.user.session_token);
        }
      }
    } catch (e) {
      console.warn("Auth check error:", e);
    }
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

      container.innerHTML = `
        <div class="flex items-center gap-2">
          <div class="relative group cursor-pointer" onclick="AuthManager.openProfileModal()">
            <img src="${this.currentUser.picture || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + this.currentUser.email}" alt="${this.currentUser.name}" class="w-8 h-8 rounded-full border-2 border-pink-500 object-cover shadow-sm">
            <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 border border-white"></span>
          </div>
          <div class="hidden sm:block text-left cursor-pointer" onclick="AuthManager.openProfileModal()">
            <div class="text-xs font-bold text-gray-900 dark:text-white leading-tight flex items-center gap-1.5">
              <span>${this.currentUser.name.split(' ')[0]}</span>
              ${planBadge}
            </div>
            <div class="text-[10px] text-gray-400 font-mono">${this.currentUser.lpu_reg_no || 'LPU Student'}</div>
          </div>
          <button onclick="AuthManager.logout()" title="Logout" class="p-1.5 rounded-lg text-gray-400 hover:text-red-500 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          </button>
        </div>
      `;
    } else {
      container.innerHTML = `
        <button onclick="AuthManager.openLoginModal()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 hover:bg-gray-50 dark:hover:bg-slate-750 text-gray-800 dark:text-white border border-gray-200 dark:border-slate-700 flex items-center gap-2 shadow-sm transition-all">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          <span>Sign In with Google</span>
        </button>
      `;
    }
  },

  setupListeners() {
    // Listen for custom trigger to login
    window.addEventListener('request-google-login', () => {
      this.openLoginModal();
    });
  },

  openLoginModal() {
    const modal = document.getElementById('google-login-modal');
    if (modal) modal.showModal();
  },

  async loginWithGoogle(accountType = 'custom') {
    let name = 'LPU Student';
    let email = 'student@lpu.in';
    let regNo = '12214589';
    let phone = '8053122848';

    if (accountType === 'demo1') {
      name = 'Aman Kumar (Verto)';
      email = 'aman.12214589@lpu.in';
      regNo = '12214589';
      phone = '8053122848';
    } else if (accountType === 'demo2') {
      name = 'Priya Sharma (CSE)';
      email = 'priya.sharma@gmail.com';
      regNo = '12108842';
      phone = '6239470804';
    } else {
      const nameInput = document.getElementById('google-login-name')?.value.trim();
      const emailInput = document.getElementById('google-login-email')?.value.trim();
      const regInput = document.getElementById('google-login-regno')?.value.trim();
      const phoneInput = document.getElementById('google-login-phone')?.value.trim();

      if (nameInput) name = nameInput;
      if (emailInput) email = emailInput;
      if (regInput) regNo = regInput;
      if (phoneInput) phone = phoneInput;
    }

    try {
      const res = await fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          google_id: 'goog_' + Math.abs(email.split('').reduce((a, b) => ((a << 5) - a) + b.charCodeAt(0), 0)),
          name: name,
          email: email,
          picture: `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(email)}`,
          lpu_reg_no: regNo,
          phone: phone
        })
      });

      const data = await res.json();
      if (data.success && data.user) {
        this.currentUser = data.user;
        localStorage.setItem(this.USER_KEY, JSON.stringify(data.user));
        localStorage.setItem(this.TOKEN_KEY, data.session_token);
        localStorage.setItem('lpu_verto_pro_token', data.session_token);

        // Pre-fill checkout form
        const checkoutName = document.getElementById('checkout-student-name');
        const checkoutReg = document.getElementById('checkout-reg-no');
        if (checkoutName) checkoutName.value = data.user.name;
        if (checkoutReg) checkoutReg.value = data.user.lpu_reg_no;

        this.renderNavUser();
        if (window.PaywallManager) window.PaywallManager.verifyStatus();

        document.getElementById('google-login-modal')?.close();
      }
    } catch (e) {
      alert("Failed to authenticate with Google. Please try again.");
    }
  },

  openProfileModal() {
    if (!this.currentUser) return;
    const modal = document.getElementById('user-profile-modal');
    if (!modal) return;

    const content = document.getElementById('user-profile-content');
    if (content) {
      content.innerHTML = `
        <div class="text-center pb-4 border-b border-gray-100 dark:border-slate-800">
          <img src="${this.currentUser.picture}" alt="${this.currentUser.name}" class="w-16 h-16 rounded-full border-2 border-pink-500 mx-auto mb-2 object-cover shadow-md">
          <h3 class="text-lg font-black text-gray-900 dark:text-white">${this.currentUser.name}</h3>
          <p class="text-xs text-gray-500 dark:text-slate-400 font-mono">${this.currentUser.email}</p>
          <div class="mt-2 inline-block px-3 py-1 rounded-full text-xs font-bold ${this.currentUser.is_pro ? 'bg-pink-100 text-pink-700 dark:bg-pink-950/60 dark:text-pink-400' : 'bg-gray-100 text-gray-600 dark:bg-slate-800 dark:text-slate-300'}">
            Active Plan: ${this.currentUser.plan_name || 'Free Starter'}
          </div>
        </div>

        <form id="update-profile-form" onsubmit="event.preventDefault(); AuthManager.saveProfile();" class="space-y-3 pt-3">
          <div>
            <label class="block text-[11px] font-semibold text-gray-500 dark:text-slate-400">LPU Registration Number:</label>
            <input type="text" id="profile-edit-reg" value="${this.currentUser.lpu_reg_no || ''}" class="w-full text-xs p-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800">
          </div>
          <div>
            <label class="block text-[11px] font-semibold text-gray-500 dark:text-slate-400">Phone / WhatsApp Number:</label>
            <input type="text" id="profile-edit-phone" value="${this.currentUser.phone || ''}" class="w-full text-xs p-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800">
          </div>

          <div class="p-3 rounded-xl bg-orange-50/50 dark:bg-slate-800/50 border border-orange-200/50 dark:border-slate-700 text-xs space-y-1">
            <div class="flex justify-between"><span class="text-gray-500">Mock Tests Attempted:</span> <span class="font-bold">${this.currentUser.mock_tests_count || 0}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Total Spent:</span> <span class="font-bold text-green-600">₹${this.currentUser.total_spent_inr || 0}</span></div>
          </div>

          <button type="submit" class="w-full py-2.5 bg-gradient-to-r from-pink-500 to-rose-500 text-white font-bold text-xs rounded-xl shadow transition-all">
            Save Profile Changes
          </button>
        </form>
      `;
    }
    modal.showModal();
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
        this.renderNavUser();
        document.getElementById('user-profile-modal')?.close();
      }
    } catch (e) {
      alert("Failed to update profile.");
    }
  },

  logout() {
    this.currentUser = null;
    localStorage.removeItem(this.USER_KEY);
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem('lpu_verto_pro_token');
    this.renderNavUser();
    if (window.PaywallManager) window.PaywallManager.verifyStatus();
  }
};

window.AuthManager = AuthManager;
document.addEventListener('DOMContentLoaded', () => AuthManager.init());
