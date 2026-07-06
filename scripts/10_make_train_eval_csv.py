"""
Split metadata_combined.csv into XTTS training CSVs (coqui formatter).

Produces, next to the combined CSV:
  metadata_train.csv   audio_file|text|speaker_name
  metadata_eval.csv    same format

The split is stratified per (speaker, domain) so every stratum keeps at
least one eval clip and the eval set stays ~5% of the data. A fixed seed
makes the split reproducible.

Usage:
  python scripts/10_make_train_eval_csv.py
"""

import os
import argparse
import pandas as pd

EVAL_FRACTION = 0.05
SEED          = 42


def main(seg_dir="data/mashi_dataset"):
    df = pd.read_csv(os.path.join(seg_dir, "metadata_combined.csv"))

    eval_rows = []
    for (_, _), grp in df.groupby(["speaker_id", "domain"]):
        n_eval = max(1, round(len(grp) * EVAL_FRACTION))
        eval_rows.append(grp.sample(n=n_eval, random_state=SEED))
    eval_df  = pd.concat(eval_rows)
    train_df = df.drop(eval_df.index)

    def to_coqui(d):
        out = pd.DataFrame()
        out["audio_file"]   = "audio/" + d["file"]
        out["text"]         = d["text"]
        out["speaker_name"] = d["speaker_id"]
        return out

    to_coqui(train_df).to_csv(os.path.join(seg_dir, "metadata_train.csv"),
                              sep="|", index=False)
    to_coqui(eval_df).to_csv(os.path.join(seg_dir, "metadata_eval.csv"),
                             sep="|", index=False)

    print(f"train: {len(train_df)} clips, {train_df.duration_s.sum()/60:.1f} min")
    print(f"eval : {len(eval_df)} clips, {eval_df.duration_s.sum()/60:.1f} min")
    print("\neval per stratum:")
    for (spk, dom), grp in eval_df.groupby(["speaker_id", "domain"]):
        print(f"  {spk}/{dom}: {len(grp)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="data/mashi_dataset")
    args = p.parse_args()
    main(args.dir)
