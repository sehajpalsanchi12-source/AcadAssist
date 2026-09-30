import asyncio
import httpx
import os

BASE_URL = "http://127.0.0.1:8000"

async def run_tests():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("1. Testing GET /api/programs ...")
        r = await client.get(f"{BASE_URL}/api/programs")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        programs = r.json()
        print(f"   ✓ Programs loaded: {len(programs)} (First: {programs[0]['id']})")

        print("\n2. Testing GET /api/preloaded-subjects (Bundled from lpuverto.xyz & poster) ...")
        r = await client.get(f"{BASE_URL}/api/preloaded-subjects")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        preloaded = r.json()
        print(f"   ✓ Preloaded subjects loaded: {len(preloaded)} courses")
        subject_codes = [s["code"] for s in preloaded]
        for poster_code in ["MTH166", "PHY109", "PHY110", "ECE131", "CSE101", "CSE205"]:
            assert poster_code in subject_codes, f"Missing {poster_code}"
            print(f"     • Poster Course Verified: {poster_code}")

        print("\n3. Testing POST /api/custom-subject (Creating Custom Course) ...")
        custom_payload = {
            "code": "CSE999",
            "name": "Advanced Autonomous AI & Multi-Agent Robotics",
            "semester": "Sem7",
            "program": "B. Tech. CSE",
            "credits": 4,
            "category": "Departmental Elective",
            "description": "Reinforcement learning, neural planners, and multi-agent coordination frameworks.",
            "units": [
                "Unit 1: Foundations of Multi-Agent Systems",
                "Unit 2: Deep Q-Learning & Policy Gradients",
                "Unit 3: Decentralized Consensus & Swarm Robotics",
                "Unit 4: Real-time Perception & Path Planning"
            ]
        }
        r = await client.post(f"{BASE_URL}/api/custom-subject", json=custom_payload)
        assert r.status_code == 200, f"Failed: {r.status_code}"
        print(f"   ✓ Custom course {custom_payload['code']} saved successfully!")

        print("\n4. Testing GET /api/custom-subjects ...")
        r = await client.get(f"{BASE_URL}/api/custom-subjects")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        custom_list = r.json()
        print(f"   ✓ Custom courses retrieved: {len(custom_list)} found")

        print("\n5. Testing Multi-Asset Generator: POST /api/generate-asset (Comprehensive Notes) ...")
        r = await client.post(f"{BASE_URL}/api/generate-asset", data={
            "asset_type": "notes",
            "subject_code": "MTH166",
            "subject_name": "Differential Equations & Vectors",
            "semester": "Sem2",
            "unit": "Unit1"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        notes_res = r.json()
        print(f"   ✓ Generated Notes for {notes_res.get('subject_code')}: {len(notes_res.get('sections', []))} sections")

        print("\n6. Testing Multi-Asset Generator: POST /api/generate-asset (Short Notes & Flashcards) ...")
        r = await client.post(f"{BASE_URL}/api/generate-asset", data={
            "asset_type": "short_notes",
            "subject_code": "PHY109",
            "subject_name": "Quantum Mechanics",
            "semester": "Sem1",
            "unit": "Unit1"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        short_res = r.json()
        print(f"   ✓ Generated Short Notes: {len(short_res.get('cheat_sheet', []))} cheat items, {len(short_res.get('flashcards', []))} flashcards")

        print("\n7. Testing Multi-Asset Generator: POST /api/generate-asset (Presentation Slides) ...")
        r = await client.post(f"{BASE_URL}/api/generate-asset", data={
            "asset_type": "slides",
            "subject_code": "ECE131",
            "subject_name": "Basic Electronics",
            "semester": "Sem1",
            "unit": "Unit1"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        slides_res = r.json()
        print(f"   ✓ Generated Slides: {slides_res.get('total_slides')} slides in deck")

        print("\n8. Testing Multi-Asset Generator: POST /api/generate-asset (9+ CGPA Roadmap) ...")
        r = await client.post(f"{BASE_URL}/api/generate-asset", data={
            "asset_type": "roadmap",
            "subject_code": "CSE316",
            "subject_name": "Operating Systems",
            "semester": "Sem3",
            "unit": "Unit1"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        roadmap_res = r.json()
        days = roadmap_res.get("study_tracks", [{}])[0].get("days", [])
        print(f"   ✓ Generated 9+ CGPA Roadmap: {len(days)} milestone days planned")

        print("\n9. Testing Fullscreen Presentation: POST /api/export-slides ...")
        r = await client.post(f"{BASE_URL}/api/export-slides", json=slides_res)
        assert r.status_code == 200, f"Failed: {r.status_code}"
        assert "Slide 1 of" in r.text
        print("   ✓ Interactive Slide Projector HTML generated successfully")

        print("\n10a. Testing Secure Student Registration: POST /api/auth/register ...")
        reg_payload = {
            "name": "Arjun Singh",
            "email": "arjun.singh.test@lpu.in",
            "password": "SecurePassword@123",
            "lpu_reg_no": "12209988",
            "phone": "9876543210"
        }
        r = await client.post(f"{BASE_URL}/api/auth/register", json=reg_payload)
        # If user exists from previous run, that's fine, otherwise 200
        if r.status_code == 200:
            reg_res = r.json()
            assert reg_res.get("success") is True
            assert "password_hash" not in reg_res.get("user", {})
            assert "salt" not in reg_res.get("user", {})
            print(f"   ✓ New student registered securely with PBKDF2 hashing: {reg_res['user']['name']}")
        else:
            print(f"   ✓ Student registration check (already registered): {r.status_code}")

        # Duplicate registration test
        r_dup = await client.post(f"{BASE_URL}/api/auth/register", json=reg_payload)
        assert r_dup.status_code == 400, "Duplicate registration should return 400"
        print("   ✓ Duplicate registration prevented (HTTP 400)")

        print("\n10b. Testing Secure Login with Invalid Password: POST /api/auth/login ...")
        r_wrong = await client.post(f"{BASE_URL}/api/auth/login", json={
            "identifier": "arjun.singh.test@lpu.in",
            "password": "WrongPassword@999"
        })
        assert r_wrong.status_code == 401, f"Expected 401, got {r_wrong.status_code}"
        print("   ✓ Invalid credentials rejected securely (HTTP 401)")

        print("\n10c. Testing Secure Login with Email and Correct Password: POST /api/auth/login ...")
        r_login = await client.post(f"{BASE_URL}/api/auth/login", json={
            "identifier": "arjun.singh.test@lpu.in",
            "password": "SecurePassword@123"
        })
        assert r_login.status_code == 200, f"Login failed: {r_login.status_code}"
        login_res = r_login.json()
        assert login_res.get("success") is True
        assert "password_hash" not in login_res.get("user", {})
        assert "salt" not in login_res.get("user", {})
        student_token = login_res.get("session_token")
        print(f"   ✓ Secure login successful: {login_res['user']['email']} (Token: {student_token[:15]}...)")

        print("\n10d. Testing Secure Login with LPU Registration Number: POST /api/auth/login ...")
        r_login_reg = await client.post(f"{BASE_URL}/api/auth/login", json={
            "identifier": "12209988",
            "password": "SecurePassword@123"
        })
        assert r_login_reg.status_code == 200
        print("   ✓ Registration Number login supported and verified!")

        print("\n10e. Testing Google Authentication: POST /api/auth/google ...")
        r = await client.post(f"{BASE_URL}/api/auth/google", json={
            "google_id": "goog_test_987654",
            "name": "Test Student Verto",
            "email": "test.verto@lpu.in",
            "picture": "https://api.dicebear.com/7.x/bottts/svg?seed=student",
            "lpu_reg_no": "12299887",
            "phone": "9876543211"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        auth_data = r.json()
        assert auth_data.get("success") is True
        user = auth_data["user"]
        assert "password_hash" not in user
        assert "salt" not in user
        user_session_token = auth_data["session_token"]
        print(f"   ✓ Google user authenticated without password leakage: {user['name']} (ID: {user['id']})")

        print("\n11. Testing Current User Profile: GET /api/auth/me ...")
        r = await client.get(f"{BASE_URL}/api/auth/me?token={user_session_token}")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        me_data = r.json()
        assert me_data.get("authenticated") is True
        assert "password_hash" not in me_data.get("user", {})
        assert "salt" not in me_data.get("user", {})
        print(f"   ✓ Current user verified: {me_data['user']['email']}")

        print("\n12. Testing Paywall Plans: GET /api/paywall/plans (Subject Pass ₹59 & Mock Test ₹29) ...")
        r = await client.get(f"{BASE_URL}/api/paywall/plans")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        plans = r.json()
        assert "subject_pass_49" in plans
        assert plans["subject_pass_49"]["price_inr"] == 59
        print(f"   ✓ Verified ₹59 Single Subject Master Pass exists! ({plans['subject_pass_49']['name']})")
        assert "mock_test_29" in plans
        assert plans["mock_test_29"]["price_inr"] == 29
        print(f"   ✓ Verified ₹29 Mock Test Simulator Pass exists! ({plans['mock_test_29']['name']})")

        print("\n13. Testing UPI Payment Destination: GET /api/paywall/upi-info ...")
        r = await client.get(f"{BASE_URL}/api/paywall/upi-info?amount=29.0&plan_name=Mock+Test+Pass")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        upi_info = r.json()
        assert upi_info["upi_id"] == "mk9817223@okicici"
        assert upi_info["amount"] == 29.0
        print(f"   ✓ Official UPI Destination verified: {upi_info['upi_id']} for ₹{upi_info['amount']}")

        print("\n14. Testing Mock Test Checkout (₹29) to mk9817223@okicici: POST /api/paywall/checkout ...")
        r = await client.post(f"{BASE_URL}/api/paywall/checkout", json={
            "plan_id": "mock_test_29",
            "payment_method": "upi",
            "coupon_code": None,
            "user_name": "Test Student Verto",
            "reg_no": "12299887",
            "phone": "9876543211",
            "utr_ref": "UTR299827361829",
            "user_id": user["id"],
            "subject_code": "MTH166"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        checkout_res = r.json()
        mock_token = checkout_res.get("token")
        assert checkout_res["amount_paid"] == 29.0
        assert checkout_res["upi_destination"] == "mk9817223@okicici"
        print(f"   ✓ Mock Test Payment recorded: UTR={checkout_res['utr_ref']} | Amount=₹{checkout_res['amount_paid']}")

        print("\n14b. Testing Subject Pass Checkout (₹59) to mk9817223@okicici: POST /api/paywall/checkout ...")
        r = await client.post(f"{BASE_URL}/api/paywall/checkout", json={
            "plan_id": "subject_pass_49",
            "payment_method": "upi",
            "coupon_code": None,
            "user_name": "Test Student Verto",
            "reg_no": "12299887",
            "phone": "9876543211",
            "utr_ref": "UTR499827361849",
            "user_id": user["id"],
            "subject_code": "CSE205"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        checkout_sub_res = r.json()
        pro_token = checkout_sub_res.get("token")
        assert checkout_sub_res["amount_paid"] == 59.0
        assert checkout_sub_res["upi_destination"] == "mk9817223@okicici"
        print(f"   ✓ Subject Pass Payment recorded: UTR={checkout_sub_res['utr_ref']} | Amount=₹{checkout_sub_res['amount_paid']} for CSE205")
        print(f"   ✓ Payment recorded: UTR={checkout_res['utr_ref']} | Amount=₹{checkout_res['amount_paid']}")

        print("\n15. Testing Exam Generation: POST /api/generate-exam ...")
        file_path = os.path.join(os.path.dirname(__file__), "test_samples", "sample_notes.txt")
        with open(file_path, "rb") as f:
            files = {"file": ("sample_notes.txt", f, "text/plain")}
            data = {
                "subject_code": "MTH166",
                "subject_name": "Differential Equations & Vectors",
                "program": "B. Tech. CSE",
                "semester": "Sem2",
                "unit": "Unit1",
                "exam_type": "mte",
                "mcq_count": "15",
                "difficulty": "Mixed",
                "negative_marking": "true",
                "token": pro_token
            }
            r = await client.post(f"{BASE_URL}/api/generate-exam", files=files, data=data)
        assert r.status_code == 200, f"Failed: {r.status_code}"
        paper = r.json()
        print(f"   ✓ Authentic LPU exam generated: {paper.get('exam_title')} for {paper.get('subject_code')}")

        print("\n16. Testing Mock Test Scorecard Submission: POST /api/mock-test/submit ...")
        r = await client.post(f"{BASE_URL}/api/mock-test/submit", json={
            "user_id": user["id"],
            "user_name": user["name"],
            "subject_code": "MTH166",
            "subject_name": "Differential Equations & Vectors",
            "exam_type": "Midterm Mock Test",
            "score": 28.5,
            "total_marks": 30.0,
            "percentage": 95.0,
            "grade": "O (Outstanding)",
            "summary": {"correct": 29, "incorrect": 1}
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        test_rec = r.json()
        print(f"   ✓ Mock test result saved: Grade {test_rec['grade']} ({test_rec['percentage']}%)")

        print("\n17. Testing Service Inquiry Submission (Poster Offers): POST /api/services/inquiry ...")
        r = await client.post(f"{BASE_URL}/api/services/inquiry", json={
            "service_category": "EduCode Completion Support",
            "student_name": "Test Student Verto",
            "phone": "9876543211",
            "email": "test.verto@lpu.in",
            "details": "Need debugging help with DSA graph traversal and dynamic programming project.",
            "subject_or_topic": "CSE205 DSA",
            "deadline": "2026-10-15"
        })
        assert r.status_code == 200, f"Failed: {r.status_code}"
        inq_res = r.json()
        print(f"   ✓ Service inquiry recorded: {inq_res['service_category']} (ID: {inq_res['id']})")

        print("\n18. Testing Admin Login (User: acadassit0812) ...")
        r = await client.post(f"{BASE_URL}/api/admin/login", json={
            "username": "acadassit0812",
            "password": ";Sharma@1290"
        })
        assert r.status_code == 200, f"Admin login failed: {r.text}"
        admin_data = r.json()
        assert admin_data.get("success") is True
        admin_token = admin_data["token"]
        print(f"   ✓ Admin authenticated successfully: {admin_data['admin']['username']}")

        print("\n19. Testing Admin Dashboard Controls & Data Sync ...")
        # Stats
        r = await client.get(f"{BASE_URL}/api/admin/stats?token={admin_token}")
        assert r.status_code == 200
        stats = r.json()
        print(f"   ✓ Admin Stats: Users={stats['total_users']} | Revenue=₹{stats['total_revenue_inr']} | Tests={stats['total_mock_tests']}")

        # Transactions
        r = await client.get(f"{BASE_URL}/api/admin/transactions?token={admin_token}")
        assert r.status_code == 200
        txs = r.json()
        print(f"   ✓ Admin Transactions: {len(txs)} payments found (Destination: {stats['upi_destination']})")

        # Inquiries
        r = await client.get(f"{BASE_URL}/api/admin/service-requests?token={admin_token}")
        assert r.status_code == 200
        inqs = r.json()
        print(f"   ✓ Admin Inquiries: {len(inqs)} requests found")

        # Export
        r = await client.get(f"{BASE_URL}/api/admin/export?token={admin_token}")
        assert r.status_code == 200
        export = r.json()
        print(f"   ✓ Admin Export Snapshot: {len(export['users'])} users, {len(export['transactions'])} transactions")

        print("\n20. Testing GET /api/all-subjects (All 266+ Subjects from notes.lpuverto.xyz) ...")
        r = await client.get(f"{BASE_URL}/api/all-subjects")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        all_subs = r.json()
        print(f"   ✓ All subjects loaded: {len(all_subs)} courses (>= 266)")
        assert len(all_subs) >= 266, "Missing scraped courses"

        print("\n21. Testing Subject Search & Filter on 266+ courses ...")
        r = await client.get(f"{BASE_URL}/api/all-subjects?search=algorithms")
        assert r.status_code == 200
        alg_hits = r.json()
        print(f"   ✓ Search 'algorithms': {len(alg_hits)} matches found")
        assert len(alg_hits) >= 1

        print("\n22. Testing GET /api/pyq/subjects (Past Question Papers Catalog) ...")
        r = await client.get(f"{BASE_URL}/api/pyq/subjects")
        assert r.status_code == 200
        pyq_subs = r.json()
        print(f"   ✓ PYQ subjects available: {len(pyq_subs)} course archives")
        assert len(pyq_subs) >= 10

        print("\n23. Testing Full PYQ Question Paper & Solutions: GET /api/pyq/paper/MTH166-2024-ETE ...")
        r = await client.get(f"{BASE_URL}/api/pyq/paper/MTH166-2024-ETE")
        assert r.status_code == 200
        p_data = r.json()
        print(f"   ✓ Full Paper Loaded: {p_data['paper_id']} - {p_data['subject_name']}")
        print(f"     • Part A MCQs/Short: {len(p_data['part_a'])} questions")
        print(f"     • Part B Analytical: {len(p_data['part_b'])} questions")
        print(f"     • Part C Comprehensive: {len(p_data['part_c'])} questions")
        assert len(p_data["part_a"]) > 0 and len(p_data["part_b"]) > 0 and len(p_data["part_c"]) > 0

        print("\n24. Testing PYQ Question Search Across Papers: GET /api/pyq/search?q=theorem ...")
        r = await client.get(f"{BASE_URL}/api/pyq/search?q=theorem")
        assert r.status_code == 200
        q_results = r.json()
        print(f"   ✓ Search for 'theorem': found {len(q_results)} questions with model answers")
        assert len(q_results) >= 1

        print("\n25. Testing GET /api/subject/CSE205/presentation (JSON Slide Structure) ...")
        r = await client.get(f"{BASE_URL}/api/subject/CSE205/presentation")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        pres_data = r.json()
        print(f"   ✓ Presentation Generated: {pres_data.get('subject_code')} - {pres_data.get('subject_name')}")
        print(f"     • Total Slides: {len(pres_data.get('slides', []))} (Expected >= 10)")
        assert len(pres_data.get('slides', [])) >= 10

        print("\n26. Testing Native PowerPoint Download: GET /api/subject/CSE205/download-pptx ...")
        r = await client.get(f"{BASE_URL}/api/subject/CSE205/download-pptx")
        assert r.status_code == 200, f"Failed: {r.status_code}"
        assert "application/vnd.openxmlformats-officedocument.presentationml.presentation" in r.headers.get("content-type", "")
        assert len(r.content) > 30000, f"PPTX file too small: {len(r.content)} bytes"
        print(f"   ✓ PowerPoint (.pptx) downloaded successfully: {len(r.content):,} bytes")

        print("\n27. Testing GET /api/all-ppts (All 266 Subject PPT Status) ...")
        r = await client.get(f"{BASE_URL}/api/all-ppts")
        assert r.status_code == 200
        all_ppts = r.json()
        print(f"   ✓ All PPTs catalog: {all_ppts['total_ppts_ready']} of {all_ppts['total_subjects']} ready")
        assert all_ppts['total_ppts_ready'] >= 266

        print("\n28. Testing Custom PPT Generation: POST /api/generate-custom-pptx ...")
        r = await client.post(f"{BASE_URL}/api/generate-custom-pptx", data={
            "title": "Cloud Computing & Distributed Systems",
            "code": "CSE408",
            "unit": "Unit 2",
            "text": "Virtualization, containerization, Kubernetes orchestration, consensus protocols, Paxos and Raft."
        })
        assert r.status_code == 200
        assert len(r.content) > 20000
        print(f"   ✓ Custom PPT Generated: {len(r.content):,} bytes")

        print("\n29. Testing Real Relational Database Health: GET /api/database/status ...")
        r = await client.get(f"{BASE_URL}/api/database/status")
        assert r.status_code == 200, f"Database status failed: {r.status_code}"
        db_res = r.json()
        assert db_res.get("success") is True, "Database success flag false"
        db_info = db_res.get("database", {})
        print(f"   ✓ Database Engine: {db_info.get('database_type')}")
        print(f"   ✓ Database File: {db_info.get('database_file')}")
        print(f"   ✓ SQLite Version: {db_info.get('sqlite_version')}")
        print(f"   ✓ Database Size: {db_info.get('database_size_kb')} KB")
        print(f"   ✓ Table Counts: {db_info.get('tables')}")
        assert db_info.get("status") == "HEALTHY & CONNECTED"
        assert db_info.get("tables", {}).get("users", 0) >= 1
        assert db_info.get("tables", {}).get("transactions", 0) >= 1

        print("\n30. Testing Database ACID Persistence & Dual-Sync Integrity ...")
        import time
        unique_email = f"student_{int(time.time())}@lpu.in"
        reg_r = await client.post(f"{BASE_URL}/api/auth/register", json={
            "name": "Database Integration Student",
            "email": unique_email,
            "password": "SecurePassword123!",
            "lpu_reg_no": f"120{int(time.time()) % 1000000}",
            "phone": "9876543210"
        })
        assert reg_r.status_code == 200, f"Registration failed: {reg_r.text}"
        reg_data = reg_r.json()
        assert reg_data.get("success") is True
        token = reg_data.get("session_token")

        # Verify immediate indexed lookup from database via /api/auth/me
        me_r = await client.get(f"{BASE_URL}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_r.status_code == 200
        me_data = me_r.json()
        assert me_data.get("authenticated") is True
        assert me_data.get("user", {}).get("email") == unique_email
        print(f"   ✓ New user saved & retrieved from real database instantly: {me_data['user']['email']}")

        # Clean up ephemeral test artifacts so test runs do not artificially inflate real database revenue
        try:
            import json
            import sqlite3
            from app.database import Database
            conn = sqlite3.connect("data/acadassist.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM transactions WHERE utr_ref IN ('UTR299827361829', 'UTR499827361849')")
            cur.execute("DELETE FROM users WHERE email = ?", (unique_email,))
            conn.commit()
            conn.close()
            with open("data/transactions.json", "r", encoding="utf-8") as f:
                tx_data = json.load(f)
            tx_data["transactions"] = [t for t in tx_data.get("transactions", []) if not (t.get("utr_ref", "").startswith("UTR299") or t.get("utr_ref", "").startswith("UTR499"))]
            with open("data/transactions.json", "w", encoding="utf-8") as f:
                json.dump(tx_data, f, indent=2)
            with open("data/users.json", "r", encoding="utf-8") as f:
                u_data = json.load(f)
            u_data["users"] = {k: v for k, v in u_data.get("users", {}).items() if v.get("email") != unique_email}
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump(u_data, f, indent=2)
        except Exception as e:
            print(f"   (Notice: test cleanup: {e})")

        print("\n🎉 ALL 30 EXTENSIVE END-TO-END TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    asyncio.run(run_tests())
