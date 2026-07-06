# mashi-tts-bootstrap

**Bootstrapping TTS for Mashi: Exploring Cross-Lingual Transfer from Kinyarwanda for a Low-Resource Bantu Language**

Mashi (also called Bashi or Shi, ISO 639-3: `shi`) is spoken by approximately 3 million people in South Kivu, eastern DRC. No TTS, ASR, or NLP tools exist for this language. This project builds the first Mashi speech dataset — 3 speakers, 5 domains, 723 curated clips — and fine-tunes a multilingual TTS model (Coqui XTTS v2) on it as a methodological contribution for low-resource languages.

---

## Research question

Can fine-tuning a multilingual TTS model on roughly one hour of Mashi audio produce intelligible Mashi speech?

> **Scope note (July 2026):** the originally planned Track A (automatic WhisperX
> forced alignment) was dropped for time reasons. The project uses a single
> curated dataset built by silence-based splitting at natural pauses, verified
> and transcribed by the collector.

---

## Key contribution

**Dataset contribution:** The first Mashi speech dataset — 3 speakers, 5 domains,
**723 clips / 67 minutes** of segmented, transcribed, TTS-ready audio
(from ~10 hours of raw Bible audio plus vocabulary, story, and clock-time recordings).

**Method contribution:** a reproducible low-resource curation pipeline —
silence-based segmentation at natural speech pauses (scripts 07/09), component-based
synthesis of clock-time clips from web audio (script 08), and casing/apostrophe
normalization (script 06) — all cutting only at silences so no word is ever split.

---

## The dataset

### Language
- **Name:** Mashi (Bashi, Shi) — `shi` (ISO 639-3)
- **Region:** South Kivu province, eastern DRC. Ngweshe, Nyangezi, Bunyakiri, Muganzo territories.
- **Script:** Latin-based with diacritics (ê, â, î, û)
- **Prior resources:** None. This is the first open Mashi speech dataset.

### Dataset collector
**Muhigiri Ashuza** (age 28, Mushi from Bukavu, South Kivu, DRC) — native/heritage speaker of Mashi. He recorded, organized, and curated all data. He is not a speaker in the recordings.

### Three speakers

| Code | Person | Age | Origin | Domains | Raw audio |
|---|---|---|---|---|---|
| `bib` | Unknown male (Padri Matabaro's Bible project) | ~35 | Unknown | Bible / Genesis | ~10 hours |
| `dav` | David Namulabarha (collector's father) | 51 | Ngweshe Nyangezi, Muganzo, South Kivu | Stories, family, numbers, calendar | ~24 min |
| `mrl` | Unknown female (murhula.com) | ~28 | Unknown | Clock time expressions | ~10 min |

### Domains and files

| Domain | Speaker | Files | Raw duration | Text source |
|---|---|---|---|---|
| Bible — Genesis (ch01–ch04 for training) | bib | `shi_bible_bib_ch01.mp3` … `ch31.mp3` | ~10 hours total; ~67 min (ch01–04) | Padri Pierre MATABARO OFM, bible.com/bible/3953/GEN.1.MKB |
| Short stories / folk tales | dav | `shi_story_dav_001` … `005` | ~12.6 min | Written by Muhigiri Ashuza; recorded by David Namulabarha |
| Family vocabulary | dav | `shi_family_dav_001.aac` | ~2.7 min | Written by Muhigiri Ashuza; recorded by David Namulabarha |
| Numbers (esabu) | dav | `shi_numbers_dav_001.aac` | ~4.8 min | Written by Muhigiri Ashuza; recorded by David Namulabarha |
| Calendar / nsaha | dav | `shi_time_dav_001_nsaha_calendar.aac` | ~3.9 min | Written by Muhigiri Ashuza; recorded by David Namulabarha |
| Clock time expressions | mrl | `shi_time_mrl_07_53.mp3` … `10_56.mp3` | ~10 min | Murhula.com — Marius NSHOMBO |

### Bible chapter coverage

27 chapters have both audio and transcript. 2 chapters are text-only (no individual audio). 1 chapter has audio but its transcript is empty and needs manual transcription.

| Status | Chapters |
|---|---|
| Audio + transcript ✓ | ch01–ch07, ch08\_09, ch10\_11, ch12, ch14–ch19, ch21–ch24, ch26–ch31 |
| Audio only — transcript to copy from source | ch13 (~11.4 min — get text at bible.com/bible/3953/GEN.13.MKB) |
| Text only — audio to re-record from source | ch20, ch25 |

### Attribution and permissions

| Content | Source | Permission |
|---|---|---|
| Bible audio | Padri Pierre MATABARO OFM, bible.com/bible/3953/GEN.1.MKB | Recorded from public source; attribution required |
| Bible transcripts | Same source | Same |
| Stories, numbers, family, calendar — text | Written by Muhigiri Ashuza | — |
| Stories, numbers, family, calendar — audio | Recorded by David Namulabarha | Family member; explicit consent |
| Time expressions audio | murhula.com | Permission granted by Marius NSHOMBO |

---

## Model

**Base model:** [Coqui XTTS v2](https://github.com/coqui-ai/TTS) — multilingual, few-shot capable, runs on Google Colab T4 GPU.
**Transfer language proxy:** Spanish (`es`). XTTS v2 supports no Bantu language
(its 17 languages include neither Swahili nor Kinyarwanda), so the closest
*phonetic* proxy is used instead: Spanish shares Mashi's five pure vowels
/a e i o u/ and open CV syllable structure. The Spanish text frontend also
expands the clock-time digits ("9:05") deterministically, keeping training and
inference consistent.
**Why not Kinyarwanda/Swahili directly:** neither has an XTTS v2 checkpoint. The
poster title refers to the broader cross-lingual transfer concept across Bantu
languages.

---

## Project structure

```
mashi-tts-bootstrap/
├── data/
│   └── mashi_dataset/                # THE DATASET — upload this folder to Drive
│       ├── audio/                    # 723 wav clips, 22050 Hz mono, 2.0–11.3 s
│       ├── transcripts/              # one .txt per clip, normalized Mashi text
│       ├── metadata_combined.csv     # full record: file, text, speaker, domain, duration
│       ├── metadata_train.csv        # coqui format (audio_file|text|speaker_name) — 687 clips
│       ├── metadata_eval.csv         # held-out eval set — 36 clips
│       └── speaker_references/       # ref_bib/dav/mrl.wav for voice conditioning
├── scripts/
│   ├── 01–04  (legacy: WhisperX track + early splitter — kept for reference)
│   ├── 05_build_combined_metadata.py # build metadata_combined.csv + speaker references
│   ├── 06_normalize_text.py          # lowercase + sentence-case transcripts
│   ├── 07_segment_short_domains.py   # segment dav vocabulary + mrl recordings
│   ├── 08_build_mrl_clock_clips.py   # build clock clips from murhula.com components
│   ├── 09_segment_stories.py         # segment narratives (stories + Bible chapters)
│   └── 10_make_train_eval_csv.py     # stratified train/eval split in coqui format
├── notebooks/
│   └── 02_finetune_xtts_colab.ipynb  # fine-tune XTTS v2 — run on Colab
├── models/checkpoints/               # saved checkpoints — gitignored
├── results/samples/                  # generated test audio
└── docs/
    ├── DATA_CARD.md                  # full dataset documentation
    ├── combined_dataset_guide.md     # how the dataset was built (record + extension guide)
    └── manual_segmentation_guide.md  # Audacity step-by-step (reference)
```

Raw source audio (`To_Segment/`) and the per-domain working copy
(`Segmented_dataset/`) are archived outside the repository; the murhula.com
clock components are preserved with them for reproducibility.

---

## Quickstart (Google Colab)

The dataset is already segmented, transcribed, and split — no preparation needed.

1. Upload `data/mashi_dataset/` to Google Drive under `My Drive/mashi-tts-bootstrap/data/`
2. Open the notebook in Colab:
   [`02_finetune_xtts_colab.ipynb`](https://colab.research.google.com/github/Ashuza11/mashi-tts-bootstrap/blob/main/notebooks/02_finetune_xtts_colab.ipynb)
3. Runtime → Change runtime type → **GPU (T4)** → Run all
4. Listen to the generated samples in `results/samples/` on Drive

To rebuild the dataset from the raw audio archive: scripts 07 → 08 → 09,
copy the segments into `data/mashi_dataset/{audio,transcripts}`, then
scripts 06 → 05 → 10.

---

## Final training dataset

| Speaker | Domain | Clips | Minutes |
|---|---|---|---|
| bib | Bible — Genesis ch01–04 | 183 | 24.2 |
| dav | Short stories | 109 | 12.5 |
| dav | Numbers | 39 | 3.5 |
| dav | Family | 25 | 3.0 |
| dav | Calendar | 31 | 3.3 |
| mrl | Clock times | 336 | 20.9 |
| **Total** | | **723 clips** | **67.4 min** |

All clips are 2.0–11.3 s, mono 22050 Hz WAV, cut only at natural pauses.
Split: 687 train / 36 eval (stratified per speaker+domain, seed 42).

> **mrl provenance note:** the clock-time domain is built from the 95 component
> announcements used by murhula.com's talking clock (18 hours, 59 minutes,
> 18 exact-hour phrases; hours 1–6 do not exist on the site). 13 times were
> screen-recorded; the remaining clips are unique hour+minute combinations
> assembled the same way the site plays them (permission: Marius NSHOMBO).
> Per-speaker minutes for mrl therefore recombine 95 unique recordings —
> disclosed here to keep the totals honest.

---

## Citation

```
Muhigiri Ashuza (2026). Bootstrapping TTS for Mashi: Exploring Cross-Lingual
Transfer from Kinyarwanda for a Low-Resource Bantu Language.

Bible audio source: Padri Pierre MATABARO OFM, bible.com/bible/3953/GEN.1.MKB
Time expressions source: murhula.com — permission: Marius NSHOMBO
Additional recordings: David Namulabarha (Ngweshe Nyangezi, South Kivu, DRC)
```
