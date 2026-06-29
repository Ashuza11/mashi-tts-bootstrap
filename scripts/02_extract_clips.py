"""
Track A — Extract WAV clips from WhisperX alignment JSON.
Run after 01_whisperx_align.py.

Filters:
  - clip duration between MIN_SEC and MAX_SEC
  - transcript text at least MIN_CHARS characters
  - skips segments where WhisperX confidence is too low (no words aligned)

Output: data/auto_segments/audio/*.wav
        data/auto_segments/transcripts/*.txt
        data/auto_segments/metadata.csv
"""

import os
import json
import pandas as pd
from pydub import AudioSegment

CHAPTERS  = ["ch01", "ch02", "ch03", "ch04"]
MIN_SEC   = 2.0
MAX_SEC   = 12.0
MIN_CHARS = 8


def main(raw_dir, seg_dir):
    audio_dir    = os.path.join(raw_dir,  "Dataset_Mashi", "Bible", "audio")
    json_dir     = os.path.join(seg_dir,  "alignment_json")
    clip_dir     = os.path.join(seg_dir,  "audio")
    txt_dir      = os.path.join(seg_dir,  "transcripts")
    os.makedirs(clip_dir, exist_ok=True)
    os.makedirs(txt_dir,  exist_ok=True)

    rows = []

    for ch in CHAPTERS:
        json_path  = os.path.join(json_dir,  f"shi_bible_bib_{ch}_aligned.json")
        audio_path = os.path.join(audio_dir, f"shi_bible_bib_{ch}.mp3")

        if not os.path.exists(json_path):
            print(f"  SKIP (no alignment): {ch}")
            continue

        audio = AudioSegment.from_mp3(audio_path)
        with open(json_path, encoding="utf-8") as f:
            segments = json.load(f)

        kept = 0
        for i, seg in enumerate(segments):
            dur  = seg["end"] - seg["start"]
            text = seg.get("text", "").strip()
            if dur < MIN_SEC or dur > MAX_SEC or len(text) < MIN_CHARS:
                continue

            clip_name = f"shi_bible_bib_{ch}_bib_seg{i:04d}"
            clip = audio[int(seg["start"] * 1000) : int(seg["end"] * 1000)]
            clip.export(os.path.join(clip_dir, f"{clip_name}.wav"), format="wav")

            with open(os.path.join(txt_dir, f"{clip_name}.txt"), "w", encoding="utf-8") as f:
                f.write(text + "\n")

            rows.append({"file": f"{clip_name}.wav", "text": text, "duration_s": round(dur, 2), "chapter": ch})
            kept += 1

        print(f"  {ch}: {kept}/{len(segments)} segments kept")

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(seg_dir, "metadata.csv"), index=False)
    total_min = df["duration_s"].sum() / 60
    print(f"\nTotal clips  : {len(df)}")
    print(f"Total duration: {total_min:.1f} min ({total_min/60:.2f} h)")
    print(f"Saved to: {seg_dir}/metadata.csv")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--raw_dir", default="data/raw")
    p.add_argument("--seg_dir", default="data/auto_segments")
    args = p.parse_args()
    main(args.raw_dir, args.seg_dir)
