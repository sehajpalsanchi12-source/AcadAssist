import os
import json
import time
import uuid
from typing import Dict, List, Optional, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

class AdminService:
    """Manages administrator authentication, analytics, permissions, and full platform controls."""

    # Explicit credentials requested by user
    ADMIN_USERNAMES = {"acasassist0812", "acadassist0812", "acadassit0812"}
    ADMIN_PASSWORDS = {"sharma@1290", ";sharma@1290"}

    # Active admin sessions
    _admin_sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def login(cls, username: str, password: str) -> Dict[str, Any]:
        """Authenticate admin with username and password."""
        u_clean = username.strip().lower()
        p_clean = password.strip()

        if u_clean in cls.ADMIN_USERNAMES and (p_clean in cls.ADMIN_PASSWORDS or p_clean.lower() in cls.ADMIN_PASSWORDS):
            token = f"admin_sess_{uuid.uuid4().hex}"
            session = {
                "token": token,
                "username": u_clean,
                "role": "SuperAdmin",
                "logged_in_at": time.time(),
                "expires_at": time.time() + (7 * 86400)
            }
            cls._admin_sessions[token] = session
            return {
                "success": True,
                "message": "Admin authenticated successfully. Welcome, AcadAssist Administrator!",
                "token": token,
                "admin": {
                    "username": u_clean,
                    "role": "SuperAdmin",
                    "permissions": ["all", "users_manage", "payments_approve", "catalog_edit", "export_data"]
                }
            }
        return {"success": False, "message": "Invalid admin username or password."}

    @classmethod
    def verify_admin_token(cls, token: Optional[str]) -> bool:
        if not token:
            return False
        clean = token.strip()
        sess = cls._admin_sessions.get(clean)
        if not sess:
            return False
        if time.time() > sess.get("expires_at", 0):
            del cls._admin_sessions[clean]
            return False
        return True

    @classmethod
    def get_dashboard_stats(cls) -> Dict[str, Any]:
        """Aggregate platform statistics for the Admin Dashboard."""
        from app.services.user_service import UserService
        from app.services.paywall_service import PaywallService
        from app.database import Database

        users = UserService.list_all_users()
        mock_tests = UserService.list_all_mock_tests()
        inquiries = UserService.list_service_inquiries()
        transactions = PaywallService.list_all_transactions()
        visitor_stats = Database.get_visitor_analytics()

        total_revenue = sum(t.get("amount", 0.0) for t in transactions if t.get("status") in ["approved", "active"])
        pending_payments = [t for t in transactions if t.get("status") == "pending"]
        approved_payments = [t for t in transactions if t.get("status") == "approved"]
        rejected_payments = [t for t in transactions if t.get("status") == "rejected"]

        return {
            "total_users": len(users),
            "pro_users": len([u for u in users if u.get("is_pro")]),
            "total_revenue_inr": round(total_revenue, 2),
            "upi_destination": PaywallService.UPI_ID,
            "total_mock_tests": len(mock_tests),
            "total_service_inquiries": len(inquiries),
            "pending_payments_count": len(pending_payments),
            "approved_payments_count": len(approved_payments),
            "rejected_payments_count": len(rejected_payments),
            "total_transactions_count": len(transactions),
            "visitor_analytics": visitor_stats,
            "active_now": visitor_stats.get("active_now", 0),
            "active_today": visitor_stats.get("active_today", 0),
            "total_visits": visitor_stats.get("total_visits", 0),
            "unique_visitors": visitor_stats.get("unique_visitors", 0),
            "recent_visits": visitor_stats.get("recent_visits", []),
            "database": Database.get_stats(),
            "recent_activity": {
                "recent_users": users[-5:] if users else [],
                "recent_transactions": transactions[:5],
                "recent_inquiries": inquiries[:5]
            }
        }

    @classmethod
    def export_all_data(cls) -> Dict[str, Any]:
        """Export comprehensive JSON snapshot of the platform."""
        from app.services.user_service import UserService
        from app.services.paywall_service import PaywallService
        from app.services.lpuverto_service import LPUVertoService

        return {
            "exported_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "upi_id": PaywallService.UPI_ID,
            "users": UserService.list_all_users(),
            "transactions": PaywallService.list_all_transactions(),
            "mock_tests": UserService.list_all_mock_tests(),
            "service_inquiries": UserService.list_service_inquiries(),
            "custom_subjects": LPUVertoService.get_custom_subjects()
        }
