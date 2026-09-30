/**
 * AcadAssist - Full Admin Portal Controller
 * Authentication handled via secure backend session tokens
 */

const AdminPortal = {
  TOKEN_KEY: 'acadassist_admin_token',
  adminToken: null,

  init() {
    this.adminToken = localStorage.getItem(this.TOKEN_KEY);
    this.setupListeners();
  },

  setupListeners() {
    // Admin login form submit
    const loginForm = document.getElementById('admin-login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.login();
      });
    }
  },

  openPortal() {
    if (this.adminToken) {
      this.loadDashboard();
    } else {
      document.getElementById('admin-login-modal')?.showModal();
    }
  },

  async login() {
    const username = document.getElementById('admin-username-input')?.value.trim();
    const password = document.getElementById('admin-password-input')?.value.trim();
    const errBox = document.getElementById('admin-login-error');

    if (!username || !password) {
      if (errBox) errBox.textContent = 'Please enter both username and password.';
      return;
    }

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      if (res.ok && data.success) {
        this.adminToken = data.token;
        localStorage.setItem(this.TOKEN_KEY, data.token);
        document.getElementById('admin-login-modal')?.close();
        this.loadDashboard();
      } else {
        if (errBox) errBox.textContent = data.detail || 'Invalid username or password.';
      }
    } catch (e) {
      if (errBox) errBox.textContent = 'Connection error. Please try again.';
    }
  },

  async loadDashboard() {
    const modal = document.getElementById('admin-dashboard-modal');
    if (!modal) return;

    modal.showModal();
    await this.refreshAll();
  },

  async refreshAll() {
    await this.fetchStats();
    await this.fetchTransactions();
    await this.fetchUsers();
    await this.fetchMockTests();
    await this.fetchServiceRequests();
  },

  async fetchStats() {
    try {
      const res = await fetch(`/api/admin/stats?token=${encodeURIComponent(this.adminToken)}`);
      if (res.status === 401) {
        this.logout();
        return;
      }
      const data = await res.json();
      document.getElementById('admin-stat-revenue').textContent = `₹${data.total_revenue_inr}`;
      document.getElementById('admin-stat-users').textContent = data.total_users;
      document.getElementById('admin-stat-tests').textContent = data.total_mock_tests;
      document.getElementById('admin-stat-inquiries').textContent = data.total_service_inquiries;
      document.getElementById('admin-stat-pending').textContent = data.pending_payments_count;
    } catch (e) {
      console.warn("Failed to load admin stats:", e);
    }
  },

  async fetchTransactions() {
    try {
      const res = await fetch(`/api/admin/transactions?token=${encodeURIComponent(this.adminToken)}`);
      const txs = await res.json();
      const tbody = document.getElementById('admin-tx-table-body');
      if (!tbody) return;

      if (!txs.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-6 text-gray-400">No transactions recorded yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = txs.map(t => `
        <tr class="border-b border-gray-100 dark:border-slate-800 text-xs">
          <td class="py-3 px-2 font-mono font-bold text-gray-900 dark:text-white">${t.tx_id}</td>
          <td class="py-3 px-2">
            <span class="font-bold block">${t.user_name}</span>
            <span class="text-[11px] text-gray-400 font-mono">Reg: ${t.reg_no || 'N/A'}</span>
          </td>
          <td class="py-3 px-2 font-semibold text-orange-600 dark:text-orange-400">${t.plan_name}</td>
          <td class="py-3 px-2 font-black text-emerald-600 dark:text-emerald-400">₹${t.amount}</td>
          <td class="py-3 px-2 font-mono text-[11px] text-gray-600 dark:text-slate-300">
            <span>${t.utr_ref || 'N/A'}</span>
            <span class="block text-[10px] text-gray-400">To: ${t.upi_destination}</span>
          </td>
          <td class="py-3 px-2">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${t.status === 'approved' ? 'bg-green-100 text-green-700 dark:bg-green-950/60 dark:text-green-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400'}">
              ${t.status.toUpperCase()}
            </span>
          </td>
          <td class="py-3 px-2">
            ${t.status !== 'approved' ? `
              <button onclick="AdminPortal.updateTxStatus('${t.tx_id}', 'approved')" class="px-2.5 py-1 rounded-lg text-[11px] font-bold bg-green-500 hover:bg-green-600 text-white transition-colors">
                Approve
              </button>
            ` : `
              <span class="text-xs text-gray-400">Active</span>
            `}
          </td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn("Transactions load error:", e);
    }
  },

  async updateTxStatus(txId, status) {
    try {
      const res = await fetch(`/api/admin/transactions/${txId}/status?token=${encodeURIComponent(this.adminToken)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });
      if (res.ok) {
        this.fetchStats();
        this.fetchTransactions();
        this.fetchUsers();
      }
    } catch (e) {
      alert("Failed to update transaction status.");
    }
  },

  async fetchUsers() {
    try {
      const res = await fetch(`/api/admin/users?token=${encodeURIComponent(this.adminToken)}`);
      const users = await res.json();
      const tbody = document.getElementById('admin-users-table-body');
      if (!tbody) return;

      if (!users.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-gray-400">No registered students yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = users.map(u => `
        <tr class="border-b border-gray-100 dark:border-slate-800 text-xs">
          <td class="py-3 px-2 flex items-center gap-2">
            <img src="${u.picture || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + u.email}" class="w-7 h-7 rounded-full object-cover">
            <div>
              <span class="font-bold block text-gray-900 dark:text-white">${u.name}</span>
              <span class="text-[10px] text-gray-400 font-mono">${u.email}</span>
            </div>
          </td>
          <td class="py-3 px-2 font-mono">${u.lpu_reg_no || 'N/A'}</td>
          <td class="py-3 px-2">${u.phone || 'N/A'}</td>
          <td class="py-3 px-2">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${u.is_pro ? 'bg-pink-100 text-pink-700 dark:bg-pink-950/60 dark:text-pink-400' : 'bg-gray-100 text-gray-600 dark:bg-slate-800 dark:text-slate-300'}">
              ${u.plan_name || 'Free Starter'}
            </span>
          </td>
          <td class="py-3 px-2 font-bold">${u.mock_tests_count || 0}</td>
          <td class="py-3 px-2">
            <button onclick="AdminPortal.promptGrantPlan('${u.id}', '${u.name}')" class="px-2 py-1 bg-pink-500 hover:bg-pink-600 text-white rounded-lg text-[10px] font-bold">
              + Grant Plan
            </button>
            <button onclick="AdminPortal.deleteUser('${u.id}')" class="px-2 py-1 text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-lg text-[10px] font-bold">
              Delete
            </button>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn("Users load error:", e);
    }
  },

  async promptGrantPlan(userId, userName) {
    const plan = prompt(`Grant plan to ${userName}:\n1: midterm_mock_49 (₹49 Mock Test Pass)\n2: educode_99 (₹99 EduCode Pass)\n3: neobrowser_99 (₹99 NeoBrowser Pass)\n4: semester_pro (All-Access VIP)`, "1");
    if (!plan) return;

    let planId = "midterm_mock_49";
    let planName = "Midterm Mode / Subject Mock Test Pass";
    if (plan === "2") {
      planId = "educode_99";
      planName = "EduCode Completion Support Pass";
    } else if (plan === "3") {
      planId = "neobrowser_99";
      planName = "NeoBrowser Completion Support Pass";
    } else if (plan === "4") {
      planId = "semester_pro";
      planName = "AcadAssist All-Access Semester Pro";
    }

    try {
      const res = await fetch(`/api/admin/users/${userId}/grant-plan?token=${encodeURIComponent(this.adminToken)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan_id: planId, plan_name: planName, duration_days: 180 })
      });
      if (res.ok) {
        alert(`Successfully granted ${planName} to ${userName}!`);
        this.fetchUsers();
        this.fetchStats();
      }
    } catch (e) {
      alert("Failed to grant plan.");
    }
  },

  async deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;
    try {
      const res = await fetch(`/api/admin/users/${userId}?token=${encodeURIComponent(this.adminToken)}`, {
        method: 'DELETE'
      });
      if (res.ok) {
        this.fetchUsers();
        this.fetchStats();
      }
    } catch (e) {
      alert("Failed to delete user.");
    }
  },

  async fetchMockTests() {
    try {
      const res = await fetch(`/api/admin/mock-tests?token=${encodeURIComponent(this.adminToken)}`);
      const tests = await res.json();
      const tbody = document.getElementById('admin-tests-table-body');
      if (!tbody) return;

      if (!tests.length) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-6 text-gray-400">No mock tests taken yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = tests.map(t => `
        <tr class="border-b border-gray-100 dark:border-slate-800 text-xs">
          <td class="py-3 px-2 font-bold">${t.user_name}</td>
          <td class="py-3 px-2 font-mono font-bold text-orange-600 dark:text-orange-400">${t.subject_code}</td>
          <td class="py-3 px-2">${t.score} / ${t.total_marks}</td>
          <td class="py-3 px-2 font-bold">${t.percentage}%</td>
          <td class="py-3 px-2">
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-purple-100 text-purple-700 dark:bg-purple-950/60 dark:text-purple-400">
              Grade ${t.grade}
            </span>
          </td>
          <td class="py-3 px-2 text-[10px] text-gray-400 font-mono">${t.formatted_time || 'Recent'}</td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn("Mock tests load error:", e);
    }
  },

  async fetchServiceRequests() {
    try {
      const res = await fetch(`/api/admin/service-requests?token=${encodeURIComponent(this.adminToken)}`);
      const inqs = await res.json();
      const tbody = document.getElementById('admin-inquiries-table-body');
      if (!tbody) return;

      if (!inqs.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-6 text-gray-400">No service inquiries yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = inqs.map(i => `
        <tr class="border-b border-gray-100 dark:border-slate-800 text-xs">
          <td class="py-3 px-2 font-bold text-gray-900 dark:text-white">${i.service_category}</td>
          <td class="py-3 px-2">
            <span class="font-bold">${i.student_name}</span>
            <span class="block text-[10px] text-gray-400 font-mono">${i.phone}</span>
          </td>
          <td class="py-3 px-2 font-semibold text-orange-500">${i.subject_or_topic || 'General'}</td>
          <td class="py-3 px-2 max-w-xs truncate text-[11px] text-gray-600 dark:text-slate-300" title="${i.details}">${i.details}</td>
          <td class="py-3 px-2 font-mono text-[10px] text-gray-400">${i.deadline || 'Flexible'}</td>
          <td class="py-3 px-2">
            <select onchange="AdminPortal.updateInquiryStatus('${i.id}', this.value)" class="text-[10px] p-1 rounded border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 font-bold">
              <option value="New" ${i.status === 'New' ? 'selected' : ''}>New</option>
              <option value="In Progress" ${i.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
              <option value="Completed" ${i.status === 'Completed' ? 'selected' : ''}>Completed</option>
            </select>
          </td>
          <td class="py-3 px-2">
            <a href="https://wa.me/91${i.phone.replace(/[^0-9]/g, '')}?text=Hi%20${encodeURIComponent(i.student_name)}%2C%20regarding%20your%20AcadAssist%20order%20for%20${encodeURIComponent(i.service_category)}" target="_blank" class="px-2.5 py-1 bg-green-500 hover:bg-green-600 text-white rounded-lg text-[10px] font-bold inline-flex items-center gap-1">
              <span>💬 WhatsApp</span>
            </a>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn("Service inquiries load error:", e);
    }
  },

  async updateInquiryStatus(inqId, status) {
    try {
      await fetch(`/api/admin/service-requests/${inqId}/status?token=${encodeURIComponent(this.adminToken)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });
      this.fetchStats();
    } catch (e) {
      alert("Failed to update inquiry status.");
    }
  },

  async exportData() {
    try {
      const res = await fetch(`/api/admin/export?token=${encodeURIComponent(this.adminToken)}`);
      const data = await res.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `acadassist_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert("Export failed.");
    }
  },

  logout() {
    this.adminToken = null;
    localStorage.removeItem(this.TOKEN_KEY);
    document.getElementById('admin-dashboard-modal')?.close();
    alert("Admin logged out.");
  }
};

window.AdminPortal = AdminPortal;
document.addEventListener('DOMContentLoaded', () => AdminPortal.init());
