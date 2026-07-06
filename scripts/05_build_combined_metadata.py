"""
Combine all three speakers into one metadata.csv for multi-speaker TTS training.

Reads from data/mashi_dataset/ and produces:
  data/mashi_dataset/metadata_combined.csv

CSV columns:
  file        — wav filename (relative to audio/ folder)
  text        — Mashi transcript
  speaker_id  — bib | dav | mrl
  domain      — bible | story | family | numbers | time
  duration_s  — clip length in seconds

Usage:
  python scripts/05_build_combined_metadata.py
"""

import os
import re
import argparse
import pandas as pd
import soundfile as sf


SPEAKER_PATTERN = re.compile(r"shi_(\w+)_(bib|dav|mrl)_")
DOMAIN_MAP = {
    "bible":   "bible",
    "story":   "story",
    "family":  "family",
    "numbers": "numbers",
    "time":    "time",
}


def infer_meta(filename):
    """Extract domain and speaker from standardised filename."""
    m = SPEAKER_PATTERN.search(filename)
    if not m:
        return None, None
    domain  = DOMAIN_MAP.get(m.group(1), "unknown")
    speaker = m.group(2)
    return domain, speaker


def build(seg_dir="data/mashi_dataset"):
    clip_dir = os.path.join(seg_dir, "audio")
    txt_dir  = os.path.join(seg_dir, "transcripts")

    rows = []
    warnings = []

    for fname in sorted(os.listdir(clip_dir)):
        if not fname.endswith(".wav"):
            continue

        clip_path = os.path.join(clip_dir, fname)
        txt_path  = os.path.join(txt_dir,  fname.replace(".wav", ".txt"))

        if not os.path.exists(txt_path):
            warnings.append(f"No transcript: {fname}")
            continue

        with open(txt_path, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        text = " ".join(lines)

        if not text:
            warnings.append(f"Empty transcript: {fname} — skipped")
            continue

        domain, speaker = infer_meta(fname)
        if domain is None:
            warnings.append(f"Cannot parse speaker/domain: {fname}")
            continue

        info = sf.info(clip_path)
        dur  = round(info.frames / info.samplerate, 2)

        rows.append({
            "file":       fname,
            "text":       text,
            "speaker_id": speaker,
            "domain":     domain,
            "duration_s": dur,
        })

    df = pd.DataFrame(rows)
    out = os.path.join(seg_dir, "metadata_combined.csv")
    df.to_csv(out, index=False)

    print(f"\nCombined dataset — {seg_dir}")
    print(f"  Total clips  : {len(df)}")
    print(f"  Total duration: {df.duration_s.sum()/60:.1f} min")
    print()
    for spk in ["bib", "dav", "mrl"]:
        sub = df[df.speaker_id == spk]
        if len(sub) > 0:
            print(f"  Speaker [{spk}]: {len(sub)} clips, {sub.duration_s.sum()/60:.1f} min")
            for dom in sub.domain.unique():
                d = sub[sub.domain == dom]
                print(f"    {dom:10s}: {len(d)} clips, {d.duration_s.sum()/60:.1f} min")
    print()

    if warnings:
        print(f"  WARNINGS ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"    {w}")

    # Per-speaker reference audio (first clip from each speaker, for voice conditioning)
    ref_dir = os.path.join(seg_dir, "speaker_references")
    os.makedirs(ref_dir, exist_ok=True)
    for spk in ["bib", "dav", "mrl"]:
        sub = df[df.speaker_id == spk].sort_values("duration_s")
        # pick the clip closest to 5 seconds as reference
        sub["diff"] = (sub.duration_s - 5.0).abs()
        if len(sub) == 0:
            continue
        ref_file = sub.loc[sub["diff"].idxmin(), "file"]
        import shutil
        shutil.copy2(
            os.path.join(clip_dir, ref_file),
            os.path.join(ref_dir, f"ref_{spk}.wav"),
        )
        print(f"  Reference audio [{spk}]: {ref_file}")

    print(f"\n  Saved: {out}")
    print(f"  Reference wavs: {ref_dir}/")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="data/mashi_dataset")
    args = p.parse_args()
    build(args.dir)
