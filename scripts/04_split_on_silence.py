"""
Silence-based automatic splitting for structured recordings.

Best suited for David's (dav) vocabulary recordings where he paused
between each item: numbers, family terms, and calendar entries.
NOT for continuous narratives (short stories) — use WhisperX for those.

Usage:
  python scripts/04_split_on_silence.py --input data/raw/Dataset_Mashi/Numbers/audio/shi_numbers_dav_001.aac --domain numbers --speaker dav
  python scripts/04_split_on_silence.py --input data/raw/Dataset_Mashi/Family/audio/shi_family_dav_001.aac  --domain family  --speaker dav
  python scripts/04_split_on_silence.py --input data/raw/Dataset_Mashi/Time/audio/shi_time_dav_001_nsaha_calendar.aac --domain time --speaker dav

  # For each time-of-day clip from mrl:
  python scripts/04_split_on_silence.py --input data/raw/Dataset_Mashi/Time/audio/shi_time_mrl_07_53.mp3 --domain time --speaker mrl

Output: data/manual_segments/audio/shi_{domain}_{speaker}_{file_id}_seg{NNN}.wav
        data/manual_segments/transcripts/shi_{domain}_{speaker}_{file_id}_seg{NNN}.txt  (placeholder)
"""

import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence


def main(input_path, domain, speaker, out_dir, min_silence_ms, silence_thresh, min_seg_ms, max_seg_ms):
    print(f"\nInput : {input_path}")
    ext = os.path.splitext(input_path)[1].lower()

    # Load audio
    if ext == ".aac":
        audio = AudioSegment.from_file(input_path, format="aac")
    elif ext == ".mp3":
        audio = AudioSegment.from_mp3(input_path)
    else:
        audio = AudioSegment.from_file(input_path)

    print(f"Loaded: {len(audio)/1000:.1f}s, {audio.frame_rate}Hz, {audio.channels}ch")

    # Split on silence
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_ms,   # pause must be at least this long
        silence_thresh=silence_thresh,     # dBFS — audio below this is "silence"
        keep_silence=200,                  # keep 200ms padding on each side
    )
    print(f"Found {len(chunks)} segments after silence split")

    # Derive file ID from input filename
    file_id = os.path.splitext(os.path.basename(input_path))[0]

    clip_dir = os.path.join(out_dir, "audio")
    txt_dir  = os.path.join(out_dir, "transcripts")
    os.makedirs(clip_dir, exist_ok=True)
    os.makedirs(txt_dir,  exist_ok=True)

    kept   = 0
    merged = 0
    skipped = 0
    buffer_audio = None
    results = []

    for i, chunk in enumerate(chunks):
        dur_ms = len(chunk)

        # Too short — merge with next chunk (avoids single-word fragments)
        if dur_ms < min_seg_ms:
            buffer_audio = chunk if buffer_audio is None else buffer_audio + chunk
            merged += 1
            continue

        # Apply any buffered audio from previous short chunks
        if buffer_audio is not None:
            chunk = buffer_audio + chunk
            buffer_audio = None

        # Too long even after merge — skip (likely continuous speech, not vocabulary item)
        if len(chunk) > max_seg_ms:
            print(f"  SKIP seg{i:04d}: {len(chunk)/1000:.1f}s (too long — treat as narrative)")
            buffer_audio = None
            skipped += 1
            continue

        # Export as mono 22050Hz WAV (TTS training standard)
        chunk = chunk.set_channels(1).set_frame_rate(22050)
        clip_name = f"shi_{domain}_{speaker}_{file_id}_seg{kept+1:04d}"
        clip_path = os.path.join(clip_dir, f"{clip_name}.wav")
        txt_path  = os.path.join(txt_dir,  f"{clip_name}.txt")

        chunk.export(clip_path, format="wav")

        # Placeholder transcript — user fills in the Mashi text
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# [{clip_name}]  duration: {len(chunk)/1000:.1f}s\n"
                    f"# Listen to the clip and write the Mashi text here:\n\n")

        results.append({
            "file": f"{clip_name}.wav",
            "duration_s": round(len(chunk) / 1000, 2),
            "txt": txt_path,
        })
        kept += 1
        print(f"  OK  {clip_name}.wav  {len(chunk)/1000:.1f}s")

    print(f"\nSummary:")
    print(f"  Kept   : {kept}")
    print(f"  Merged into next: {merged}")
    print(f"  Skipped (too long): {skipped}")
    total_s = sum(r["duration_s"] for r in results)
    print(f"  Total usable audio: {total_s/60:.1f} min")
    print(f"\nNext step:")
    print(f"  Open each .txt file in {txt_dir}/ and fill in the Mashi text.")
    print(f"  Then run: python scripts/03_build_metadata.py --track manual")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input",          required=True,  help="Input audio file (.aac or .mp3)")
    p.add_argument("--domain",         required=True,  choices=["numbers", "family", "time", "story", "bible"])
    p.add_argument("--speaker",        required=True,  choices=["bib", "dav", "mrl"])
    p.add_argument("--out_dir",        default="data/manual_segments")
    p.add_argument("--min_silence_ms", default=600,  type=int,   help="Minimum pause length in ms to split on")
    p.add_argument("--silence_thresh", default=-40,  type=int,   help="Silence threshold in dBFS (lower = more strict)")
    p.add_argument("--min_seg_ms",     default=1500, type=int,   help="Minimum kept segment length in ms")
    p.add_argument("--max_seg_ms",     default=12000,type=int,   help="Maximum kept segment length in ms")
    args = p.parse_args()

    main(
        args.input, args.domain, args.speaker, args.out_dir,
        args.min_silence_ms, args.silence_thresh,
        args.min_seg_ms, args.max_seg_ms,
    )
