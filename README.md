# mashi-tts-bootstrap

**Bootstrapping TTS for Mashi: Exploring Cross-Lingual Transfer from Kinyarwanda for an Extremely Low-Resource Bantu Language**

Mashi (also called Bashi, ISO 639-3: `shi`) is spoken by approximately 3 million people in South Kivu, eastern DRC. No TTS, ASR, or NLP tools exist for this language. This project fine-tunes a multilingual TTS model on the first Mashi speech dataset, using Kinyarwanda as a cross-lingual bridge language.

## Key contribution

Two-pipeline comparison for data-scarce TTS:
- **Track A (Automatic):** WhisperX forced alignment on Bible chapter recordings
- **Track B (Manual):** Native-speaker verse-level segmentation of the same recordings

Fine-tuning and quality comparison are run identically on both tracks.

## Dataset

The Mashi speech dataset used in this project is the first of its kind.
It contains recordings across three speakers:
- `bib` — Male speaker (~35yo), source: Padri Pierre MATABARO OFM, bible.com/bible/3953/GEN.1.MKB
- `dav` — David Namulabarha (51), native Ngweshe speaker, South Kivu, DRC (short stories, numbers, family, calendar)
- `mrl` — Female speaker (~28yo), source: murhula.com, permission granted by Marius NSHOMBO

Dataset collector: Muhigiri Ashuza (28), Mushi from Bukavu, DRC.

## Model

Base model: [Coqui XTTS v2](https://github.com/coqui-ai/TTS) — multilingual, few-shot capable.
Transfer language: Swahili (closest Bantu language supported by XTTS).

## Project structure

```
mashi-tts-bootstrap/
├── data/
│   ├── raw/                     # full Dataset_Mashi/ (gitignored, upload to Drive)
│   ├── manual_segments/         # Track B: verse-level clips + transcripts
│   └── auto_segments/           # Track A: WhisperX clips + transcripts
├── scripts/
│   ├── 01_whisperx_align.py     # forced alignment
│   ├── 02_extract_clips.py      # extract WAV clips from alignment output
│   └── 03_build_metadata.py     # build metadata.csv for TTS trainer
├── notebooks/
│   ├── 01_forced_alignment_colab.ipynb   # run on Colab
│   └── 02_finetune_xtts_colab.ipynb      # run on Colab
├── models/checkpoints/          # saved checkpoints (gitignored)
├── results/
│   ├── manual_samples/          # generated audio — manual track
│   └── auto_samples/            # generated audio — auto track
└── docs/
    └── manual_segmentation_guide.md
```

## Quickstart (Google Colab)

1. Upload `data/raw/Dataset_Mashi/` to Google Drive at `mashi-tts-bootstrap/data/raw/`
2. Open `notebooks/01_forced_alignment_colab.ipynb` → Run all (Track A)
3. Open `notebooks/02_finetune_xtts_colab.ipynb` → set `TRACK = 'auto'` → Run all
4. For Track B: follow `docs/manual_segmentation_guide.md`, then repeat step 3 with `TRACK = 'manual'`

## Citation

If you use this work, please cite:
```
Muhigiri Ashuza (2026). Bootstrapping TTS for Mashi: Cross-Lingual Transfer
from Kinyarwanda for an Extremely Low-Resource Bantu Language.
Dataset collector: Muhigiri Ashuza. Bible source: Padri Pierre MATABARO OFM.
```
