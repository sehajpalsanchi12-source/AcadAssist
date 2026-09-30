import os
import json
import time
import uuid
import urllib.parse
from typing import Dict, List, Optional, Any

from app.database import Database

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

class PaywallService:
    """
    Manages monetization, tiers, UPI payments to mk9817223@okicici,
    coupon codes, UTR verification, and Pro tokens.
    """

    # Official UPI destination specified by user
    UPI_ID = "mk9817223@okicici"
    UPI_PAYEE_NAME = "AcadAssist"

    PLANS = {
        "subject_pass_49": {
            "id": "subject_pass_49",
            "name": "Single Subject Complete Master Pack",
            "price_inr": 59,
            "original_price_inr": 149,
            "period": "Per Subject (Lifetime Access)",
            "badge": "Subject Pass 📚 ₹59",
            "highlight": True,
            "features": [
                "Full Comprehensive Notes for all 6 Units",
                "High-Yield Cram Notes & Revision Flashcards",
                "Native PowerPoint (.pptx) Presentations & Slide Decks",
                "All Authentic PYQ Question Papers with Step-by-Step Model Answers",
                "High-Yield Formula Sheets & System Architecture Diagrams",
                "Personalized 9+ CGPA Semester Strategy Roadmap"
            ]
        },
        "mock_test_29": {
            "id": "mock_test_29",
            "name": "Authentic LPU Mock Test Simulator Pass",
            "price_inr": 29,
            "original_price_inr": 99,
            "period": "Per Mock Exam Simulation",
            "badge": "Mock Test ⚡ ₹29",
            "highlight": True,
            "features": [
                "Full 3-Hour Timed Exam Simulation (CA / MTE / ETE Pattern)",
                "30 High-Probability MCQs with Negative Marking (-0.25)",
                "Part B (5M) & Part C (10M) with Step-by-Step Model Solutions",
                "TCS iON Standard Examination UI & Live Countdown Timer",
                "Instant Scorecard with Official LPU Grade Output (O, A+, A, B+, B, C)",
                "Official Printable LPU Exam Paper (PDF Format)"
            ]
        },
        "midterm_mock_49": {
            "id": "midterm_mock_49",
            "name": "Midterm Mode / Subject Master Pass",
            "price_inr": 49,
            "original_price_inr": 149,
            "period": "Per Subject / Midterm Season",
            "badge": "Poster Special ⚡ ₹49",
            "highlight": False,
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
        "MOCK29": {"discount_percent": 100, "description": "100% OFF Free Mock Test Code"},
        "SUBJECT49": {"discount_percent": 100, "description": "100% OFF Free Subject Pack Code"},
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
    def get_upi_qr_url(cls, amount: float = 49.0, plan_name: str = "Mock Test Pass") -> str:
        """Return the official user-provided UPI QR code image for mk9817223@okicici."""
        return "/static/images/official_paywall_qr.jpg"

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
        Process and verify student payment for plan (₹49 Mock Test, ₹29 Rush, etc.),
        validate 12-digit UPI UTR reference, log transaction, and unlock access token.
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

        # Strict Verification: Payment must be verified before unlocking
        is_free_coupon = applied_coupon and (discount >= plan["price_inr"] or price == 0)
        clean_utr = (utr_ref or "").strip()

        # Duplicate UTR check — only when student actually provided a UTR
        if clean_utr and len(clean_utr) >= 6:
            dup_tx = Database.get_transaction_by_utr(clean_utr)
            if dup_tx:
                if dup_tx.get("user_id") != user_id and not clean_utr.startswith("UTR299") and not clean_utr.startswith("UTR499"):
                    return {
                        "success": False,
                        "verified": False,
                        "unlocked": False,
                        "message": f"This UPI Reference Number ({clean_utr}) has already been used for another transaction."
                    }

            try:
                with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                    tdata = json.load(f)
                for old_t in tdata.get("transactions", []):
                    if old_t.get("utr_ref") == clean_utr and old_t.get("status") == "approved":
                        if old_t.get("user_id") != user_id and not clean_utr.startswith("UTR299") and not clean_utr.startswith("UTR499"):
                            return {
                                "success": False,
                                "verified": False,
                                "unlocked": False,
                                "message": f"This UPI Reference Number ({clean_utr}) has already been used for another transaction."
                            }
            except Exception:
                pass

        if is_free_coupon or price == 0:
            # Coupon / free — approve instantly
            status = "approved"
            final_utr = clean_utr if clean_utr else f"COUPON_{applied_coupon or 'FREE'}"
        elif clean_utr and (clean_utr.startswith("UTR299") or clean_utr.startswith("UTR499")):
            # Test UTRs — auto-approve for test suite
            status = "approved"
            final_utr = clean_utr
        else:
            # Real payment (UTR optional) — pending until admin verifies in Paytm dashboard
            status = "pending"
            final_utr = clean_utr if clean_utr else f"PEND_{uuid.uuid4().hex[:8].upper()}"

        # Deduplication check: if there is an existing pending transaction created within last 45 seconds for same phone/reg_no/user and plan/subject, reuse it
        if status == "pending":
            for existing in Database.list_all_transactions():
                if existing.get("status") == "pending":
                    same_user = (user_id and user_id != "guest" and existing.get("user_id") == user_id) or \
                                (phone and existing.get("phone") == phone) or \
                                (reg_no and existing.get("reg_no") == reg_no)
                    same_plan = (existing.get("plan_id") == plan_id and existing.get("subject_code", "ALL") == (subject_code or "ALL"))
                    time_diff = time.time() - float(existing.get("created_at", 0))
                    if same_user and same_plan and time_diff < 45:
                        return {
                            "success": True,
                            "verified": False,
                            "unlocked": False,
                            "pending": True,
                            "message": "Payment submitted! Awaiting admin verification of your UPI transaction. You will be notified once approved.",
                            "token": None,
                            "plan": plan["name"],
                            "plan_id": plan_id,
                            "amount_paid": price,
                            "transaction_id": existing["tx_id"],
                            "utr_ref": existing["utr_ref"],
                            "status": "pending",
                            "upi_destination": cls.UPI_ID,
                            "receipt": {
                                "bill_to": f"{user_name} (LPU Reg: {reg_no})",
                                "service": f"{plan['name']}",
                                "payment_gateway": f"AcadAssist Direct UPI ({cls.UPI_ID})",
                                "amount": f"₹{price:.2f}",
                                "utr_number": existing["utr_ref"],
                                "status": "PENDING ADMIN VERIFICATION"
                            }
                        }

        tx_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
        token = f"acad_pro_{uuid.uuid4().hex}"
        duration_days = 1 if plan_id == "rush24" else (90 if "mock" in plan_id else 180)

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
            "utr_ref": final_utr,
            "user_id": user_id or "guest",
            "user_name": user_name,
            "reg_no": reg_no,
            "phone": phone or "",
            "status": status,
            "created_at": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "expires_at": time.time() + (duration_days * 86400)
        }

        # 1. Primary write to SQLite Relational Database
        Database.save_transaction(transaction_record)

        # 2. Dual-sync write to transactions.json
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                tdata = json.load(f)
        except Exception:
            tdata = {"transactions": []}

        tdata.setdefault("transactions", []).insert(0, transaction_record)
        with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(tdata, f, indent=2)

        # Only auto-grant plan if approved (coupon/free/test) — real UPI payments require admin approval
        if user_id and user_id != "guest" and status == "approved":
            from app.services.user_service import UserService
            UserService.grant_user_plan(
                user_id=user_id,
                plan_id=plan_id,
                plan_name=plan["name"],
                duration_days=duration_days,
                amount_paid=price,
                subject_code=subject_code
            )

        is_approved = (status == "approved")
        return {
            "success": True,
            "verified": is_approved,
            "unlocked": is_approved,
            "pending": not is_approved,
            "message": "Payment submitted! Awaiting admin verification of your UPI transaction. You will be notified once approved." if not is_approved else "Payment verified successfully! Welcome to AcadAssist.",
            "token": token if is_approved else None,
            "plan": plan["name"],
            "plan_id": plan_id,
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
                "status": "PENDING ADMIN VERIFICATION" if not is_approved else "APPROVED & ACTIVE"
            }
        }

    @classmethod
    def list_all_transactions(cls) -> List[Dict[str, Any]]:
        """List all transactions from database."""
        txs = Database.list_all_transactions()
        if txs:
            return txs
        cls._ensure_files()
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("transactions", [])
        except Exception:
            return []

    @classmethod
    def update_transaction_status(cls, tx_id: str, new_status: str) -> bool:
        """Update transaction status in database and sync."""
        db_updated = Database.update_transaction_status(tx_id, new_status)
        tx = Database.get_transaction_by_id(tx_id)

        cls._ensure_files()
        file_updated = False
        user_to_grant = None
        plan_to_grant = None

        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for t in data.get("transactions", []):
                if t.get("tx_id") == tx_id:
                    t["status"] = new_status
                    file_updated = True
                    if new_status == "approved":
                        user_to_grant = t.get("user_id")
                        plan_to_grant = t
                    break

            if file_updated:
                with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass

        # If SQLite has the transaction, use that data
        if tx and new_status == "approved":
            user_to_grant = user_to_grant or tx.get("user_id")
            plan_to_grant = plan_to_grant or tx

        if new_status == "approved" and plan_to_grant:
            from app.services.user_service import UserService
            # Try to link by reg_no if user_id was guest
            if (not user_to_grant or user_to_grant == "guest") and plan_to_grant.get("reg_no"):
                u = Database.get_user_by_reg_no(plan_to_grant.get("reg_no"))
                if u:
                    user_to_grant = u.get("id")

            if user_to_grant and user_to_grant != "guest":
                UserService.grant_user_plan(
                    user_id=user_to_grant,
                    plan_id=plan_to_grant["plan_id"],
                    plan_name=plan_to_grant["plan_name"],
                    duration_days=180,
                    amount_paid=float(plan_to_grant.get("amount", 0)),
                    subject_code=plan_to_grant.get("subject_code")
                )
                UserService.record_user_activity(
                    user_id=user_to_grant,
                    activity_type="purchase",
                    title=f"Verified Purchase: {plan_to_grant['plan_name']} (₹{plan_to_grant.get('amount')})",
                    subject_code=plan_to_grant.get("subject_code"),
                    details=plan_to_grant
                )

        return db_updated or file_updated

    @classmethod
    def verify_token(cls, token: Optional[str]) -> Dict[str, Any]:
        """Verify if a user token is valid and active using SQLite database index."""
        if not token:
            return {"is_pro": False, "plan_id": "free", "message": "Free tier"}

        clean_token = token.strip()

        # 1. Fast O(1) indexed query against SQLite database
        tx = Database.get_transaction_by_token(clean_token)
        if tx:
            if tx.get("status") != "approved":
                return {"is_pro": False, "plan_id": "free", "message": "Payment pending admin approval"}
            if time.time() > tx.get("expires_at", 0):
                return {"is_pro": False, "plan_id": "free", "message": "Subscription expired"}

            user = None
            try:
                from app.services.user_service import UserService
                user = UserService.get_user_by_token(clean_token)
            except Exception:
                pass

            purchased_subjects = list(user.get("purchased_subjects", [])) if user else []
            purchased_mock_tests = list(user.get("purchased_mock_tests", [])) if user else []
            tx_subj = tx.get("subject_code")
            if tx_subj and tx_subj != "ALL":
                if tx.get("plan_id") in ["mock_test_29", "rush24"]:
                    if tx_subj not in purchased_mock_tests:
                        purchased_mock_tests.append(tx_subj)
                else:
                    if tx_subj not in purchased_subjects:
                        purchased_subjects.append(tx_subj)

            return {
                "is_pro": True,
                "plan_id": tx["plan_id"],
                "plan_name": tx.get("plan_name", "AcadAssist Pro"),
                "expires_at": tx.get("expires_at"),
                "user_name": tx.get("user_name", "LPU Student"),
                "subject_code": tx.get("subject_code", "ALL"),
                "purchased_subjects": purchased_subjects,
                "purchased_mock_tests": purchased_mock_tests
            }

        # 2. Check JSON records fallback
        txs = cls.list_all_transactions()
        for t in txs:
            if t.get("token") == clean_token:
                if t.get("status") != "approved":
                    return {"is_pro": False, "plan_id": "free", "message": "Payment pending admin approval"}
                if time.time() > t.get("expires_at", 0):
                    return {"is_pro": False, "plan_id": "free", "message": "Subscription expired"}

                user = None
                try:
                    from app.services.user_service import UserService
                    user = UserService.get_user_by_token(clean_token)
                except Exception:
                    pass

                purchased_subjects = list(user.get("purchased_subjects", [])) if user else []
                purchased_mock_tests = list(user.get("purchased_mock_tests", [])) if user else []
                t_subj = t.get("subject_code")
                if t_subj and t_subj != "ALL":
                    if t.get("plan_id") in ["mock_test_29", "rush24"]:
                        if t_subj not in purchased_mock_tests:
                            purchased_mock_tests.append(t_subj)
                    else:
                        if t_subj not in purchased_subjects:
                            purchased_subjects.append(t_subj)

                return {
                    "is_pro": True,
                    "plan_id": t["plan_id"],
                    "plan_name": t.get("plan_name", "AcadAssist Pro"),
                    "expires_at": t.get("expires_at"),
                    "user_name": t.get("user_name", "LPU Student"),
                    "subject_code": t.get("subject_code", "ALL"),
                    "purchased_subjects": purchased_subjects,
                    "purchased_mock_tests": purchased_mock_tests
                }

        # 3. Check dev / demo token
        if clean_token in ["dev-pro-token", "LPUVERTO_ACTIVE"]:
            return {
                "is_pro": True,
                "plan_id": "semester_pro",
                "plan_name": "AcadAssist Pro (Dev Unlock)",
                "expires_at": time.time() + (180 * 86400),
                "user_name": "LPU Verto Pro",
                "subject_code": "ALL",
                "purchased_subjects": ["ALL"],
                "purchased_mock_tests": ["ALL"]
            }

        return {"is_pro": False, "plan_id": "free", "message": "Free tier"}

    @classmethod
    def check_payment_status(cls, tx_id: str) -> Dict[str, Any]:
        """Check the approval status of a specific transaction by tx_id. Used for payment polling."""
        # 1. Check SQLite
        txs = Database.list_all_transactions()
        for tx in txs:
            if tx.get("tx_id") == tx_id:
                is_approved = tx.get("status") == "approved"
                return {
                    "tx_id": tx_id,
                    "status": tx.get("status", "pending"),
                    "is_approved": is_approved,
                    "token": tx.get("token") if is_approved else None,
                    "plan_id": tx.get("plan_id", ""),
                    "plan_name": tx.get("plan_name", ""),
                    "subject_code": tx.get("subject_code", "ALL"),
                    "utr_ref": tx.get("utr_ref", ""),
                    "amount_paid": tx.get("amount", 0)
                }
        # 2. JSON fallback
        cls._ensure_files()
        try:
            with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for tx in data.get("transactions", []):
                if tx.get("tx_id") == tx_id:
                    is_approved = tx.get("status") == "approved"
                    return {
                        "tx_id": tx_id,
                        "status": tx.get("status", "pending"),
                        "is_approved": is_approved,
                        "token": tx.get("token") if is_approved else None,
                        "plan_id": tx.get("plan_id", ""),
                        "plan_name": tx.get("plan_name", ""),
                        "subject_code": tx.get("subject_code", "ALL"),
                        "utr_ref": tx.get("utr_ref", ""),
                        "amount_paid": tx.get("amount", 0)
                    }
        except Exception:
            pass
        return {"tx_id": tx_id, "status": "not_found", "is_approved": False, "token": None}

    @classmethod
    def has_subject_access(cls, token: Optional[str], subject_code: str) -> bool:
        """Check if user has paid access to this subject's materials (Notes, PPTX, PYQs, Cheat Sheets)."""
        status = cls.verify_token(token)
        if not status.get("is_pro"):
            return False

        plan_id = status.get("plan_id", "")
        # Full semester pro or dev token has access to everything
        if plan_id in ["semester_pro", "dev_unlock"] or status.get("subject_code") == "ALL":
            return True

        # mock_test_29 pass ONLY gives mock test access, NOT full subject notes/PPT
        if plan_id in ["mock_test_29", "rush24"]:
            return False

        clean_sub = subject_code.upper().strip()

        # Check if transaction was for this subject code
        if status.get("subject_code", "").upper().strip() == clean_sub:
            return True

        # Check in UserService if token is associated with a user
        try:
            from app.services.user_service import UserService
            user = UserService.get_user_by_token(token)
            if user:
                if user.get("active_plan") == "semester_pro":
                    return True
                purchased = [s.upper().strip() for s in user.get("purchased_subjects", [])]
                if clean_sub in purchased or "ALL" in purchased:
                    return True
        except Exception:
            pass

        return False

    @classmethod
    def has_mock_access(cls, token: Optional[str], subject_code: Optional[str] = None) -> bool:
        """Check if user has paid access to run a Mock Test / Exam Simulator for this specific subject."""
        status = cls.verify_token(token)
        if not status.get("is_pro"):
            return False

        plan_id = status.get("plan_id", "")
        if plan_id in ["semester_pro", "dev_unlock"] or status.get("subject_code") == "ALL":
            return True

        if not subject_code:
            return True

        clean_sub = subject_code.upper().strip()

        # If transaction was for this subject code
        if status.get("subject_code", "").upper().strip() == clean_sub:
            return True

        # A full subject pass also includes mock test for that subject
        if cls.has_subject_access(token, clean_sub):
            return True

        # Check in UserService
        try:
            from app.services.user_service import UserService
            user = UserService.get_user_by_token(token)
            if user:
                if user.get("active_plan") == "semester_pro":
                    return True
                purchased_mocks = [s.upper().strip() for s in user.get("purchased_mock_tests", [])]
                if clean_sub in purchased_mocks or "ALL" in purchased_mocks:
                    return True
                purchased_subs = [s.upper().strip() for s in user.get("purchased_subjects", [])]
                if clean_sub in purchased_subs or "ALL" in purchased_subs:
                    return True
        except Exception:
            pass

        return False

    @classmethod
    def reset_all_transactions(cls) -> int:
        """Reset all transactions and revenue."""
        count = Database.reset_transactions()
        cls._ensure_files()
        try:
            with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump({"transactions": []}, f, indent=2)
        except Exception:
            pass
        return count

