import os
import json
import time
import uuid
from typing import Dict, List, Optional, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MOCK_TESTS_FILE = os.path.join(DATA_DIR, "mock_tests.json")
SERVICES_FILE = os.path.join(DATA_DIR, "service_inquiries.json")

class UserService:
    """Manages student profiles, Google Sign-in sessions, mock test submissions, and service requests."""

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
        data = cls._read_users()
        users = data.get("users", {})

        # Find existing user by google_id or email
        user_id = None
        for uid, u in users.items():
            if u.get("google_id") == google_id or u.get("email", "").lower() == email.lower():
                user_id = uid
                break

        now = time.time()
        session_token = f"acad_usr_{uuid.uuid4().hex}"

        if not user_id:
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
            user = users[user_id]
            user["name"] = name or user.get("name")
            user["picture"] = picture or user.get("picture")
            if lpu_reg_no:
                user["lpu_reg_no"] = lpu_reg_no
            if phone:
                user["phone"] = phone
            user["last_login"] = now
            user["session_token"] = session_token

        users[user_id] = user
        data["users"] = users
        cls._write_users(data)

        return {
            "success": True,
            "user": user,
            "session_token": session_token
        }

    @classmethod
    def get_user_by_token(cls, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """Look up active user by session token."""
        if not token:
            return None
        data = cls._read_users()
        users = data.get("users", {})
        for _, u in users.items():
            if u.get("session_token") == token:
                # Check if plan expired
                if u.get("plan_expiry", 0) > 0 and time.time() > u["plan_expiry"]:
                    u["is_pro"] = False
                    u["active_plan"] = "free"
                    u["plan_name"] = "Free Starter"
                return u
        return None

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        data = cls._read_users()
        return data.get("users", {}).get(user_id)

    @classmethod
    def update_profile(cls, user_id: str, lpu_reg_no: Optional[str] = None, phone: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
        data = cls._read_users()
        users = data.get("users", {})
        if user_id not in users:
            return {"success": False, "message": "User not found"}

        user = users[user_id]
        if lpu_reg_no:
            user["lpu_reg_no"] = lpu_reg_no
        if phone:
            user["phone"] = phone
        if name:
            user["name"] = name

        users[user_id] = user
        data["users"] = users
        cls._write_users(data)
        return {"success": True, "user": user}

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
        """Upgrade user to paid plan or subject mock test pass."""
        data = cls._read_users()
        users = data.get("users", {})
        if user_id not in users:
            return {"success": False, "message": "User not found"}

        user = users[user_id]
        user["active_plan"] = plan_id
        user["plan_name"] = plan_name
        user["plan_expiry"] = time.time() + (duration_days * 86400)
        user["is_pro"] = True
        user["total_spent_inr"] = user.get("total_spent_inr", 0) + amount_paid

        if subject_code:
            purchased = user.get("purchased_subjects", [])
            if subject_code not in purchased:
                purchased.append(subject_code)
            user["purchased_subjects"] = purchased

        users[user_id] = user
        data["users"] = users
        cls._write_users(data)
        return {"success": True, "user": user}

    @classmethod
    def list_all_users(cls) -> List[Dict[str, Any]]:
        data = cls._read_users()
        return list(data.get("users", {}).values())

    @classmethod
    def delete_user(cls, user_id: str) -> bool:
        data = cls._read_users()
        users = data.get("users", {})
        if user_id in users:
            del users[user_id]
            data["users"] = users
            cls._write_users(data)
            return True
        return False

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
        cls._ensure_files()
        try:
            with open(MOCK_TESTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"tests": []}

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

        data.setdefault("tests", []).insert(0, test_record)
        with open(MOCK_TESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Increment user count if registered
        if user_id and user_id != "guest":
            udata = cls._read_users()
            if user_id in udata.get("users", {}):
                udata["users"][user_id]["mock_tests_count"] = udata["users"][user_id].get("mock_tests_count", 0) + 1
                cls._write_users(udata)

        return test_record

    @classmethod
    def list_all_mock_tests(cls) -> List[Dict[str, Any]]:
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
        cls._ensure_files()
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"inquiries": []}

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

        data.setdefault("inquiries", []).insert(0, inquiry)
        with open(SERVICES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return inquiry

    @classmethod
    def list_service_inquiries(cls) -> List[Dict[str, Any]]:
        cls._ensure_files()
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("inquiries", [])
        except Exception:
            return []

    @classmethod
    def update_inquiry_status(cls, inquiry_id: str, status: str) -> bool:
        cls._ensure_files()
        try:
            with open(SERVICES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            found = False
            for item in data.get("inquiries", []):
                if item.get("id") == inquiry_id:
                    item["status"] = status
                    found = True
                    break
            if found:
                with open(SERVICES_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return True
        except Exception:
            pass
        return False
