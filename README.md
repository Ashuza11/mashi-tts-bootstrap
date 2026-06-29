# mashi-tts-bootstrap

**Bootstrapping TTS for Mashi: Exploring Cross-Lingual Transfer from Kinyarwanda for a Low-Resource Bantu Language**

Mashi (also called Bashi or Shi, ISO 639-3: `shi`) is spoken by approximately 3 million people in South Kivu, eastern DRC. No TTS, ASR, or NLP tools exist for this language. This project fine-tunes a multilingual TTS model on the first Mashi speech dataset and compares two data curation pipelines — automatic and manual — as a methodological contribution for low-resource languages.

---

## Research questions

1. Can fine-tuning a multilingual TTS model on fewer than 90 minutes of Mashi audio produce intelligible Mashi speech?
2. Does manual native-speaker segmentation produce better TTS output than automatic forced alignment (WhisperX) on the same data?

---

## Key contribution

**Two-pipeline comparison for data-scarce TTS:**
- **Track A (Automatic):** WhisperX forced alignment on chapter-level recordings → clips
- **Track B (Manual):** Native-speaker segmentation at natural speech boundaries + silence-based splitting

Fine-tuning is run identically on both tracks. Output quality is compared qualitatively and (if possible) with MOS scores from native listeners.

**Dataset contribution:** The first Mashi speech dataset — 3 speakers, 5 domains, ~10 hours of raw audio (Bible) plus ~34 minutes of vocabulary and narrative recordings.

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
**Transfer language proxy:** Swahili (`sw`) — the closest Bantu language supported by XTTS v2.
**Why not Kinyarwanda directly:** XTTS v2 does not include a Kinyarwanda checkpoint; Swahili is used as the nearest available Bantu proxy. The poster title refers to the broader cross-lingual transfer concept across Bantu languages.

---

## Project structure

```
mashi-tts-bootstrap/
├── data/
│   ├── raw/                          # full Dataset_Mashi/ — gitignored, upload to Drive
│   ├── manual_segments/              # Track B: segmented clips + transcripts
│   │   ├── audio/
│   │   ├── transcripts/
│   │   └── speaker_references/       # reference wavs per speaker (auto-generated)
│   └── auto_segments/                # Track A: WhisperX clips + transcripts
│       ├── audio/
│       ├── transcripts/
│       └── alignment_json/
├── scripts/
│   ├── 01_whisperx_align.py          # Track A: forced alignment
│   ├── 02_extract_clips.py           # Track A: extract WAV clips from JSON
│   ├── 03_build_metadata.py          # build metadata.csv per track
│   ├── 04_split_on_silence.py        # Track B: silence-based split for dav vocabulary
│   └── 05_build_combined_metadata.py # merge all 3 speakers into one CSV with speaker/domain columns
├── notebooks/
│   ├── 01_forced_alignment_colab.ipynb   # Track A — run on Colab
│   └── 02_finetune_xtts_colab.ipynb      # fine-tune XTTS v2 — run on Colab, set TRACK variable
├── models/checkpoints/               # saved checkpoints — gitignored
├── results/
│   ├── manual_samples/               # generated audio — Track B model
│   └── auto_samples/                 # generated audio — Track A model
└── docs/
    ├── DATA_CARD.md                  # full dataset documentation
    ├── combined_dataset_guide.md     # how to segment and combine all 3 speakers
    └── manual_segmentation_guide.md  # Audacity step-by-step for Bible chapters
```

---

## Quickstart (Google Colab)

**Before you start:** Complete manual segmentation following `docs/combined_dataset_guide.md`, then upload `data/` to Google Drive under `My Drive/mashi-tts-bootstrap/`.

**Track A — Automatic:**
1. Open `notebooks/01_forced_alignment_colab.ipynb` → Runtime → Run all
2. Open `notebooks/02_finetune_xtts_colab.ipynb` → set `TRACK = 'auto'` → Run all

**Track B — Manual:**
1. Follow `docs/combined_dataset_guide.md` to segment all 3 speakers locally
2. Run `python scripts/05_build_combined_metadata.py --track manual`
3. Upload `data/manual_segments/` to Drive
4. Open `notebooks/02_finetune_xtts_colab.ipynb` → set `TRACK = 'manual'` → Run all

---

## Expected training dataset size

| Speaker | Domain | Est. clips | Est. minutes |
|---|---|---|---|
| bib | Bible (ch01–04) | ~320 | ~52 |
| dav | Short stories | ~60 | ~11 |
| dav | Numbers | ~30 | ~4 |
| dav | Family | ~20 | ~3 |
| dav | Calendar | ~25 | ~4 |
| mrl | Time expressions | ~15 | ~8 |
| **Total** | | **~470 clips** | **~82 minutes** |

---

## Citation

```
Muhigiri Ashuza (2026). Bootstrapping TTS for Mashi: Exploring Cross-Lingual
Transfer from Kinyarwanda for a Low-Resource Bantu Language.

Bible audio source: Padri Pierre MATABARO OFM, bible.com/bible/3953/GEN.1.MKB
Time expressions source: murhula.com — permission: Marius NSHOMBO
Additional recordings: David Namulabarha (Ngweshe Nyangezi, South Kivu, DRC)
```
