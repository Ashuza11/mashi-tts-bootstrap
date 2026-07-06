"""
Silence-based segmentation for continuous narrative recordings
(dav stories, bib Bible chapters).

Unlike the vocabulary recordings (script 07), narratives have pauses at
sentence/phrase boundaries. Chunks are grouped into phrase- or
paragraph-sized segments (target 4-10s, hard cap below the XTTS ~11.6s
training limit), always cutting at detected pauses.

Segments are grouped per source file: each keeps its own prefix and
segment numbering, in narrative order, so transcription can follow the
source text.

Usage:
  python scripts/09_segment_stories.py                      # To_Segment/Stories → Segmented_dataset/Stories
  python scripts/09_segment_stories.py --in_dir To_Segment/Bible --out_dir Segmented_dataset/Bible
"""

import os
import glob
import argparse
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

SR_OUT          = 22050
SILENCE_THRESH  = -40    # dBFS
MIN_SILENCE_MS  = 500    # narrative pause = sentence/phrase boundary
LONG_GAP_MS     = 1400   # gap above this always closes the segment
MAX_SPAN_MS     = 9500   # target cap; keeps clips well under XTTS ~11.6s limit
MIN_SEGMENT_MS  = 2000
PAD_MS          = 200


def segment_story(input_path, out_dir):
    name  = os.path.splitext(os.path.basename(input_path))[0]
    audio = AudioSegment.from_file(input_path)
    chunks = detect_nonsilent(
        audio,
        min_silence_len=MIN_SILENCE_MS,
        silence_thresh=SILENCE_THRESH,
    )
    print(f"\n{name} ({len(audio)/1000:.0f}s) — {len(chunks)} speech chunks")

    groups  = []
    current = []
    for s, e in chunks:
        if not current:
            current = [(s, e)]
        elif s - current[-1][1] > LONG_GAP_MS or e - current[0][0] > MAX_SPAN_MS:
            groups.append(current)
            current = [(s, e)]
        else:
            current.append((s, e))
    if current:
        groups.append(current)

    seg_num  = 1
    total_s  = 0.0
    pending  = None   # too-short group carried into the next one

    for group in groups:
        if pending:
            group = pending + group
            pending = None
        s = max(0, group[0][0] - PAD_MS)
        e = min(len(audio), group[-1][1] + PAD_MS)
        if e - s < MIN_SEGMENT_MS:
            pending = group
            continue

        clip = audio[s:e].set_channels(1).set_frame_rate(SR_OUT)
        base = f"{name}_seg{seg_num:03d}"
        clip.export(os.path.join(out_dir, f"{base}.wav"), format="wav")
        open(os.path.join(out_dir, f"{base}.txt"), "w").close()
        print(f"  {base}.wav  {len(clip)/1000:.2f}s")
        total_s += len(clip) / 1000
        seg_num += 1

    if pending:  # trailing short group — attach to previous segment
        print(f"  NOTE: trailing short chunk(s) at {pending[0][0]/1000:.1f}s dropped "
              f"({(pending[-1][1]-pending[0][0])/1000:.1f}s) — check by ear")

    print(f"  → {seg_num-1} segments, {total_s/60:.1f} min")
    return seg_num - 1, total_s


def main(in_dir, out_dir):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_dir  = os.path.join(base, in_dir)
    out_dir = os.path.join(base, out_dir)
    os.makedirs(out_dir, exist_ok=True)

    n_total, s_total = 0, 0.0
    for path in sorted(glob.glob(os.path.join(in_dir, "*.wav"))):
        n, s = segment_story(path, out_dir)
        n_total += n
        s_total += s

    print(f"\n✓ Total: {n_total} segments, {s_total/60:.1f} min")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in_dir",  default=os.path.join("To_Segment", "Stories"))
    p.add_argument("--out_dir", default=os.path.join("Segmented_dataset", "Stories"))
    args = p.parse_args()
    main(args.in_dir, args.out_dir)
