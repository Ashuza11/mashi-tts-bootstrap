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

---

## Text sources

| Domain | Text author | Format | Notes |
|---|---|---|---|
| Bible — Genesis | Padri Pierre MATABARO OFM | .txt (29 files, one per chapter) | Original from bible.com/bible/3953/GEN.1.MKB |
| Short stories | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (one file: `shi_story_dav_source_text.pdf`) | Texts written by collector, read aloud by father |
| Family vocabulary | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_family_dav_source_text.pdf`) | |
| Numbers (esabu) | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_numbers_dav_source_text.pdf`) | Sourced from existing Mashi resources |
| Calendar (nsaha) | Muhigiri Ashuza (written); David Namulabarha (recorded) | PDF (`shi_time_dav_source_text.pdf`) | Curated from murhula.com and other sources |
| Time expressions | Marius NSHOMBO / murhula.com | .txt placeholders (to be filled) | Muhigiri Ashuza will write the Mashi text after listening |

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
| Time expression text missing | All `shi_time_mrl_*.txt` files | Muhigiri Ashuza listens to each clip and writes the Mashi phrase |

---

## Dataset totals

| Category | Audio files | Approx. raw duration |
|---|---|---|
| Bible audio (all chapters) | 27 MP3s | ~10 hours |
| Bible transcripts | 28 .txt files | — |
| Short stories | 5 AAC | ~12.6 min |
| Family | 1 AAC | ~2.7 min |
| Numbers | 1 AAC | ~4.8 min |
| Calendar | 1 AAC | ~3.9 min |
| Time expressions | 12 MP3s | ~10 min |
| **Grand total audio** | **47 files** | **~10 hours 34 min** |

---

## File locations

```
/home/ashuza/2026-project/machi-project/Dataset_Mashi/
├── Bible/
│   ├── audio/          27 MP3 files  (shi_bible_bib_ch01.mp3 … ch31.mp3)
│   └── transcripts/    30 TXT files  (29 chapter texts + 1 flag file for ch13)
├── Short_stories/
│   ├── audio/          5 AAC files   (shi_story_dav_001 … 005)
│   └── documents/      1 PDF         (source text for all 5 stories)
├── Family/
│   ├── audio/          1 AAC file    (shi_family_dav_001.aac)
│   └── documents/      1 PDF         (source text)
├── Numbers/
│   ├── audio/          1 AAC file    (shi_numbers_dav_001.aac)
│   └── documents/      1 PDF         (source text)
└── Time/
    ├── audio/          13 files      (12 MP3 clock clips + 1 AAC calendar)
    ├── transcripts/    12 TXT        (placeholder files, to be filled)
    └── documents/      1 PDF         (calendar source text)
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
