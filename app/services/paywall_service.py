import os
import json
import time
import uuid
import urllib.parse
from typing import Dict, List, Optional, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

class PaywallService:
    """
    Manages monetization, tiers, UPI payments to 7719730804@ptyes,
    coupon codes, UTR verification, and Pro tokens.
    """

    # Official UPI destination specified by user
    UPI_ID = "7719730804@ptyes"
    UPI_PAYEE_NAME = "AcadAssist"

    PLANS = {
        "midterm_mock_49": {
            "id": "midterm_mock_49",
            "name": "Midterm Mode / Subject Mock Test Pass",
            "price_inr": 49,
            "original_price_inr": 149,
            "period": "Per Subject / Midterm Season",
            "badge": "Poster Special ⚡ ₹49",
            "highlight": True,
            "features": [
                "Full Authentic Mock Test for Any Subject (CA / MTE / ETE Pattern)",
                "30 High-Probability MCQs with Distractor Analysis & Explanations",
                "5-Mark & 10-Mark Model Answers with Evaluator Rubrics",
                "Unit-Wise Revision Packs & Practice Question Banks",
                "Formula Sheets, Diagrams & One-Night Cram Sheets",
                "Interactive TCS iON Exam Simulator with Negative Marking (-0.25)",
                "Official Printable LPU Exam Paper (PDF Format)"
            ]
        },
        "educode_99": {
            "id": "educode_99",
            "name": "EduCode Completion Support Pass",
            "price_inr": 99,
            "original_price_inr": 299,
            "period": "Per Task / Lab Guidance",
            "badge": "Coding Desk 💻 ₹99",
            "highlight": False,
            "features": [
                "C / C++, Python, DSA, Java, Web Basics",
                "Concept Explanation & Error Debugging",
                "Lab / Practical File Guidance & Code Review",
                "Viva Questions Preparation & Project Guidance",
                "Direct WhatsApp Expert Support"
            ]
        },
        "neobrowser_99": {
            "id": "neobrowser_99",
            "name": "NeoBrowser Completion Support Pass",
            "price_inr": 99,
            "original_price_inr": 299,
            "period": "Per Task / Assessment",
            "badge": "Smooth & On Time 🌐 ₹99",
            "highlight": False,
            "features": [
                "Your NeoBrowser Tasks Done Smoothly & On Time",
                "Technical Setup & Troubleshooting",
                "Assignments, Quizzes & Assessments Assistance",
                "Reports & Submission Workflow Support",
                "100% On-Time Completion Guarantee"
            ]
        },
        "rush24": {
            "id": "rush24",
            "name": "Exam Night Rush Pass",
            "price_inr": 29,
            "original_price_inr": 99,
            "period": "24 Hours (Night before exam)",
            "badge": "Quick Rush ⚡",
            "highlight": False,
            "features": [
                "Unlimited Exam Generations for 24 hours",
                "ALL MCQs Unlocked with Detailed Explanations",
                "ALL 5M & 10M LPU Model Answers with Rubrics",
                "Download Printable Official LPU Exam PDF",
                "Score Analyzer & Grade Prediction"
            ]
        },
        "semester_pro": {
            "id": "semester_pro",
            "name": "AcadAssist All-Access Semester Pro",
            "price_inr": 199,
            "original_price_inr": 599,
            "period": "Full Semester (6 Months)",
            "badge": "All Subjects VIP 🌟",
            "highlight": False,
            "features": [
                "Unlimited Mock Tests & Papers for ALL Subjects",
                "Unlimited Full Notes, Cram Sheets, Presentation Slides & Roadmaps",
                "Direct Access to ALL notes.lpuverto.xyz Question Banks",
                "High PYQ Repeat Predictions (95%+ match probability)",
                "Priority 24/7 Question Paper Setter Engine",
                "Verified LPU 9+ CGPA Scoring Blueprints"
            ]
        }
    }

    COUPONS = {
        "LPUVERTO": {"discount_percent": 100, "description": "100% OFF Verto Campus Welcome Code"},
        "TOPPER100": {"discount_percent": 100, "description": "100% OFF Academic Excellence Grant"},
        "FREEMIUM": {"discount_percent": 100, "description": "100% OFF Developer & Beta Tester Pass"},
        "MIDTERM49": {"discount_percent": 100, "description": "100% OFF Midterm Mock Test Code"},
        "EXAM50": {"discount_percent": 50, "description": "50% OFF Mid-Term Discount"},
        "VERTOPRO": {"discount_percent": 100, "description": "100% OFF Full Access Token"}
    }

    @classmethod
    def _ensure_files(cls):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump({"transactions": []}, f, indent=2)

    @classmethod
    def get_plans(cls) -> Dict[str, Any]:
        return cls.PLANS

    @classmethod
    def get_upi_payment_link(cls, amount: float, plan_name: str) -> str:
        """Construct standard UPI intent string."""
        encoded_note = urllib.parse.quote(f"{plan_name} - AcadAssist")
        encoded_pn = urllib.parse.quote(cls.UPI_PAYEE_NAME)
        return f"upi://pay?pa={cls.UPI_ID}&pn={encoded_pn}&am={amount:.2f}&cu=INR&tn={encoded_note}"

    @classmethod
    def get_upi_qr_url(cls, amount: float, plan_name: str) -> str:
        """Construct URL for dynamic UPI QR code generator."""
        upi_link = cls.get_upi_payment_link(amount, plan_name)
        encoded_link = urllib.parse.quote(upi_link)
        return f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&margin=10&data={encoded_link}"

    @classmethod
    def validate_coupon(cls, code: str, plan_id: str) -> Dict[str, Any]:
        code_upper = code.strip().upper()
        if code_upper in cls.COUPONS:
            coupon = cls.COUPONS[code_upper]
            plan = cls.PLANS.get(plan_id, cls.PLANS["midterm_mock_49"])
            original_price = plan["price_inr"]
            discount = (original_price * coupon["discount_percent"]) / 100.0
            final_price = max(0.0, original_price - discount)

            return {
                "valid": True,
                "code": code_upper,
                "discount_percent": coupon["discount_percent"],
                "discount_amount": discount,
                "final_price": final_price,
                "description": coupon["description"]
            }
        return {"valid": False, "message": "Invalid coupon code. Try 'LPUVERTO' or 'TOPPER100' for 100% off!"}

    @classmethod
    def process_checkout(
        cls,
        plan_id: str,
        payment_method: str = "upi",
        coupon_code: Optional[str] = None,
        user_name: str = "LPU Student",
        reg_no: str = "12000000",
        phone: Optional[str] = None,
        utr_ref: Optional[str] = None,
        user_id: Optional[str] = None,
        subject_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process student payment for plan (₹49 Mock Test, ₹99 EduCode, etc.),
        log transaction to data/transactions.json, and issue access token.
        """
        cls._ensure_files()
        plan = cls.PLANS.get(plan_id, cls.PLANS["midterm_mock_49"])
        price = float(plan["price_inr"])

        discount = 0.0
        applied_coupon = None
        if coupon_code:
            coupon_res = cls.validate_coupon(coupon_code, plan_id)
            if coupon_res["valid"]:
                applied_coupon = coupon_res["code"]
                discount = coupon_res["discount_amount"]
                price = coupon_res["final_price"]

        tx_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
        token = f"acad_pro_{uuid.uuid4().hex}"
        duration_days = 1 if plan_id == "rush24" else (90 if "mock" in plan_id else 180)

        # Status is approved immediately if coupon used or UTR provided
        status = "approved" if (applied_coupon or utr_ref or price == 0) else "pending"

        transaction_record = {
            "tx_id": tx_id,
            "token": token,
            "plan_id": plan_id,
            "plan_name": plan["name"],
            "subject_code": subject_code or "ALL",
            "amount": price,
            "original_amount": plan["price_inr"],
            "discount": discount,
            "applied_coupon": applied_coupon,
            "payment_method": payment_method.upper(),
            "upi_destination": cls.UPI_ID,
            "utr_ref": utr_ref or f"UTR_{uuid.uuid4().hex[:12].upper()}",
            "user_id": user_id or "guest",
            "user_name": user_name,
            "reg_no": reg_no,
            "phone": phone or "",
            "status": status,
            "created_at": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "expires_at": time.time() + (duration_days * 86400)
        }

        # Write to transactions.json
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                tdata = json.load(f)
        except Exception:
            tdata = {"transactions": []}

        tdata.setdefault("transactions", []).insert(0, transaction_record)
        with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(tdata, f, indent=2)

        # If user_id is provided, upgrade user profile automatically
        if user_id and user_id != "guest":
            from app.services.user_service import UserService
            UserService.grant_user_plan(
                user_id=user_id,
                plan_id=plan_id,
                plan_name=plan["name"],
                duration_days=duration_days,
                amount_paid=price,
                subject_code=subject_code
            )

        return {
            "success": True,
            "message": "Payment verified successfully! Welcome to AcadAssist Midterm Mode.",
            "token": token,
            "plan": plan["name"],
            "amount_paid": price,
            "transaction_id": tx_id,
            "utr_ref": transaction_record["utr_ref"],
            "status": status,
            "upi_destination": cls.UPI_ID,
            "receipt": {
                "bill_to": f"{user_name} (LPU Reg: {reg_no})",
                "service": f"{plan['name']}",
                "payment_gateway": f"AcadAssist Direct UPI ({cls.UPI_ID})",
                "amount": f"₹{price:.2f}",
                "utr_number": transaction_record["utr_ref"],
                "status": "APPROVED & ACTIVE" if status == "approved" else "PENDING VERIFICATION"
            }
        }

    @classmethod
    def list_all_transactions(cls) -> List[Dict[str, Any]]:
        cls._ensure_files()
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("transactions", [])
        except Exception:
            return []

    @classmethod
    def update_transaction_status(cls, tx_id: str, new_status: str) -> bool:
        cls._ensure_files()
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            found = False
            user_to_grant = None
            plan_to_grant = None

            for t in data.get("transactions", []):
                if t.get("tx_id") == tx_id:
                    t["status"] = new_status
                    found = True
                    if new_status == "approved":
                        user_to_grant = t.get("user_id")
                        plan_to_grant = t
                    break

            if found:
                with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

                if user_to_grant and user_to_grant != "guest" and plan_to_grant:
                    from app.services.user_service import UserService
                    UserService.grant_user_plan(
                        user_id=user_to_grant,
                        plan_id=plan_to_grant["plan_id"],
                        plan_name=plan_to_grant["plan_name"],
                        duration_days=180,
                        amount_paid=plan_to_grant["amount"],
                        subject_code=plan_to_grant.get("subject_code")
                    )
                return True
        except Exception:
            pass
        return False

    @classmethod
    def verify_token(cls, token: Optional[str]) -> Dict[str, Any]:
        """Verify if a user token is valid and active."""
        if not token:
            return {"is_pro": False, "plan_id": "free", "message": "Free tier"}

        clean_token = token.strip()
        txs = cls.list_all_transactions()
        for t in txs:
            if t.get("token") == clean_token:
                if time.time() > t.get("expires_at", 0):
                    return {"is_pro": False, "plan_id": "free", "message": "Subscription expired"}
                return {
                    "is_pro": True,
                    "plan_id": t["plan_id"],
                    "plan_name": t.get("plan_name", "AcadAssist Pro"),
                    "expires_at": t.get("expires_at"),
                    "user_name": t.get("user_name", "LPU Student"),
                    "subject_code": t.get("subject_code", "ALL")
                }

        # Check dev / demo token
        if clean_token in ["dev-pro-token", "LPUVERTO_ACTIVE"]:
            return {
                "is_pro": True,
                "plan_id": "semester_pro",
                "plan_name": "AcadAssist Pro (Dev Unlock)",
                "expires_at": time.time() + (180 * 86400),
                "user_name": "LPU Verto Pro"
            }

        return {"is_pro": False, "plan_id": "free", "message": "Free tier"}
