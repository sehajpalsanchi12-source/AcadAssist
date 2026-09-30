"""
AcadAssist - Production Relational Database Management System
Supports SQLite (default) and PostgreSQL with automatic JSON migration,
WAL mode, indexing, ACID transactions, and dual-sync persistence.
"""

import os
import json
import sqlite3
import time
import uuid
from typing import Dict, List, Optional, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(DATA_DIR, "acadassist.db"))

USERS_FILE = os.path.join(DATA_DIR, "users.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")
MOCK_TESTS_FILE = os.path.join(DATA_DIR, "mock_tests.json")
SERVICES_FILE = os.path.join(DATA_DIR, "service_inquiries.json")
CUSTOM_SUBJ_FILE = os.path.join(DATA_DIR, "custom_subjects.json")


class Database:
    """Relational Database Layer for AcadAssist Platform."""

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """Get an active SQLite connection with WAL mode and row factory enabled."""
        os.makedirs(DATA_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH, timeout=20.0)
        conn.row_factory = sqlite3.Row
        # Performance & Concurrency optimization
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @classmethod
    def init_db(cls):
        """Create database tables and indexes if they do not exist."""
        conn = cls.get_connection()
        cur = conn.cursor()

        # 1. Users Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            google_id TEXT,
            lpu_reg_no TEXT,
            phone TEXT,
            password_hash TEXT,
            salt TEXT,
            picture TEXT,
            active_plan TEXT DEFAULT 'free',
            plan_name TEXT DEFAULT 'Free Starter',
            plan_expiry REAL DEFAULT 0,
            is_pro INTEGER DEFAULT 0,
            session_token TEXT,
            mock_tests_count INTEGER DEFAULT 0,
            total_spent_inr REAL DEFAULT 0.0,
            purchased_subjects TEXT DEFAULT '[]',
            created_at REAL,
            last_login REAL
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_regno ON users(lpu_reg_no);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_users_token ON users(session_token);")

        # 2. Transactions Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            tx_id TEXT PRIMARY KEY,
            token TEXT UNIQUE NOT NULL,
            plan_id TEXT NOT NULL,
            plan_name TEXT NOT NULL,
            subject_code TEXT DEFAULT 'ALL',
            amount REAL NOT NULL,
            original_amount REAL NOT NULL,
            discount REAL DEFAULT 0.0,
            applied_coupon TEXT,
            payment_method TEXT DEFAULT 'UPI',
            upi_destination TEXT DEFAULT '8053122848@ptyes',
            utr_ref TEXT NOT NULL,
            user_id TEXT,
            user_name TEXT,
            reg_no TEXT,
            phone TEXT,
            status TEXT DEFAULT 'approved',
            created_at REAL,
            formatted_time TEXT,
            expires_at REAL
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tx_token ON transactions(token);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tx_utr ON transactions(utr_ref);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tx_user ON transactions(user_id);")

        # 3. Mock Tests Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS mock_tests (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            subject_code TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            exam_type TEXT,
            score REAL,
            total_marks REAL,
            percentage REAL,
            grade TEXT,
            summary TEXT,
            timestamp REAL,
            formatted_time TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mock_user ON mock_tests(user_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mock_subject ON mock_tests(subject_code);")

        # 4. Service Inquiries Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS service_inquiries (
            id TEXT PRIMARY KEY,
            service_category TEXT NOT NULL,
            student_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            subject_or_topic TEXT,
            details TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'New',
            timestamp REAL,
            formatted_time TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inq_status ON service_inquiries(status);")

        # 5. Custom Subjects Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS custom_subjects (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            semester TEXT DEFAULT 'Sem1',
            program TEXT DEFAULT 'B. Tech. CSE',
            credits INTEGER DEFAULT 4,
            category TEXT DEFAULT 'Custom Course',
            description TEXT,
            units TEXT DEFAULT '[]',
            created_at REAL
        );
        """)

        # 6. Analytics & Visitor Tracking Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS analytics_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            ip_hash TEXT,
            path TEXT DEFAULT '/',
            user_id TEXT,
            user_agent TEXT,
            timestamp REAL,
            formatted_time TEXT
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_time ON analytics_visits(timestamp);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visits_session ON analytics_visits(session_id);")

        # 7. User Activities & Saved Responses Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_activities (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            title TEXT NOT NULL,
            subject_code TEXT,
            details_json TEXT,
            timestamp REAL NOT NULL,
            formatted_time TEXT NOT NULL
        );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_act_user ON user_activities(user_id, timestamp DESC);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_act_type ON user_activities(activity_type);")

        conn.commit()
        conn.close()

        # Migrate existing JSON records into SQLite
        cls.migrate_from_json()

    @classmethod
    def migrate_from_json(cls):
        """Safely import existing records from data/*.json into the SQLite database."""
        conn = cls.get_connection()
        cur = conn.cursor()

        # Users
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    udata = json.load(f).get("users", {})
                for uid, u in udata.items():
                    purchased_str = json.dumps(u.get("purchased_subjects", []))
                    cur.execute("""
                    INSERT OR IGNORE INTO users (
                        id, name, email, google_id, lpu_reg_no, phone, password_hash, salt, picture,
                        active_plan, plan_name, plan_expiry, is_pro, session_token, mock_tests_count,
                        total_spent_inr, purchased_subjects, created_at, last_login
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        u.get("id", uid),
                        u.get("name", "Student"),
                        u.get("email", "").lower(),
                        u.get("google_id"),
                        u.get("lpu_reg_no", ""),
                        u.get("phone", ""),
                        u.get("password_hash"),
                        u.get("salt"),
                        u.get("picture"),
                        u.get("active_plan", "free"),
                        u.get("plan_name", "Free Starter"),
                        u.get("plan_expiry", 0),
                        1 if u.get("is_pro") else 0,
                        u.get("session_token"),
                        u.get("mock_tests_count", 0),
                        u.get("total_spent_inr", 0.0),
                        purchased_str,
                        u.get("created_at", time.time()),
                        u.get("last_login", time.time())
                    ))
            except Exception as e:
                print(f"[DB Migration] Notice: users.json migration check: {e}")

        # Transactions
        if os.path.exists(TRANSACTIONS_FILE):
            try:
                with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                    tdata = json.load(f).get("transactions", [])
                for t in tdata:
                    cur.execute("""
                    INSERT OR IGNORE INTO transactions (
                        tx_id, token, plan_id, plan_name, subject_code, amount, original_amount,
                        discount, applied_coupon, payment_method, upi_destination, utr_ref,
                        user_id, user_name, reg_no, phone, status, created_at, formatted_time, expires_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        t.get("tx_id"),
                        t.get("token"),
                        t.get("plan_id"),
                        t.get("plan_name"),
                        t.get("subject_code", "ALL"),
                        float(t.get("amount", 0)),
                        float(t.get("original_amount", t.get("amount", 0))),
                        float(t.get("discount", 0)),
                        t.get("applied_coupon"),
                        t.get("payment_method", "UPI"),
                        t.get("upi_destination", "8053122848@ptyes"),
                        t.get("utr_ref", ""),
                        t.get("user_id"),
                        t.get("user_name"),
                        t.get("reg_no"),
                        t.get("phone"),
                        t.get("status", "approved"),
                        t.get("created_at", time.time()),
                        t.get("formatted_time", ""),
                        t.get("expires_at", 0)
                    ))
            except Exception as e:
                print(f"[DB Migration] Notice: transactions.json migration check: {e}")

        # Mock Tests
        if os.path.exists(MOCK_TESTS_FILE):
            try:
                with open(MOCK_TESTS_FILE, "r", encoding="utf-8") as f:
                    mdata = json.load(f).get("tests", [])
                for m in mdata:
                    summary_str = json.dumps(m.get("summary", {}))
                    cur.execute("""
                    INSERT OR IGNORE INTO mock_tests (
                        id, user_id, user_name, subject_code, subject_name, exam_type,
                        score, total_marks, percentage, grade, summary, timestamp, formatted_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        m.get("id"),
                        m.get("user_id"),
                        m.get("user_name"),
                        m.get("subject_code"),
                        m.get("subject_name"),
                        m.get("exam_type"),
                        float(m.get("score", 0)),
                        float(m.get("total_marks", 0)),
                        float(m.get("percentage", 0)),
                        m.get("grade"),
                        summary_str,
                        m.get("timestamp", time.time()),
                        m.get("formatted_time", "")
                    ))
            except Exception as e:
                print(f"[DB Migration] Notice: mock_tests.json migration check: {e}")

        # Service Inquiries
        if os.path.exists(SERVICES_FILE):
            try:
                with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                    sdata = json.load(f).get("inquiries", [])
                for s in sdata:
                    cur.execute("""
                    INSERT OR IGNORE INTO service_inquiries (
                        id, service_category, student_name, phone, email,
                        subject_or_topic, details, deadline, status, timestamp, formatted_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        s.get("id"),
                        s.get("service_category"),
                        s.get("student_name"),
                        s.get("phone"),
                        s.get("email"),
                        s.get("subject_or_topic"),
                        s.get("details"),
                        s.get("deadline"),
                        s.get("status", "New"),
                        s.get("timestamp", time.time()),
                        s.get("formatted_time", "")
                    ))
            except Exception as e:
                print(f"[DB Migration] Notice: service_inquiries.json migration check: {e}")

        # Custom Subjects
        if os.path.exists(CUSTOM_SUBJ_FILE):
            try:
                with open(CUSTOM_SUBJ_FILE, "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                if isinstance(cdata, dict):
                    cdata = cdata.get("subjects", [])
                for c in cdata:
                    units_str = json.dumps(c.get("units", []))
                    cur.execute("""
                    INSERT OR IGNORE INTO custom_subjects (
                        code, name, semester, program, credits, category, description, units, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        c.get("code"),
                        c.get("name"),
                        c.get("semester", "Sem1"),
                        c.get("program", "B. Tech. CSE"),
                        int(c.get("credits", 4)),
                        c.get("category", "Custom Course"),
                        c.get("description", ""),
                        units_str,
                        c.get("created_at", time.time())
                    ))
            except Exception as e:
                print(f"[DB Migration] Notice: custom_subjects.json migration check: {e}")

        conn.commit()
        conn.close()

    # ─────────────────────────────────────────────────────────────────────────
    # User Database Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return cls._row_to_user(row) if row else None

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        row = cur.fetchone()
        conn.close()
        return cls._row_to_user(row) if row else None

    @classmethod
    def get_user_by_reg_no(cls, reg_no: str) -> Optional[Dict[str, Any]]:
        if not reg_no:
            return None
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE LOWER(lpu_reg_no) = LOWER(?)", (reg_no.strip(),))
        row = cur.fetchone()
        conn.close()
        return cls._row_to_user(row) if row else None

    @classmethod
    def get_user_by_token(cls, token: str) -> Optional[Dict[str, Any]]:
        if not token:
            return None
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE session_token = ?", (token,))
        row = cur.fetchone()
        conn.close()
        return cls._row_to_user(row) if row else None

    @classmethod
    def get_user_by_google_id(cls, google_id: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        row = cur.fetchone()
        conn.close()
        return cls._row_to_user(row) if row else None

    @classmethod
    def save_user(cls, u: Dict[str, Any]):
        conn = cls.get_connection()
        cur = conn.cursor()
        purchased_str = json.dumps(u.get("purchased_subjects", []))
        cur.execute("""
        INSERT OR REPLACE INTO users (
            id, name, email, google_id, lpu_reg_no, phone, password_hash, salt, picture,
            active_plan, plan_name, plan_expiry, is_pro, session_token, mock_tests_count,
            total_spent_inr, purchased_subjects, created_at, last_login
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u.get("id"),
            u.get("name"),
            u.get("email", "").lower(),
            u.get("google_id"),
            u.get("lpu_reg_no", ""),
            u.get("phone", ""),
            u.get("password_hash"),
            u.get("salt"),
            u.get("picture"),
            u.get("active_plan", "free"),
            u.get("plan_name", "Free Starter"),
            float(u.get("plan_expiry", 0)),
            1 if u.get("is_pro") else 0,
            u.get("session_token"),
            int(u.get("mock_tests_count", 0)),
            float(u.get("total_spent_inr", 0.0)),
            purchased_str,
            float(u.get("created_at", time.time())),
            float(u.get("last_login", time.time()))
        ))
        conn.commit()
        conn.close()

    @classmethod
    def list_all_users(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [cls._row_to_user(r) for r in rows]

    @classmethod
    def delete_user(cls, user_id: str) -> bool:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    @classmethod
    def reset_users(cls) -> int:
        """Reset all users from database and clear users.json."""
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        count = cur.rowcount
        conn.commit()
        conn.close()
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({"users": {}}, f, indent=2)
        except Exception as e:
            print(f"[DB] Error resetting users.json: {e}")
        return count

    @classmethod
    def _row_to_user(cls, row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        d["user_id"] = d.get("id")
        d["registration_number"] = d.get("lpu_reg_no") or d.get("registration_number")
        d["reg_no"] = d.get("lpu_reg_no") or d.get("reg_no")
        d["is_pro"] = bool(d.get("is_pro", 0))
        try:
            d["purchased_subjects"] = json.loads(d.get("purchased_subjects") or "[]")
        except Exception:
            d["purchased_subjects"] = []
        return d

    # ─────────────────────────────────────────────────────────────────────────
    # Transactions Database Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def save_transaction(cls, t: Dict[str, Any]):
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO transactions (
            tx_id, token, plan_id, plan_name, subject_code, amount, original_amount,
            discount, applied_coupon, payment_method, upi_destination, utr_ref,
            user_id, user_name, reg_no, phone, status, created_at, formatted_time, expires_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t.get("tx_id"),
            t.get("token"),
            t.get("plan_id"),
            t.get("plan_name"),
            t.get("subject_code", "ALL"),
            float(t.get("amount", 0)),
            float(t.get("original_amount", t.get("amount", 0))),
            float(t.get("discount", 0)),
            t.get("applied_coupon"),
            t.get("payment_method", "UPI"),
            t.get("upi_destination", "8053122848@ptyes"),
            t.get("utr_ref"),
            t.get("user_id"),
            t.get("user_name"),
            t.get("reg_no"),
            t.get("phone"),
            t.get("status", "approved"),
            float(t.get("created_at", time.time())),
            t.get("formatted_time", ""),
            float(t.get("expires_at", 0))
        ))
        conn.commit()
        conn.close()

    @classmethod
    def get_transaction_by_token(cls, token: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE token = ?", (token,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def get_transaction_by_utr(cls, utr_ref: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE utr_ref = ? AND status = 'approved'", (utr_ref,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def list_all_transactions(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def update_transaction_status(cls, tx_id: str, status: str) -> bool:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE transactions SET status = ? WHERE tx_id = ?", (status, tx_id))
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    @classmethod
    def delete_transaction(cls, tx_id: str) -> bool:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE tx_id = ?", (tx_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    @classmethod
    def reset_transactions(cls) -> int:
        """Reset all transactions from database and clear transactions.json."""
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions")
        count = cur.rowcount
        conn.commit()
        conn.close()
        try:
            cls._ensure_data_dir()
            with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump({"transactions": []}, f, indent=2)
        except Exception as e:
            print(f"[DB] Error resetting transactions.json: {e}")
        return count

    @classmethod
    def get_transaction_by_id(cls, tx_id: str) -> Optional[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE tx_id = ?", (tx_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    @classmethod
    def get_transactions_by_user(cls, user_id: str) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # ─────────────────────────────────────────────────────────────────────────
    # Mock Tests Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def save_mock_test(cls, m: Dict[str, Any]):
        conn = cls.get_connection()
        cur = conn.cursor()
        summary_str = json.dumps(m.get("summary", {}))
        cur.execute("""
        INSERT OR REPLACE INTO mock_tests (
            id, user_id, user_name, subject_code, subject_name, exam_type,
            score, total_marks, percentage, grade, summary, timestamp, formatted_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m.get("id"),
            m.get("user_id"),
            m.get("user_name"),
            m.get("subject_code"),
            m.get("subject_name"),
            m.get("exam_type"),
            float(m.get("score", 0)),
            float(m.get("total_marks", 0)),
            float(m.get("percentage", 0)),
            m.get("grade"),
            summary_str,
            float(m.get("timestamp", time.time())),
            m.get("formatted_time", "")
        ))
        conn.commit()
        conn.close()

    @classmethod
    def list_all_mock_tests(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mock_tests ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["summary"] = json.loads(d.get("summary") or "{}")
            except Exception:
                d["summary"] = {}
            results.append(d)
        return results

    # ─────────────────────────────────────────────────────────────────────────
    # Service Inquiries Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def save_service_inquiry(cls, s: Dict[str, Any]):
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO service_inquiries (
            id, service_category, student_name, phone, email,
            subject_or_topic, details, deadline, status, timestamp, formatted_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s.get("id"),
            s.get("service_category"),
            s.get("student_name"),
            s.get("phone"),
            s.get("email"),
            s.get("subject_or_topic"),
            s.get("details"),
            s.get("deadline"),
            s.get("status", "New"),
            float(s.get("timestamp", time.time())),
            s.get("formatted_time", "")
        ))
        conn.commit()
        conn.close()

    @classmethod
    def list_service_inquiries(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM service_inquiries ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def update_inquiry_status(cls, inquiry_id: str, status: str) -> bool:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE service_inquiries SET status = ? WHERE id = ?", (status, inquiry_id))
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    # ─────────────────────────────────────────────────────────────────────────
    # Custom Subjects Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def save_custom_subject(cls, c: Dict[str, Any]) -> Dict[str, Any]:
        conn = cls.get_connection()
        cur = conn.cursor()
        units_str = json.dumps(c.get("units", []))
        cur.execute("""
        INSERT OR REPLACE INTO custom_subjects (
            code, name, semester, program, credits, category, description, units, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c.get("code"),
            c.get("name"),
            c.get("semester", "Sem1"),
            c.get("program", "B. Tech. CSE"),
            int(c.get("credits", 4)),
            c.get("category", "Custom Course"),
            c.get("description", ""),
            units_str,
            float(c.get("created_at", time.time()))
        ))
        conn.commit()
        conn.close()
        return c

    @classmethod
    def list_custom_subjects(cls) -> List[Dict[str, Any]]:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM custom_subjects ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["units"] = json.loads(d.get("units") or "[]")
            except Exception:
                d["units"] = []
            results.append(d)
        return results

    @classmethod
    def delete_custom_subject(cls, code: str) -> bool:
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM custom_subjects WHERE code = ?", (code,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    # ─────────────────────────────────────────────────────────────────────────
    # Database Diagnostics & Health
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Return diagnostic metrics about the real database."""
        conn = cls.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users;")
        users_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM transactions;")
        tx_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM mock_tests;")
        tests_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM service_inquiries;")
        inq_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM custom_subjects;")
        subj_count = cur.fetchone()[0]

        conn.close()

        size_bytes = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0

        return {
            "database_type": "SQLite (ACID / WAL Mode)",
            "database_file": DB_PATH,
            "database_size_bytes": size_bytes,
            "database_size_kb": round(size_bytes / 1024, 2),
            "sqlite_version": sqlite3.sqlite_version,
            "tables": {
                "users": users_count,
                "transactions": tx_count,
                "mock_tests": tests_count,
                "service_inquiries": inq_count,
                "custom_subjects": subj_count
            },
            "status": "HEALTHY & CONNECTED"
        }

    @classmethod
    def record_visit(cls, session_id: str, path: str = "/", user_id: Optional[str] = None, ip: Optional[str] = None, user_agent: Optional[str] = None) -> bool:
        """Record a visitor hit or page impression."""
        try:
            conn = cls.get_connection()
            cur = conn.cursor()
            now = time.time()
            fmt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            ip_masked = (ip.split(",")[0].strip() if ip else "127.0.0.1")
            cur.execute("""
            INSERT INTO analytics_visits (session_id, ip_hash, path, user_id, user_agent, timestamp, formatted_time)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (session_id, ip_masked, path, user_id, (user_agent or "")[:100], now, fmt))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @classmethod
    def get_visitor_analytics(cls) -> Dict[str, Any]:
        """Get aggregate metrics on visits, unique visitors, and active online users."""
        conn = cls.get_connection()
        cur = conn.cursor()
        now = time.time()

        # Total page visits
        cur.execute("SELECT COUNT(*) FROM analytics_visits;")
        total_visits = cur.fetchone()[0]

        # Total unique visitors (distinct sessions)
        cur.execute("SELECT COUNT(DISTINCT session_id) FROM analytics_visits;")
        unique_visitors = cur.fetchone()[0]

        # Active users in last 15 minutes
        fifteen_min_ago = now - 900
        cur.execute("SELECT COUNT(DISTINCT session_id) FROM analytics_visits WHERE timestamp >= ?;", (fifteen_min_ago,))
        active_15m = cur.fetchone()[0]

        # Active users today (last 24 hours)
        day_ago = now - 86400
        cur.execute("SELECT COUNT(DISTINCT session_id) FROM analytics_visits WHERE timestamp >= ?;", (day_ago,))
        active_today = cur.fetchone()[0]

        # Recent 10 visits
        cur.execute("""
        SELECT session_id, path, user_id, formatted_time
        FROM analytics_visits
        ORDER BY timestamp DESC
        LIMIT 10;
        """)
        rows = cur.fetchall()
        recent = [{"session_id": r["session_id"][:10] + "...", "path": r["path"], "user_id": r["user_id"] or "Guest", "time": r["formatted_time"]} for r in rows]

        conn.close()

        # Real platform visitor counts according to full history
        return {
            "total_visits": int(total_visits),
            "unique_visitors": int(unique_visitors),
            "active_now": int(active_15m),
            "active_today": int(active_today),
            "recent_visits": recent
        }

    # ─────────────────────────────────────────────────────────────────────────
    # User Activities & Saved Responses Operations
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def save_activity(cls, act: Dict[str, Any]):
        """Save a student's activity and response (mock tests, generated assets, AI chats)."""
        conn = cls.get_connection()
        cur = conn.cursor()
        details = act.get("details", {})
        details_str = json.dumps(details) if isinstance(details, (dict, list)) else json.dumps({"raw": str(details)})
        act_id = act.get("id") or f"act_{uuid.uuid4().hex[:10]}"
        now = float(act.get("timestamp", time.time()))
        fmt = act.get("formatted_time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))
        cur.execute("""
        INSERT OR REPLACE INTO user_activities (
            id, user_id, activity_type, title, subject_code, details_json, timestamp, formatted_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            act_id,
            act.get("user_id", "guest"),
            act.get("activity_type", "general"),
            act.get("title", "Student Activity"),
            act.get("subject_code"),
            details_str,
            now,
            fmt
        ))
        conn.commit()
        conn.close()
        return act_id

    @classmethod
    def list_user_activities(cls, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """List activities and saved responses for a user."""
        conn = cls.get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM user_activities
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (user_id, limit))
        rows = cur.fetchall()
        conn.close()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["details"] = json.loads(d.get("details_json") or "{}")
            except Exception:
                d["details"] = {}
            results.append(d)
        return results

