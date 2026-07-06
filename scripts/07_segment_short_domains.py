"""
Segment dav vocabulary recordings (Numbers, Family, Calendar) and mrl clock recordings.

dav  → group non-silent chunks into 4-10s segments, empty .txt placeholder
mrl  → extract each spoken repetition as its own segment, .txt = time "H:MM"

Output: Segmented_dataset/{Numbers,Family,Time}/
"""

import os
import re
import sys
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from scipy.signal import fftconvolve

# ── Audio params ───────────────────────────────────────────────────────────────
SR_OUT       = 22050
CHANNELS_OUT = 1

# ── dav grouping params ────────────────────────────────────────────────────────
SILENCE_THRESH  = -42   # dBFS — audio below this = silence
MIN_SILENCE_MS  = 700   # minimum gap to consider as silence between chunks
LONG_GAP_MS     = 2200  # gap above this always closes the current group
MAX_SPAN_MS     = 8000  # max span (first_start → last_end) per group
MIN_SEGMENT_MS  = 2000  # discard groups shorter than this
PAD_MS          = 200   # silence padding kept on each side of a segment

# ── mrl params ─────────────────────────────────────────────────────────────────
MRL_SILENCE_THRESH = -42
MRL_MIN_SILENCE_MS = 500
MRL_PAD_MS         = 150


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def load_as_mono(path, sr=16000):
    """Load audio, mix to mono, resample — returns numpy float32 array."""
    audio = AudioSegment.from_file(path)
    audio = audio.set_channels(1).set_frame_rate(sr)
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    samples /= np.iinfo(audio.array_type).max
    return samples, sr


def find_segment_end_in_original(original_path, segment_path):
    """
    Cross-correlate segment against original to find where segment ends.
    Returns end position in milliseconds.
    """
    orig, sr  = load_as_mono(original_path)
    seg,  _   = load_as_mono(segment_path, sr=sr)

    if len(seg) > len(orig):
        print("  WARNING: segment longer than original — skipping cross-correlation")
        return None

    # Normalised cross-correlation via FFT
    correlation = fftconvolve(orig, seg[::-1], mode="valid")
    offset_samples = int(np.argmax(np.abs(correlation)))
    end_samples    = offset_samples + len(seg)
    end_ms         = int(end_samples / sr * 1000)
    print(f"  Cross-correlation: segment ends at {end_ms/1000:.2f}s in original")
    return end_ms


def export_segment(audio_slice, out_dir, base_name, txt_content=""):
    """Resample, convert to mono, export wav + txt."""
    seg = audio_slice.set_channels(CHANNELS_OUT).set_frame_rate(SR_OUT)
    wav_path = os.path.join(out_dir, f"{base_name}.wav")
    txt_path = os.path.join(out_dir, f"{base_name}.txt")
    seg.export(wav_path, format="wav")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)
    return len(seg) / 1000  # duration in seconds


# ──────────────────────────────────────────────────────────────────────────────
# dav segmentation
# ──────────────────────────────────────────────────────────────────────────────

def segment_dav(input_path, out_dir, start_seg_num=1, skip_first_ms=0):
    """
    Group non-silent chunks of a dav recording into TTS-ready segments.

    skip_first_ms  — skip this many ms from the start of the source (used for
                     calendar where seg001/seg002 were already done manually).
    start_seg_num  — first segment number to use.
    """
    print(f"\n[dav] {os.path.basename(input_path)}")
    audio    = AudioSegment.from_file(input_path)
    full_dur = len(audio)
    working  = audio[skip_first_ms:] if skip_first_ms else audio

    chunks = detect_nonsilent(
        working,
        min_silence_len=MIN_SILENCE_MS,
        silence_thresh=SILENCE_THRESH,
    )
    print(f"  Source: {full_dur/1000:.1f}s total, working from {skip_first_ms/1000:.1f}s")
    print(f"  Detected {len(chunks)} non-silent regions")

    # Greedy span grouping
    groups = []
    current = []

    for s, e in chunks:
        if not current:
            current = [(s, e)]
        else:
            gap  = s - current[-1][1]
            span = e - current[0][0]
            if gap > LONG_GAP_MS or span > MAX_SPAN_MS:
                groups.append(current)
                current = [(s, e)]
            else:
                current.append((s, e))

    if current:
        groups.append(current)

    file_id  = os.path.splitext(os.path.basename(input_path))[0]
    seg_num  = start_seg_num
    total_s  = 0.0
    exported = 0

    for group in groups:
        s   = max(0, group[0][0] - PAD_MS)
        e   = min(len(working), group[-1][1] + PAD_MS)
        dur = e - s
        if dur < MIN_SEGMENT_MS:
            continue

        base = f"{file_id}_seg{seg_num:03d}"
        dur_s = export_segment(working[s:e], out_dir, base, txt_content="")
        print(f"  {base}.wav  {dur_s:.2f}s")
        total_s += dur_s
        seg_num += 1
        exported += 1

    print(f"  → {exported} segments, {total_s/60:.1f} min total")
    return seg_num  # next available number


# ──────────────────────────────────────────────────────────────────────────────
# mrl clock segmentation
# ──────────────────────────────────────────────────────────────────────────────

def parse_mrl_times(filename):
    """
    Extract time(s) from an mrl filename.

    shi_time_mrl_07_53.wav      →  ["7:53"]
    shi_time_mrl_10_15_16.wav   →  ["10:15", "10:16"]  (two captures, time changed)
    """
    stem = os.path.splitext(os.path.basename(filename))[0]
    # Remove prefix up to and including 'mrl_'
    m = re.match(r".*_mrl_([\d_]+)$", stem)
    if not m:
        raise ValueError(f"Cannot parse mrl time from: {filename}")
    parts = m.group(1).split("_")   # e.g. ["07","53"] or ["10","15","16"]

    if len(parts) == 2:
        h, mi = parts
        return [f"{int(h)}:{mi}"]   # "7:53" — no leading zero on hour
    elif len(parts) == 3:
        h, m1, m2 = parts
        return [f"{int(h)}:{m1}", f"{int(h)}:{m2}"]
    else:
        raise ValueError(f"Unexpected time parts: {parts} in {filename}")


def segment_mrl(input_path, out_dir):
    """
    Extract each non-silent region (repetition) from an mrl clock file.

    For files with two captured times (10_15_16), assign the first half of
    regions to time1 and the second half to time2.
    """
    print(f"\n[mrl] {os.path.basename(input_path)}")
    audio  = AudioSegment.from_file(input_path)
    times  = parse_mrl_times(input_path)
    chunks = detect_nonsilent(
        audio,
        min_silence_len=MRL_MIN_SILENCE_MS,
        silence_thresh=MRL_SILENCE_THRESH,
    )
    n      = len(chunks)
    print(f"  Duration: {len(audio)/1000:.1f}s | {n} repetitions | times: {times}")

    # Assign each chunk to a time label
    if len(times) == 1:
        labels = [times[0]] * n
    else:
        # Two times: split chunks evenly (first half → time[0], rest → time[1])
        mid    = n // 2
        labels = [times[0]] * mid + [times[1]] * (n - mid)

    file_id      = os.path.splitext(os.path.basename(input_path))[0]
    seg_counters = {}  # track per-time index for the 2-time case

    for i, ((s, e), label) in enumerate(zip(chunks, labels)):
        s_pad = max(0, s - MRL_PAD_MS)
        e_pad = min(len(audio), e + MRL_PAD_MS)

        # Segment number: 001, 002, ... per source file (not per time)
        seg_idx = i + 1
        base    = f"{file_id}_seg{seg_idx:03d}"
        dur_s   = export_segment(audio[s_pad:e_pad], out_dir, base, txt_content=label)
        print(f"  {base}.wav  {dur_s:.2f}s  → \"{label}\"")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    base    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    to_seg  = os.path.join(base, "To_Segment")
    out_seg = os.path.join(base, "Segmented_dataset")

    # ── Numbers ────────────────────────────────────────────────────────────────
    segment_dav(
        input_path  = os.path.join(to_seg, "Numbers", "shi_numbers_dav_001.wav"),
        out_dir     = os.path.join(out_seg, "Numbers"),
        start_seg_num = 1,
    )

    # ── Family ─────────────────────────────────────────────────────────────────
    segment_dav(
        input_path  = os.path.join(to_seg, "Family", "shi_family_dav_001.wav"),
        out_dir     = os.path.join(out_seg, "Family"),
        start_seg_num = 1,
    )

    # ── Calendar (continue from seg003) ────────────────────────────────────────
    cal_src  = os.path.join(to_seg,  "Time", "shi_time_dav_001_nsaha_calendar.wav")
    cal_out  = os.path.join(out_seg, "Time")
    seg002   = os.path.join(cal_out, "shi_time_dav_001_nsaha_calendar_seg002.wav")

    print(f"\nFinding end of calendar seg002 via cross-correlation …")
    end_ms = find_segment_end_in_original(cal_src, seg002)

    if end_ms is None:
        # Fallback: rough estimate based on accumulated speech duration
        # seg001 + seg002 = ~19s of speech; leading silence ~6.5s → ~25.5s offset
        end_ms = 25500
        print(f"  Fallback: using {end_ms/1000:.1f}s offset")

    segment_dav(
        input_path    = cal_src,
        out_dir       = cal_out,
        start_seg_num = 3,
        skip_first_ms = end_ms,
    )

    # ── mrl clock files ────────────────────────────────────────────────────────
    mrl_dir = os.path.join(to_seg, "Time")
    mrl_files = sorted(
        f for f in os.listdir(mrl_dir)
        if f.startswith("shi_time_mrl") and f.endswith(".wav")
    )
    for fname in mrl_files:
        segment_mrl(
            input_path = os.path.join(mrl_dir, fname),
            out_dir    = os.path.join(out_seg, "Time"),
        )

    print("\n✓ All done.")


if __name__ == "__main__":
    main()
