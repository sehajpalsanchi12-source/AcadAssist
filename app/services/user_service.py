import os
import json
import time
import uuid
import hashlib
import secrets
from typing import Dict, List, Optional, Any

from app.database import Database

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MOCK_TESTS_FILE = os.path.join(DATA_DIR, "mock_tests.json")
SERVICES_FILE = os.path.join(DATA_DIR, "service_inquiries.json")

class UserService:
    """Manages student profiles, secure authentication, mock test submissions, and service requests."""

    @classmethod
    def _hash_password(cls, password: str, salt: Optional[str] = None) -> tuple:
        """Hash a password using PBKDF2-HMAC-SHA256 with 100,000 iterations."""
        if not salt:
            salt = secrets.token_hex(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000)
        return dk.hex(), salt

    @classmethod
    def _verify_password(cls, password: str, salt: str, password_hash: str) -> bool:
        """Securely verify password hash using constant-time comparison."""
        if not salt or not password_hash:
            return False
        try:
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000)
            return secrets.compare_digest(dk.hex(), password_hash)
        except Exception:
            return False

    @classmethod
    def safe_user(cls, user: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Strip sensitive credentials (password hash, salt) from user object before sending to clients."""
        if not user:
            return None
        safe = dict(user)
        safe.pop("password_hash", None)
        safe.pop("salt", None)
        return safe

    @classmethod
    def _ensure_files(cls):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump({"users": {}}, f, indent=2)
        if not os.path.exists(MOCK_TESTS_FILE):
            with open(MOCK_TESTS_FILE, "w", encoding="utf-8") as f:
                json.dump({"tests": []}, f, indent=2)
        if not os.path.exists(SERVICES_FILE):
            with open(SERVICES_FILE, "w", encoding="utf-8") as f:
                json.dump({"inquiries": []}, f, indent=2)

    @classmethod
    def _read_users(cls) -> Dict[str, Any]:
        cls._ensure_files()
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}}

    @classmethod
    def _write_users(cls, data: Dict[str, Any]):
        cls._ensure_files()
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def register_user(
        cls,
        name: str,
        email: str,
        password: str,
        lpu_reg_no: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register a new student with salted PBKDF2 password hashing."""
        name = (name or "").strip()
        email = (email or "").strip().lower()
        password = (password or "").strip()
        lpu_reg_no = (lpu_reg_no or "").strip()
        phone = (phone or "").strip()

        if not name:
            return {"success": False, "message": "Please enter your full name."}
        if not email or "@" not in email or "." not in email:
            return {"success": False, "message": "Please provide a valid email address."}
        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters long."}

        # Check for existing email or reg no in DB and JSON
        if Database.get_user_by_email(email):
            return {"success": False, "message": "An account with this email already exists. Please sign in."}
        if lpu_reg_no and Database.get_user_by_reg_no(lpu_reg_no):
            return {"success": False, "message": "An account with this LPU Registration Number already exists. Please sign in."}

        data = cls._read_users()
        users = data.get("users", {})

        for uid, u in users.items():
            if u.get("email", "").lower() == email:
                return {"success": False, "message": "An account with this email already exists. Please sign in."}
            if lpu_reg_no and u.get("lpu_reg_no") and u.get("lpu_reg_no") == lpu_reg_no:
                return {"success": False, "message": "An account with this LPU Registration Number already exists. Please sign in."}

        now = time.time()
        session_token = f"acad_usr_{uuid.uuid4().hex}"
        pwd_hash, salt = cls._hash_password(password)
        user_id = f"user_{uuid.uuid4().hex[:10]}"

        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "picture": f"https://api.dicebear.com/7.x/bottts/svg?seed={email}",
            "lpu_reg_no": lpu_reg_no,
            "phone": phone,
            "password_hash": pwd_hash,
            "salt": salt,
            "created_at": now,
            "last_login": now,
            "active_plan": "free",
            "plan_name": "Free Starter",
            "plan_expiry": 0,
            "is_pro": False,
            "session_token": session_token,
            "mock_tests_count": 0,
            "total_spent_inr": 0,
            "purchased_subjects": []
        }

        # 1. Primary write to SQLite Relational Database
        Database.save_user(user)

        # 2. Dual-sync write to users.json for backward compatibility
        users[user_id] = user
        data["users"] = users
        cls._write_users(data)

        return {
            "success": True,
            "message": "Account created successfully.",
            "user": cls.safe_user(user),
            "session_token": session_token
        }

    @classmethod
    def login_user(cls, identifier: str, password: str) -> Dict[str, Any]:
        """Authenticate user by Email or LPU Registration Number and verify password."""
        identifier = (identifier or "").strip().lower()
        password = (password or "").strip()

        if not identifier:
            return {"success": False, "message": "Please enter your Email or LPU Registration Number."}
        if not password:
            return {"success": False, "message": "Please enter your password."}

        # Query Database first
        target_user = Database.get_user_by_email(identifier) or Database.get_user_by_reg_no(identifier)

        if not target_user:
            # Fallback check in JSON
            data = cls._read_users()
            users = data.get("users", {})
            for uid, u in users.items():
                u_email = u.get("email", "").lower()
                u_reg = (u.get("lpu_reg_no") or "").lower()
                if u_email == identifier or (u_reg and u_reg == identifier):
                    target_user = u
                    break

        if not target_user:
            return {"success": False, "message": "No account found with this email or registration number. Please create an account."}

        stored_hash = target_user.get("password_hash")
        stored_salt = target_user.get("salt")

        if not stored_hash or not stored_salt:
            return {
                "success": False,
                "message": "This account was registered via Google Sign-In. Please sign in with Google or reset your password."
            }

        if not cls._verify_password(password, stored_salt, stored_hash):
            return {"success": False, "message": "Incorrect password. Please try again."}

        now = time.time()
        session_token = f"acad_usr_{uuid.uuid4().hex}"
        target_user["last_login"] = now
        target_user["session_token"] = session_token

        # Save to SQLite Database
        Database.save_user(target_user)

        # Dual-sync to JSON
        data = cls._read_users()
        users = data.get("users", {})
        users[target_user["id"]] = target_user
        data["users"] = users
        cls._write_users(data)

        return {
            "success": True,
            "message": "Logged in successfully.",
            "user": cls.safe_user(target_user),
            "session_token": session_token
        }

    @classmethod
    def google_auth(
        cls,
        google_id: str,
        name: str,
        email: str,
        picture: Optional[str] = None,
        lpu_reg_no: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """Sign in or register a user with Google credentials."""
        now = time.time()
        session_token = f"acad_usr_{uuid.uuid4().hex}"

        # Check in Database first
        user = Database.get_user_by_google_id(google_id) or Database.get_user_by_email(email)

        if not user:
            user_id = f"user_{uuid.uuid4().hex[:10]}"
            user = {
                "id": user_id,
                "google_id": google_id,
                "name": name,
                "email": email.lower(),
                "picture": picture or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}",
                "lpu_reg_no": lpu_reg_no or "",
                "phone": phone or "",
                "created_at": now,
                "last_login": now,
                "active_plan": "free",
                "plan_name": "Free Starter",
                "plan_expiry": 0,
                "is_pro": False,
                "session_token": session_token,
                "mock_tests_count": 0,
                "total_spent_inr": 0,
                "purchased_subjects": []
            }
        else:
            user["name"] = name or user.get("name")
            user["picture"] = picture or user.get("picture")
            if lpu_reg_no:
                user["lpu_reg_no"] = lpu_reg_no
            if phone:
                user["phone"] = phone
            user["last_login"] = now
            user["session_token"] = session_token

        # Save to Database
        Database.save_user(user)

        # Dual-sync to JSON
        data = cls._read_users()
        users = data.get("users", {})
        users[user["id"]] = user
        data["users"] = users
        cls._write_users(data)

        return {
            "success": True,
            "user": cls.safe_user(user),
            "session_token": session_token
        }

    @classmethod
    def get_user_by_token(cls, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """Look up active user by session token from real database (with JSON fallback)."""
        if not token:
            return None

        # Check SQLite Database first
        user = Database.get_user_by_token(token)

        # Fallback to JSON if not yet in SQLite
        if not user:
            data = cls._read_users()
            users = data.get("users", {})
            for _, u in users.items():
                if u.get("session_token") == token:
                    user = u
                    break

        if user:
            # Check if plan expired
            if user.get("plan_expiry", 0) > 0 and time.time() > user["plan_expiry"]:
                user["is_pro"] = False
                user["active_plan"] = "free"
                user["plan_name"] = "Free Starter"
                Database.save_user(user)

                data = cls._read_users()
                if user.get("id") in data.get("users", {}):
                    data["users"][user["id"]] = user
                    cls._write_users(data)

            return cls.safe_user(user)

        return None

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Fetch user by primary key ID."""
        user = Database.get_user_by_id(user_id)
        if not user:
            data = cls._read_users()
            user = data.get("users", {}).get(user_id)
        return cls.safe_user(user)

    @classmethod
    def update_profile(cls, user_id: str, lpu_reg_no: Optional[str] = None, phone: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
        """Update student profile details in database."""
        user = Database.get_user_by_id(user_id)
        data = cls._read_users()
        users = data.get("users", {})

        if not user and user_id in users:
            user = users[user_id]

        if not user:
            return {"success": False, "message": "User not found"}

        if lpu_reg_no:
            user["lpu_reg_no"] = lpu_reg_no
        if phone:
            user["phone"] = phone
        if name:
            user["name"] = name

        # Persist to Database & JSON
        Database.save_user(user)
        users[user_id] = user
        data["users"] = users
        cls._write_users(data)

        return {"success": True, "user": cls.safe_user(user)}

    @classmethod
    def grant_user_plan(
        cls,
        user_id: str,
        plan_id: str,
        plan_name: str,
        duration_days: int = 180,
        amount_paid: float = 0.0,
        subject_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upgrade user to paid plan or subject mock test pass in database."""
        user = Database.get_user_by_id(user_id)
        data = cls._read_users()
        users = data.get("users", {})

        if not user and user_id in users:
            user = users[user_id]

        if not user:
            return {"success": False, "message": "User not found"}

        user["active_plan"] = plan_id
        user["plan_name"] = plan_name
        user["plan_expiry"] = time.time() + (duration_days * 86400)
        user["is_pro"] = True
        user["total_spent_inr"] = float(user.get("total_spent_inr", 0)) + float(amount_paid)

        if subject_code:
            purchased = user.get("purchased_subjects", [])
            if subject_code not in purchased:
                purchased.append(subject_code)
            user["purchased_subjects"] = purchased

        # Persist to Database & JSON
        Database.save_user(user)
        users[user_id] = user
        data["users"] = users
        cls._write_users(data)

        return {"success": True, "user": cls.safe_user(user)}

    @classmethod
    def list_all_users(cls) -> List[Dict[str, Any]]:
        """List all users from database."""
        db_users = Database.list_all_users()
        if db_users:
            return [cls.safe_user(u) for u in db_users]
        data = cls._read_users()
        return [cls.safe_user(u) for u in data.get("users", {}).values()]

    @classmethod
    def delete_user(cls, user_id: str) -> bool:
        """Delete user by ID from database and file."""
        deleted_db = Database.delete_user(user_id)
        data = cls._read_users()
        users = data.get("users", {})
        deleted_json = False
        if user_id in users:
            del users[user_id]
            data["users"] = users
            cls._write_users(data)
            deleted_json = True
        return deleted_db or deleted_json

    # ── Mock Tests Storage ──

    @classmethod
    def record_mock_test(
        cls,
        user_id: Optional[str],
        user_name: str,
        subject_code: str,
        subject_name: str,
        exam_type: str,
        score: float,
        total_marks: float,
        percentage: float,
        grade: str,
        summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save student mock test result into SQLite relational database and JSON."""
        test_record = {
            "id": f"test_{uuid.uuid4().hex[:10]}",
            "user_id": user_id or "guest",
            "user_name": user_name,
            "subject_code": subject_code,
            "subject_name": subject_name,
            "exam_type": exam_type,
            "score": score,
            "total_marks": total_marks,
            "percentage": percentage,
            "grade": grade,
            "summary": summary,
            "timestamp": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 1. Primary write to SQLite Relational Database
        Database.save_mock_test(test_record)

        # 2. Dual-sync write to mock_tests.json
        cls._ensure_files()
        try:
            with open(MOCK_TESTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"tests": []}
        data.setdefault("tests", []).insert(0, test_record)
        with open(MOCK_TESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Increment user count if registered
        if user_id and user_id != "guest":
            user = Database.get_user_by_id(user_id)
            if user:
                user["mock_tests_count"] = int(user.get("mock_tests_count", 0)) + 1
                Database.save_user(user)

            udata = cls._read_users()
            if user_id in udata.get("users", {}):
                udata["users"][user_id]["mock_tests_count"] = udata["users"][user_id].get("mock_tests_count", 0) + 1
                cls._write_users(udata)

        return test_record

    @classmethod
    def list_all_mock_tests(cls) -> List[Dict[str, Any]]:
        """List all mock tests from database."""
        tests = Database.list_all_mock_tests()
        if tests:
            return tests
        cls._ensure_files()
        try:
            with open(MOCK_TESTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("tests", [])
        except Exception:
            return []

    # ── Service Inquiries Storage ──

    @classmethod
    def record_service_inquiry(
        cls,
        service_category: str,
        student_name: str,
        phone: str,
        email: Optional[str],
        details: str,
        subject_or_topic: Optional[str] = None,
        deadline: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save a new service inquiry into SQLite database and JSON."""
        inquiry = {
            "id": f"inq_{uuid.uuid4().hex[:10]}",
            "service_category": service_category,
            "student_name": student_name,
            "phone": phone,
            "email": email or "",
            "subject_or_topic": subject_or_topic or "",
            "details": details,
            "deadline": deadline or "Flexible",
            "status": "New",
            "timestamp": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 1. Primary write to SQLite Relational Database
        Database.save_service_inquiry(inquiry)

        # 2. Dual-sync write to service_inquiries.json
        cls._ensure_files()
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"inquiries": []}
        data.setdefault("inquiries", []).insert(0, inquiry)
        with open(SERVICES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return inquiry

    @classmethod
    def list_service_inquiries(cls) -> List[Dict[str, Any]]:
        """List all service inquiries from database."""
        inquiries = Database.list_service_inquiries()
        if inquiries:
            return inquiries
        cls._ensure_files()
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("inquiries", [])
        except Exception:
            return []

    @classmethod
    def update_inquiry_status(cls, inquiry_id: str, status: str) -> bool:
        """Update inquiry status in database and file."""
        db_updated = Database.update_inquiry_status(inquiry_id, status)
        cls._ensure_files()
        file_updated = False
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data.get("inquiries", []):
                if item.get("id") == inquiry_id:
                    item["status"] = status
                    file_updated = True
                    break
            if file_updated:
                with open(SERVICES_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass
        return db_updated or file_updated
