"""
Normalize casing in all transcript .txt files.

Rule: lowercase everything, then capitalize the first letter of each sentence.
This ensures the TTS model sees consistent text regardless of how it was typed.

Usage:
  python scripts/06_normalize_text.py                                   # data/mashi_dataset/transcripts
  python scripts/06_normalize_text.py --dir path/to/any/transcripts/folder
"""

import os
import re
import argparse


def normalize(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    # Lowercase everything first
    text = text.lower()
    # Capitalize first character
    text = text[0].upper() + text[1:]
    # Capitalize after sentence-ending punctuation
    text = re.sub(r'([.!?]\s+)([a-zêâîûàèù])', lambda m: m.group(1) + m.group(2).upper(), text)
    return text


def process_folder(folder: str):
    changed = 0
    skipped = 0
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding="utf-8") as f:
            original = f.read()
        # Skip placeholder/comment files
        if original.strip().startswith("#") or not original.strip():
            skipped += 1
            continue
        normalized = normalize(original)
        if normalized != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(normalized)
            changed += 1
    print(f"  {folder}")
    print(f"    changed: {changed}  |  skipped (empty/placeholder): {skipped}")


def main(directory):
    if not os.path.exists(directory):
        print(f"Folder not found: {directory}")
        return
    process_folder(directory)
    print("Done.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="data/mashi_dataset/transcripts")
    args = p.parse_args()
    main(args.dir)
