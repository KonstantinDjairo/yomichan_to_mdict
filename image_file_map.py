#!/usr/bin/env python3

import json
import os
import shutil
import sys

MANIFEST = "image_file_map.json"
FIXED_DIR = os.path.join(os.path.dirname(__file__), "..", "fixed")

def main():
    cwd = os.path.dirname(os.path.realpath(__file__))
    manifest_path = os.path.join(cwd, MANIFEST)

    # Load the JSON manifest (original → hashed)
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            orig_to_hashed = json.load(f)
    except Exception as e:
        print(f"❌ Error loading '{MANIFEST}': {e}")
        sys.exit(1)

    # Invert to hashed → original
    hashed_to_orig = {v: k for k, v in orig_to_hashed.items()}

    # Ensure fixed output directory exists
    os.makedirs(FIXED_DIR, exist_ok=True)
    print(f"➡️  Output directory: {FIXED_DIR}")

    renamed = 0
    missing = []

    # Process each hashed filename
    for hashed, original in hashed_to_orig.items():
        src = os.path.join(cwd, hashed)
        dst = os.path.join(FIXED_DIR, original)

        if os.path.exists(src):
            if os.path.exists(dst):
                print(f"⚠️  Skipping (already exists): {original}")
            else:
                # Move or copy? Change shutil.move→shutil.copy2 if you prefer copy
                shutil.move(src, dst)
                print(f"✅  Restored: {hashed} → fixed/{original}")
                renamed += 1
        else:
            print(f"❓  Not found: {hashed}")
            missing.append(hashed)

    # Summary
    print("\n--- Summary ---")
    print(f"Restored: {renamed} files")
    if missing:
        print(f"Missing: {len(missing)} files ({', '.join(missing)})")

if __name__ == "__main__":
    main()
