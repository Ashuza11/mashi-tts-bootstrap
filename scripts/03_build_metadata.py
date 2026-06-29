"""
Build metadata.csv for either track after manual OR auto segmentation.
Run once per track to generate the CSV the TTS trainer expects.

Usage:
  python scripts/03_build_metadata.py --track manual
  python scripts/03_build_metadata.py --track auto
"""

import os
import argparse
import pandas as pd
import soundfile as sf


def build(track):
    seg_dir  = f"data/{track}_segments"
    clip_dir = os.path.join(seg_dir, "audio")
    txt_dir  = os.path.join(seg_dir, "transcripts")

    rows = []
    missing_txt = []

    for fname in sorted(os.listdir(clip_dir)):
        if not fname.endswith(".wav"):
            continue
        clip_path = os.path.join(clip_dir, fname)
        txt_path  = os.path.join(txt_dir,  fname.replace(".wav", ".txt"))

        if not os.path.exists(txt_path):
            missing_txt.append(fname)
            continue

        with open(txt_path, encoding="utf-8") as f:
            text = f.read().strip()

        info = sf.info(clip_path)
        dur  = info.frames / info.samplerate

        rows.append({"file": fname, "text": text, "duration_s": round(dur, 2)})

    df = pd.DataFrame(rows)
    out = os.path.join(seg_dir, "metadata.csv")
    df.to_csv(out, index=False)

    total_min = df["duration_s"].sum() / 60
    print(f"Track [{track}]  clips: {len(df)}  duration: {total_min:.1f} min")
    if missing_txt:
        print(f"  WARNING — {len(missing_txt)} clips have no matching .txt:")
        for f in missing_txt[:5]:
            print(f"    {f}")
    print(f"  Saved: {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--track", choices=["manual", "auto"], required=True)
    args = p.parse_args()
    build(args.track)
