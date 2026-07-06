"""
Build mrl clock-time training clips from murhula.com component audio.

The site (murhula.com, permission: Marius NSHOMBO) announces the time by
playing two files back-to-back:
    audio/nsa/audios/hours/{H}.mp3   +   audio/nsa/audios/minutes/{M}.mp3
and a single file for exact hours:
    audio/nsa/audios/hours_special/{H}.mp3

Hours 1-6 do not exist on the server (404). Available: 0, 7-23.

This script generates a BALANCED sample rather than all 18x59 combos:
  - one exact-hour clip per available hour
  - one combo per minute 1-59, hours assigned round-robin
  - times already covered by Ashuza's screen recordings are skipped
so every component file appears at least once without flooding the
dataset with redundant recombinations.

Output: Segmented_dataset/Time/shi_time_mrl_{HH}_{MM}_seg001.wav
        Segmented_dataset/Time/shi_time_mrl_{HH}_{MM}_seg001.txt   ("H:MM")
"""

import os
from pydub import AudioSegment

AVAILABLE_HOURS = [0] + list(range(7, 24))          # server has no 1-6
GAP_MS          = 150                                # pause between hour and minute
SR_OUT          = 22050

# Times already present as screen recordings in Segmented_dataset/Time
ALREADY_RECORDED = {
    (7, 53), (7, 58), (8, 0), (8, 7), (8, 50),
    (9, 0), (9, 6), (9, 26),
    (10, 15), (10, 16), (10, 22), (10, 42), (10, 56),
}


def build_plan(rounds=1):
    """
    Return list of (hour, minute) pairs to generate. minute=0 → exact hour.

    rounds — how many hour+minute combos per minute. Round 1 skips minutes
    already covered by the screen recordings; later rounds cover every
    minute again with a rotated hour assignment, producing new unique
    pairs (existing output files are skipped at export time).
    """
    plan = []

    # Exact hours not already recorded
    recorded_exact = {h for h, m in ALREADY_RECORDED if m == 0}
    for h in AVAILABLE_HOURS:
        if h not in recorded_exact:
            plan.append((h, 0))

    # Round 1: one combo per uncovered minute, hour round-robin
    recorded_minutes = {m for _, m in ALREADY_RECORDED if m != 0}
    seen = set(ALREADY_RECORDED)
    uncovered = [m for m in range(1, 60) if m not in recorded_minutes]
    for i, m in enumerate(uncovered):
        h = AVAILABLE_HOURS[i % len(AVAILABLE_HOURS)]
        plan.append((h, m))
        seen.add((h, m))

    # Rounds 2+: every minute again, hour assignment rotated per round
    n = len(AVAILABLE_HOURS)
    for r in range(1, rounds):
        for i, m in enumerate(range(1, 60)):
            h = AVAILABLE_HOURS[(i + r * 7) % n]   # 7 is coprime with 18 → good spread
            if (h, m) in seen:
                h = AVAILABLE_HOURS[(i + r * 7 + 1) % n]
            if (h, m) in seen:
                continue
            plan.append((h, m))
            seen.add((h, m))

    return plan


def main(rounds=1):
    base       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    comp_dir   = os.path.join(base, "To_Segment", "Time", "murhula_components")
    out_dir    = os.path.join(base, "Segmented_dataset", "Time")
    os.makedirs(out_dir, exist_ok=True)

    plan    = build_plan(rounds)
    total_s = 0.0
    skipped = 0

    for h, m in plan:
        base_name = f"shi_time_mrl_{h:02d}_{m:02d}_seg001"
        if os.path.exists(os.path.join(out_dir, f"{base_name}.wav")):
            skipped += 1
            continue
        if m == 0:
            clip = AudioSegment.from_mp3(os.path.join(comp_dir, "hours_special", f"{h}.mp3"))
        else:
            hour_a = AudioSegment.from_mp3(os.path.join(comp_dir, "hours", f"{h}.mp3"))
            min_a  = AudioSegment.from_mp3(os.path.join(comp_dir, "minutes", f"{m}.mp3"))
            clip   = hour_a + AudioSegment.silent(duration=GAP_MS) + min_a

        clip = clip.set_channels(1).set_frame_rate(SR_OUT)
        clip.export(os.path.join(out_dir, f"{base_name}.wav"), format="wav")
        with open(os.path.join(out_dir, f"{base_name}.txt"), "w", encoding="utf-8") as f:
            f.write(f"{h}:{m:02d}")

        total_s += len(clip) / 1000
        print(f"  {base_name}.wav  {len(clip)/1000:.2f}s  → \"{h}:{m:02d}\"")

    n_exact = sum(1 for _, m in plan if m == 0)
    print(f"\n→ plan: {len(plan)} ({n_exact} exact hours + {len(plan)-n_exact} combos) | "
          f"skipped existing: {skipped} | new audio: {total_s/60:.1f} min")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--rounds", type=int, default=1,
                   help="Combo rounds per minute (1 = original balanced sample)")
    args = p.parse_args()
    main(args.rounds)
