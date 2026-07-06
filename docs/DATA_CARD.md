# Data Card — Mashi (Shi) Speech Dataset

The first open speech dataset for the Mashi language (ISO 639-3: `shi`),
spoken by the Bashi people of South Kivu, eastern Democratic Republic of Congo.

---

## Language

| Field | Value |
|---|---|
| Language name | Mashi (also: Mashi, Bashi, Shi, Ki-Shi) |
| ISO 639-3 code | `shi` |
| Language family | Bantu, Niger-Congo |
| Related languages | Kinyarwanda, Kirundi, Swahili (more distant) |
| Region | South Kivu province, eastern DRC — Ngweshe, Nyangezi, Bunyakiri, Muganzo territories |
| Estimated speakers | ~3 million |
| Script | Latin-based with diacritics: ê, â, î, û, and tone markings |
| Prior digital resources | None. No TTS, ASR, NLP dataset, or language model existed before this project. |

---

## Dataset creator

**Muhigiri Ashuza**
- Age: 28
- Origin: Bukavu, South Kivu, DRC
- Identity: Mushi (Bashi people), native/heritage Mashi speaker
- Role: Dataset collector and curator — NOT a speaker in the recordings
- Contact: ashuza1411@gmail.com

---

## Speakers

### Speaker `bib` — Bible narrator

| Field | Value |
|---|---|
| Identity | Unknown male speaker |
| Estimated age | ~35 years old |
| Gender | Male |
| Origin | Unknown |
| Source | Padri Pierre MATABARO OFM's Mashi Bible audio project |
| Source URL | bible.com/bible/3953/GEN.1.MKB |
| How recorded | Muhigiri Ashuza recorded the audio stream while listening from the online source |
| Permission | Recorded from a public religious resource; source credited in citation |
| Domains | Biblical narrative — Old Testament, Book of Genesis (Murhondero), chapters 1–31 |
| Total raw audio | ~10 hours (633 MB of MP3 files) |
| Format | MP3, 128kbps |

### Speaker `dav` — David Namulabarha

| Field | Value |
|---|---|
| Full name | David Namulabarha |
| Age | 51 years old |
| Gender | Male |
| Origin | Ngweshe Nyangezi, Muganzo, South Kivu province, DRC |
| Relationship to collector | Father of Muhigiri Ashuza |
| Native dialect | Ngweshe dialect of Mashi |
| Permission | Explicit family consent; Muhigiri Ashuza wrote the texts, David recorded them |
| Domains | Short stories, family vocabulary, numbers, calendar (days and months) |
| Total raw audio | ~24 minutes |
| Format | AAC |
| Recording style | Vocabulary items (numbers, family, calendar) read one by one with natural pauses. Stories read as continuous narrative. |

**David's recordings in detail:**

| File | Domain | Duration | Content |
|---|---|---|---|
| `shi_story_dav_001_budiba_mulalwe_bona_mukage.aac` | Short story | ~2 min | Folk tale |
| `shi_story_dav_002_ifunze_lya_mwali_kadege.aac` | Short story | ~5 min | Folk tale |
| `shi_story_dav_003_kurhenga_kwobwami_bwe_bushi.aac` | Short story | ~3 min | Historical narrative |
| `shi_story_dav_004_murhondero_gw_abantu.aac` | Short story | ~2 min | Folk tale |
| `shi_story_dav_005_obufumu_bwa_m_kagugu.aac` | Short story | ~1 min | Folk tale |
| `shi_family_dav_001.aac` | Family vocabulary | ~2.7 min | Family relationship terms |
| `shi_numbers_dav_001.aac` | Numbers (esabu) | ~4.8 min | Mashi number words, one per pause |
| `shi_time_dav_001_nsaha_calendar.aac` | Calendar (nsaha) | ~3.9 min | Days of the week, months, read one per pause |

### Speaker `mrl` — Murhula.com woman

| Field | Value |
|---|---|
| Identity | Unknown female speaker |
| Estimated age | ~27–30 years old |
| Gender | Female |
| Origin | Unknown |
| Source | murhula.com — a Mashi cultural and language website |
| Permission | Granted by Marius NSHOMBO, website owner and community member |
| How recorded | Muhigiri Ashuza recorded audio from murhula.com watch/video content |
| Domains | Clock time expressions |
| Total raw audio | ~10 minutes (12 clips, 36–75 seconds each) |
| Format | MP3 |

**mrl's recordings in detail:**

| File | Time expressed | Duration |
|---|---|---|
| `shi_time_mrl_07_53.mp3` | 7:53 AM | ~44s |
| `shi_time_mrl_07_58.mp3` | 7:58 AM | ~36s |
| `shi_time_mrl_08_00.mp3` | 8:00 AM | ~36s |
| `shi_time_mrl_08_07.mp3` | 8:07 AM | ~55s |
| `shi_time_mrl_08_50.mp3` | 8:50 AM | ~46s |
| `shi_time_mrl_09_00.mp3` | 9:00 AM | ~41s |
| `shi_time_mrl_09_06.mp3` | 9:06 AM | ~47s |
| `shi_time_mrl_09_26.mp3` | 9:26 AM | ~55s |
| `shi_time_mrl_10_15.mp3` | 10:15–10:16 AM | ~64s |
| `shi_time_mrl_10_22.mp3` | 10:22 AM | ~75s |
| `shi_time_mrl_10_42.mp3` | 10:42 AM | ~59s |
| `shi_time_mrl_10_56.mp3` | 10:56 AM | ~57s |

**Component-synthesized clips (July 2026).** murhula.com's talking clock plays two
files back-to-back: `hours/{H}.mp3` + `minutes/{M}.mp3` (or `hours_special/{H}.mp3`
for exact hours). With the owner's permission, all 95 existing components were
downloaded (archived with the raw sources in `To_Segment/Time/murhula_components/`;
hours 1–6 do not exist on the server). Script `08_build_mrl_clock_clips.py` assembles unique
hour+minute combinations exactly as the site plays them (150 ms gap), skipping the
13 screen-recorded times. Final mrl domain: **336 clips, 20.9 min**, every
component used ≥3 times, every minute 0–59 covered. Because these recombine 95
unique recordings, mrl's per-speaker minutes overstate its acoustic diversity —
state this in any publication. One server file (`minutes/35.mp3`) contained an
unedited 38 s session; the first take was kept (original preserved as
`35_original_server.mp3`).

---

## Text sources

| Domain | Text author | Format | Notes |
|---|---|---|---|
| Bible — Genesis | Padri Pierre MATABARO OFM | .txt (29 files, one per chapter) | Original from bible.com/bible/3953/GEN.1.MKB |
| Short stories | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (one file: `shi_story_dav_source_text.pdf`) | Texts written by collector, read aloud by father |
| Family vocabulary | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_family_dav_source_text.pdf`) | |
| Numbers (esabu) | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_numbers_dav_source_text.pdf`) | Sourced from existing Mashi resources |
| Calendar (nsaha) | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_time_dav_source_text.pdf`) | Curated from murhula.com and other sources |
| Time expressions | Marius NSHOMBO / murhula.com | .txt per clip (complete) | Transcripts carry the time as digits (`9:05`) — the model learns the digit→speech mapping through the training-language frontend |

---

## Naming convention

```
shi_{category}_{speaker}_{id}.{ext}
│    │          │         │
│    │          │         └── chapter id (ch01), sequence (001), or time value (07_53)
│    │          └──────────── bib | dav | mrl
│    └─────────────────────── bible | story | family | numbers | time
└──────────────────────────── ISO 639-3 language code for Shi/Mashi
```

---

## Gaps to complete

| Gap | File(s) | How to fill |
|---|---|---|
| Transcript missing locally | `shi_bible_bib_ch13.mp3` (~11.4 min) | Go to bible.com/bible/3953/GEN.13.MKB, copy the Mashi text, save as `shi_bible_bib_ch13.txt` |
| No audio for ch20, ch25 | `shi_bible_bib_ch20_textonly.txt`, `shi_bible_bib_ch25_textonly.txt` | Re-record from source: bible.com/bible/3953/GEN.20.MKB and GEN.25.MKB |
| ch08_09 audio has tail from ch10 | `shi_bible_bib_ch08_09.mp3` | Trim the last portion before segmentation, or note in metadata |
| ~~Time expression text missing~~ | ~~All `shi_time_mrl_*.txt`~~ | **Done (July 2026)** — every clip carries its time in `H:MM` format |
| mrl hours 1–6 | murhula.com `hours/1–6.mp3` | Do not exist on the server; only fixable if the site owner records them |

**Segmentation status (July 2026): complete.** All five domains are segmented and
transcribed — 723 clips / 67.4 min in `data/mashi_dataset/`. Bible chapters
ch05+ remain unsegmented raw audio (only ch01–ch04 are in the training set).

---

## Dataset totals

**Raw source audio:**

| Category | Audio files | Approx. raw duration |
|---|---|---|
| Bible audio (all chapters) | 27 MP3s | ~10 hours |
| Bible transcripts | 28 .txt files | — |
| Short stories | 5 AAC | ~12.6 min |
| Family | 1 AAC | ~2.7 min |
| Numbers | 1 AAC | ~4.8 min |
| Calendar | 1 AAC | ~3.9 min |
| Time expressions | 12 MP3s + 95 components | ~10 min + ~3 min |
| **Grand total audio** | **47 files** | **~10 hours 34 min** |

**Final segmented training dataset (July 2026):**

| Speaker | Domain | Clips | Minutes |
|---|---|---|---|
| bib | Bible (Genesis ch01–04) | 183 | 24.2 |
| dav | Short stories | 109 | 12.5 |
| dav | Numbers | 39 | 3.5 |
| dav | Family | 25 | 3.0 |
| dav | Calendar | 31 | 3.3 |
| mrl | Clock times | 336 | 20.9 |
| **Total** | | **723** | **67.4** |

All clips: mono 22050 Hz WAV, 2.0–11.3 s, cut only at natural silences.
Transcripts: lowercase with sentence-case, ASCII apostrophes, diacritics
preserved; clock times written as digits (`9:05`). Train/eval split:
687 / 36, stratified per speaker+domain (`metadata_train.csv` /
`metadata_eval.csv`, coqui format).

---

## File locations

**Training dataset (in the repository):**

```
data/mashi_dataset/
├── audio/                  723 WAV clips (22050 Hz mono)
├── transcripts/            723 TXT files (normalized Mashi text)
├── metadata_combined.csv   file | text | speaker_id | domain | duration_s
├── metadata_train.csv      coqui format — 687 clips
├── metadata_eval.csv       coqui format — 36 clips
└── speaker_references/     ref_bib.wav, ref_dav.wav, ref_mrl.wav
```

**Raw source archive (kept outside the repository):**

```
To_Segment/                 original recordings per domain
├── Bible/                  4 chapter WAVs + transcripts (ch01–ch04)
├── Stories/                5 story WAVs + source PDF
├── Family/  Numbers/       1 WAV + source PDF each
└── Time/                   calendar WAV, 12 clock recordings, source PDF
    └── murhula_components/ 95 MP3 components from murhula.com talking clock
Segmented_dataset/          per-domain working copy of the curated clips
Dataset_Mashi/              full raw collection incl. Bible ch05–ch31 (~10 h)
```

---

## Citation

```
Muhigiri Ashuza (2026). Bootstrapping TTS for Mashi: Exploring Cross-Lingual Transfer
from Kinyarwanda for a Low-Resource Bantu Language.

Speakers:
  - Bible narrator: Padri Pierre MATABARO OFM (source: bible.com/bible/3953/GEN.1.MKB)
  - David Namulabarha, 51, Ngweshe Nyangezi, Muganzo, South Kivu, DRC
  - Female time expressions narrator (source: murhula.com, permission: Marius NSHOMBO)

Dataset collected and curated by: Muhigiri Ashuza, Bukavu, DRC, 2025–2026.
```
