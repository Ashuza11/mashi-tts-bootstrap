"""
Track A — Automatic segmentation using WhisperX.
Run on Google Colab (GPU required).

Input : data/raw/Dataset_Mashi/Bible/audio/shi_bible_bib_ch01.mp3 ... ch04.mp3
Output: data/auto_segments/audio/*.wav  +  alignment JSON files
"""

import os
import json
import argparse
import whisperx

CHAPTERS = ["ch01", "ch02", "ch03", "ch04"]

def main(raw_dir, out_dir, device="cuda"):
    audio_dir = os.path.join(raw_dir, "Dataset_Mashi", "Bible", "audio")
    json_dir  = os.path.join(out_dir, "alignment_json")
    os.makedirs(json_dir, exist_ok=True)

    print("Loading WhisperX model...")
    model = whisperx.load_model("large-v2", device, compute_type="float16")

    for ch in CHAPTERS:
        audio_path = os.path.join(audio_dir, f"shi_bible_bib_{ch}.mp3")
        if not os.path.exists(audio_path):
            print(f"  SKIP (not found): {audio_path}")
            continue

        print(f"\nProcessing {ch}...")
        audio = whisperx.load_audio(audio_path)

        # Transcribe — use Swahili as proxy (closest Bantu WhisperX supports)
        result = model.transcribe(audio, language="sw", batch_size=16)
        print(f"  Transcribed: {len(result['segments'])} raw segments")

        # Force-align to get precise timestamps
        align_model, metadata = whisperx.load_align_model(
            language_code="sw", device=device
        )
        result = whisperx.align(
            result["segments"], align_model, metadata, audio, device
        )

        out_path = os.path.join(json_dir, f"shi_bible_bib_{ch}_aligned.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result["segments"], f, ensure_ascii=False, indent=2)
        print(f"  Saved alignment: {out_path}")

    print("\nDone. Run 02_extract_clips.py next.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--raw_dir", default="data/raw")
    p.add_argument("--out_dir", default="data/auto_segments")
    p.add_argument("--device", default="cuda")
    args = p.parse_args()
    main(args.raw_dir, args.out_dir, args.device)
