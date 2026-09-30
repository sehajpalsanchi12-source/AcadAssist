#!/usr/bin/env python3
"""
Batch PPT Generator for AcadAssist
Generates PowerPoint presentation slide decks (.pptx) for all 266+ subjects in catalog.
"""
import os
import sys
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.ppt_service import PPTService

def main():
    print("=" * 60)
    print("  AcadAssist — Batch PowerPoint (.pptx) Deck Generator")
    print("  Lovely Professional University Academic Curriculum")
    print("=" * 60)

    start_time = time.time()
    subjects = PPTService._load_subjects()
    total = len(subjects)
    print(f"Loaded {total} subjects from catalog.")

    os.makedirs(PPTService.PPTS_DIR, exist_ok=True)
    
    success = 0
    skipped = 0
    failed = 0

    for i, (code, sub) in enumerate(subjects.items(), 1):
        target_file = os.path.join(PPTService.PPTS_DIR, f"{code}_presentation.pptx")
        if os.path.exists(target_file) and os.path.getsize(target_file) > 1024:
            skipped += 1
            if i % 25 == 0 or i == total:
                print(f"[{i}/{total}] {code}: Already generated ({os.path.getsize(target_file):,} bytes)")
            continue

        try:
            deck_data = PPTService.generate_presentation_data(code)
            PPTService.create_pptx(deck_data, output_path=target_file)
            success += 1
            if i % 25 == 0 or i == total:
                print(f"[{i}/{total}] {code}: Generated {sub.get('name', '')[:35]} ({os.path.getsize(target_file):,} bytes)")
        except Exception as e:
            failed += 1
            print(f"[{i}/{total}] {code}: ERROR -> {e}")

    elapsed = time.time() - start_time
    print("=" * 60)
    print(f"Batch generation completed in {elapsed:.2f}s!")
    print(f"Newly generated: {success}")
    print(f"Already cached:  {skipped}")
    print(f"Failed:          {failed}")
    print(f"Total ready:     {success + skipped}/{total}")
    print(f"Output directory: {PPTService.PPTS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
