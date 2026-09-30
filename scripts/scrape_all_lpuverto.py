"""
Scrape all subjects, unit outlines, notes URLs, and metadata from notes.lpuverto.xyz
Saves to data/lpu_all_subjects.json
"""
import asyncio
import httpx
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os

BASE_URL = "https://notes.lpuverto.xyz"

# Clean text helper
def clean_text(s: str) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()

async def fetch_semesters(client: httpx.AsyncClient):
    """Fetch Sem1 to Sem8 to extract course names, credits, and categories"""
    semester_catalog = {}
    for sem in range(1, 9):
        url = f"{BASE_URL}/Sem{sem}"
        try:
            resp = await client.get(url, timeout=12)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                # Match subject code at end of link
                m = re.search(r"/([A-Z]{2,5}\d{3}[A-Z0-9]?)$", href)
                if not m:
                    continue
                code = m.group(1)
                text = clean_text(a.get_text(" ", strip=True))
                
                # Check for card container
                card = a.find_parent("div", class_=lambda c: c and ("rounded" in c or "border" in c)) or a
                card_text = clean_text(card.get_text(" | ", strip=True))
                
                # Extract credits if present
                credits = ""
                cred_m = re.search(r"(\d+)\s*Credits?", card_text, re.IGNORECASE)
                if cred_m:
                    credits = f"{cred_m.group(1)} Credits"
                
                # Extract category
                category = "Core"
                for cat in ["Elective", "Minor", "Open Minor", "Specialization", "Improvement/ReAppear"]:
                    if cat.lower() in card_text.lower():
                        category = cat
                        break
                
                # Extract clean name
                name = ""
                name_m = re.search(r"[A-Z]{2,5}\d{3}[A-Z0-9]?\s*[-—]\s*([^|0-9]+?)(?:\d+\s*Units|View|CA|$)", card_text, re.IGNORECASE)
                if name_m:
                    name = clean_text(name_m.group(1)).title()
                
                if code not in semester_catalog or not semester_catalog[code].get("name"):
                    semester_catalog[code] = {
                        "code": code,
                        "name": name,
                        "semester": f"Semester {sem}",
                        "credits": credits,
                        "category": category,
                        "source_card": href
                    }
        except Exception as e:
            print(f"Error fetching Sem{sem}: {e}")
            
    return semester_catalog

async def scrape_subject_details(client: httpx.AsyncClient, code: str, landing_url: str, sem_info: dict, sem_lock: asyncio.Semaphore):
    async with sem_lock:
        try:
            resp = await client.get(landing_url, timeout=15)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Title
            h1 = soup.find("h1")
            h1_text = clean_text(h1.get_text(strip=True)) if h1 else ""
            
            name = sem_info.get("name", "")
            if not name:
                if "—" in h1_text:
                    name = clean_text(h1_text.split("—", 1)[1]).title()
                elif "-" in h1_text:
                    name = clean_text(h1_text.split("-", 1)[1]).title()
                elif soup.title:
                    t = soup.title.string or ""
                    if "—" in t:
                        name = clean_text(t.split("—", 1)[1].split("Notes")[0]).title()
                    elif "-" in t:
                        name = clean_text(t.split("-", 1)[1].split("Notes")[0]).title()
            
            if not name:
                name = code
            
            # Extract program and semester from breadcrumbs or url
            program = "B. Tech. Computer Science & Engineering"
            semester = sem_info.get("semester", "")
            
            # Check breadcrumbs
            crumbs = soup.find("nav", attrs={"aria-label": re.compile(r"breadcrumb", re.I)}) or soup.find("div", class_=lambda c: c and "breadcrumb" in c.lower() if c else False)
            if crumbs:
                crumb_text = clean_text(crumbs.get_text(" > ", strip=True))
                if "Aerospace" in crumb_text:
                    program = "B. Tech. Aerospace Engineering"
                elif "Biomedical" in crumb_text:
                    program = "B. Tech. Biomedical Engineering"
                elif "Biotechnology" in crumb_text:
                    program = "B. Tech. Biotechnology"
                elif "Forensic" in crumb_text:
                    program = "B.Sc. Forensic Sciences"
                elif "Agriculture" in crumb_text:
                    program = "B.Sc. Hons Agriculture"
                elif "BBA" in crumb_text:
                    program = "Bachelor of Business Administration (BBA)"
                elif "BCA" in crumb_text:
                    program = "Bachelor of Computer Applications (BCA)"
                elif "MCA" in crumb_text:
                    program = "Master of Computer Applications (MCA)"
                
                sem_m = re.search(r"Semester\s*(\d+)|Sem\s*(\d+)", crumb_text, re.IGNORECASE)
                if sem_m and not semester:
                    s_num = sem_m.group(1) or sem_m.group(2)
                    semester = f"Semester {s_num}"
            
            if not semester:
                url_sem = re.search(r"/Sem(\d+)/", landing_url)
                if url_sem:
                    semester = f"Semester {url_sem.group(1)}"
                else:
                    semester = "Semester 1"
            
            # Extract units
            units = []
            for u_num in range(1, 7):
                u_title = f"Unit {u_num}"
                # Search for "Unit N" text
                for el in soup.find_all(string=lambda t: t and t.strip() == f"Unit {u_num}"):
                    card = el.find_parent("div", class_=lambda c: c and "border" in c) or el.parent.parent.parent
                    card_text = clean_text(card.get_text(" | ", strip=True))
                    # Pattern: Unit 1 | Revision | — | Unit Title | Notes | MCQ
                    u_m = re.search(rf"Unit\s*{u_num}\s*(?:\|\s*Revision\s*)?(?:\|\s*[—\-]\s*|\s*:\s*)([^|]+)", card_text)
                    if u_m:
                        raw_title = clean_text(u_m.group(1))
                        if len(raw_title) > 3 and not raw_title.startswith("Notes"):
                            u_title = raw_title.title()
                    break
                
                # Build canonical URLs
                base_path = landing_url.replace(BASE_URL, "").rstrip("/")
                notes_path = f"{base_path}/Unit{u_num}/notes"
                mcq_path = f"{base_path}/Unit{u_num}/mcq"
                subj_path = f"{base_path}/Unit{u_num}/subjective"
                
                units.append({
                    "unit": u_num,
                    "title": u_title,
                    "notes_url": f"{BASE_URL}{notes_path}",
                    "mcq_url": f"{BASE_URL}{mcq_path}",
                    "subjective_url": f"{BASE_URL}{subj_path}"
                })
            
            # Meta description
            desc = ""
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                desc = clean_text(meta_desc["content"])
            if not desc:
                desc = f"Comprehensive study material, unit-wise notes, and mock tests for {code} ({name}) at Lovely Professional University."
            
            # Check exams
            page_text = soup.get_text()
            has_ete = "/ete" in page_text or "End Term" in page_text
            has_mock = "/mock" in page_text or "Mock Test" in page_text or "CA Tests" in page_text
            
            return {
                "code": code,
                "name": name,
                "semester": semester,
                "program": program,
                "credits": sem_info.get("credits", "4 Credits"),
                "category": sem_info.get("category", "Core"),
                "description": desc,
                "units": units,
                "landing_url": landing_url,
                "has_ete": has_ete,
                "has_mock": has_mock
            }
        except Exception as e:
            print(f"Error scraping {code} at {landing_url}: {e}")
            return None

async def main():
    print("Step 1: Parsing sitemap.xml...")
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/sitemap.xml")
        root = ET.fromstring(resp.content)
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [elem.text for elem in root.findall(".//ns:loc", ns)]
        
        with open("data/lpu_sitemap_courses.json") as f:
            courses_map = json.load(f)
        
        landing_map = {}
        for code in courses_map:
            matches = [u for u in urls if u.rstrip("/").endswith("/" + code)]
            if matches:
                non_reappear = [m for m in matches if "reappear" not in m]
                best = non_reappear[0] if non_reappear else matches[0]
                landing_map[code] = best
        
        print(f"Matched {len(landing_map)} landing URLs for courses.")
        
        print("Step 2: Harvesting semester course catalogs (Sem 1 to Sem 8)...")
        sem_catalog = await fetch_semesters(client)
        print(f"Loaded {len(sem_catalog)} subjects from semester grids.")
        
        print(f"Step 3: Concurrently scraping {len(landing_map)} subject details (15 workers)...")
        sem_lock = asyncio.Semaphore(15)
        tasks = []
        for code, url in landing_map.items():
            sem_info = sem_catalog.get(code, {})
            tasks.append(scrape_subject_details(client, code, url, sem_info, sem_lock))
        
        results = await asyncio.gather(*tasks)
        
        all_subjects = {}
        for r in results:
            if r:
                all_subjects[r["code"]] = r
        
        print(f"Step 4: Scraped {len(all_subjects)} complete subjects with 6 units and links!")
        
        os.makedirs("data", exist_ok=True)
        out_path = "data/lpu_all_subjects.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_subjects, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(all_subjects)} subjects to {out_path}!")

if __name__ == "__main__":
    asyncio.run(main())
