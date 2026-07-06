# Combined 3-Speaker Dataset Guide
## Mashi TTS — Training Data Curation

> **STATUS (July 2026): segmentation and transcription are COMPLETE.**
> The final dataset (723 clips, 67.4 min) lives in `data/mashi_dataset/`
> with `metadata_train.csv` / `metadata_eval.csv` ready for the fine-tuning
> notebook. The steps below are kept as the record of how it was built and
> how to extend it (e.g. adding Bible chapters ch05+ with
> `scripts/09_segment_stories.py --in_dir ... --out_dir ...`).

---

## Why combine all three voices

A single-speaker TTS model learns only one person's pronunciation and prosody.
Using three speakers covering different domains gives the model:
- **Phoneme coverage** — different domains use different vocabulary and sounds
- **Speaker diversity** — the model learns Mashi phonology, not just one person's accent
- **Register diversity** — formal Bible narration vs storytelling vs vocabulary listing

This is scientifically more interesting than Bible alone.
On the poster, this is described as a **multi-speaker, multi-domain dataset** —
a stronger contribution than any single-domain dataset.

---

## The three speakers and their domains

| Speaker code | Person | Voice | Domains | Est. raw audio |
|---|---|---|---|---|
| `bib` | Bible speaker (source: Padri Pierre MATABARO OFM) | Male, ~35yo | Bible narrative | ~67 min (ch01–ch04) |
| `dav` | David Namulabarha, 51, Ngweshe Nyangezi, South Kivu | Male, 51yo | Stories, family, numbers, calendar | ~24 min |
| `mrl` | Woman (murhula.com, permission: Marius NSHOMBO) | Female, ~28yo | Clock time expressions | ~10 min |

**Total raw audio across all speakers: ~101 minutes**
**Expected usable clips after segmentation: ~75–85 minutes**

---

## Domain breakdown and segmentation method

| Domain | Speaker | Files | Segmentation method | Text status |
|---|---|---|---|---|
| Bible (ch01–04) | bib | `shi_bible_bib_ch01.mp3` … `ch04.mp3` | Manual (Audacity) — see `manual_segmentation_guide.md` | Transcript exists ✓ |
| Short stories | dav | `shi_story_dav_001` … `005` | WhisperX (continuous narrative) | PDF — extract + match manually |
| Family vocabulary | dav | `shi_family_dav_001.aac` | Silence split (paused between items) | PDF — match after split |
| Numbers | dav | `shi_numbers_dav_001.aac` | Silence split (paused between each number) | PDF — match after split |
| Calendar / time names | dav | `shi_time_dav_001_nsaha_calendar.aac` | Silence split (paused between each day/month name) | PDF — match after split |
| Clock time expressions | mrl | `shi_time_mrl_07_53.mp3` … `10_56.mp3` | Already short clips — listen + write text | User fills in Mashi phrase |

---

## Section 1 — Speaker `bib` (Bible, chapters 01–04)

Follow the Audacity Label Track method in `manual_segmentation_guide.md`.
Target: ~300–400 clips, ~55–60 minutes usable audio.

Text is already in `Dataset_Mashi/Bible/transcripts/shi_bible_bib_ch01.txt` etc.
Match each exported Audacity clip to the corresponding verse.

Output goes to: `data/mashi_dataset/audio/` and `data/mashi_dataset/transcripts/`

---

## Section 2 — Speaker `dav`, Vocabulary Recordings (Numbers, Family, Calendar)

Your father recorded these item-by-item with a pause between each one.
The pause makes automatic silence-based splitting reliable.

### Step 1: Install dependencies (run once)
```
pip install pydub soundfile pandas
```
On Windows/WSL you also need ffmpeg:
```
sudo apt install ffmpeg
```

### Step 2: Run the silence splitter on each file

**Numbers** (he named each number and paused):
```
python scripts/04_split_on_silence.py \
  --input data/raw/Dataset_Mashi/Numbers/audio/shi_numbers_dav_001.aac \
  --domain numbers --speaker dav
```

**Family vocabulary** (he named each family member/term and paused):
```
python scripts/04_split_on_silence.py \
  --input data/raw/Dataset_Mashi/Family/audio/shi_family_dav_001.aac \
  --domain family --speaker dav
```

**Calendar — days and months** (he named each day/month and paused):
```
python scripts/04_split_on_silence.py \
  --input data/raw/Dataset_Mashi/Time/audio/shi_time_dav_001_nsaha_calendar.aac \
  --domain time --speaker dav
```

### Step 3: Listen and adjust if needed

The script uses these defaults:
- Silence threshold: –40 dBFS
- Minimum pause to split: 600ms
- Min clip: 1.5s, Max clip: 12s

If clips are not splitting correctly (too many merged or too many fragments):
```
# If splitting too aggressively (too many tiny clips):
python scripts/04_split_on_silence.py --input ... --min_silence_ms 800 --silence_thresh -45

# If not splitting enough (clips still too long):
python scripts/04_split_on_silence.py --input ... --min_silence_ms 400 --silence_thresh -35
```

### Step 4: Fill in the transcript files

After the script runs, it creates one .txt placeholder per clip in
`data/mashi_dataset/transcripts/`.

Open the PDF source document alongside each clip:
- Numbers: `Dataset_Mashi/Numbers/documents/shi_numbers_dav_source_text.pdf`
- Family: `Dataset_Mashi/Family/documents/shi_family_dav_source_text.pdf`
- Calendar: `Dataset_Mashi/Time/documents/shi_time_dav_source_text.pdf`

Listen to each clip → find the matching text in the PDF → paste it into the .txt file.
Delete the `#` comment lines. Leave only the Mashi text.

**Example** — `shi_numbers_dav_shi_numbers_dav_001_seg0001.txt`:
```
emu
```

**Example** — `shi_family_dav_shi_family_dav_001_seg0003.txt`:
```
Omu murhwe gwâwe akaburhwa balume bashanu.
```

---

## Section 3 — Speaker `dav`, Short Stories

Short stories are continuous narrative — your father told them as a story,
not item by item. These need sentence-level splitting like the Bible.

**Option A (faster): WhisperX on Colab**
Run notebook `01_forced_alignment_colab.ipynb` but change the input to the story files.
WhisperX will segment at sentence boundaries automatically.

**Option B (better quality): Manual in Audacity**
Open each story audio + the PDF text side by side.
Mark sentence boundaries using the Label Track (Ctrl+B at each pause).
This takes ~15–20 min per story (5 stories × 20 min = ~1h 40min).

Story files:
```
shi_story_dav_001_budiba_mulalwe_bona_mukage.aac    (~2 min)
shi_story_dav_002_ifunze_lya_mwali_kadege.aac       (~5 min)
shi_story_dav_003_kurhenga_kwobwami_bwe_bushi.aac   (~3 min)
shi_story_dav_004_murhondero_gw_abantu.aac          (~2 min)
shi_story_dav_005_obufumu_bwa_m_kagugu.aac          (~1 min)
```

Text source: `Dataset_Mashi/Short_stories/documents/shi_story_dav_source_text.pdf`
The PDF contains all 5 stories. Match each clip to its sentence in the PDF.

---

## Section 4 — Speaker `mrl`, Clock Time Expressions

Each file (`shi_time_mrl_07_53.mp3` etc.) is a clip about one specific time.
The filename tells you the time (07:53 = 7 hours 53 minutes).

These are 36–75 seconds each — they may contain the woman saying the same
time expression once, or a few times with slight variations.

### Step 1: Listen to each clip

Open each mp3 in any audio player (Windows Media Player, VLC, etc.)
and listen. You understand the language — write down what she is saying.

### Step 2: Decide: single clip or sub-split

If she says the time expression **once or twice** → keep the clip as-is.
Just write the Mashi text in the placeholder `.txt` file:
```
Dataset_Mashi/Time/transcripts/shi_time_mrl_07_53.txt
```

If she says it **3+ times with pauses** → run the silence splitter:
```
python scripts/04_split_on_silence.py \
  --input data/raw/Dataset_Mashi/Time/audio/shi_time_mrl_07_53.mp3 \
  --domain time --speaker mrl \
  --min_silence_ms 400
```
Then fill in the same Mashi text for each resulting sub-clip (they all say the same thing).

### Step 3: What to write in the text file

Write the Mashi phrase exactly as spoken. For example, for 07:53:
```
Nsaha mulingânye na eshaba na kasharhu z'edakika.
```
(or however it is said in Mashi — you know better than anyone.)

---

## Section 5 — Combining everything into one training dataset

After completing all sections above, you will have clips from all 3 speakers
in `data/mashi_dataset/audio/` and matching texts in `data/mashi_dataset/transcripts/`.

### Step 1: Build the unified metadata file
```
python scripts/05_build_combined_metadata.py
python scripts/10_make_train_eval_csv.py
```

This creates:
- `data/mashi_dataset/metadata_combined.csv` — with speaker and domain columns
- `data/mashi_dataset/speaker_references/ref_bib.wav` — reference voice for bib
- `data/mashi_dataset/speaker_references/ref_dav.wav` — reference voice for dav
- `data/mashi_dataset/speaker_references/ref_mrl.wav` — reference voice for mrl

### Step 2: Verify the numbers

Open `metadata_combined.csv` and check:
- At least ~300 clips from `bib` (Bible)
- At least ~50 clips from `dav` (all domains combined)
- At least ~12 clips from `mrl` (time expressions — may be few but they still help)

The model will use the reference wavs for voice conditioning during fine-tuning.

---

## Full timeline estimate

| Task | Method | Est. time |
|---|---|---|
| Bible ch01–04 manual segmentation (Audacity) | Manual | ~2.5 hours |
| Numbers + Family + Calendar silence split | Automatic script | ~15 min to run |
| Fill in text for Numbers + Family + Calendar | Manual (PDF match) | ~45 min |
| Short stories segmentation | WhisperX on Colab | ~30 min |
| Time expressions (mrl) — listen + write text | Manual | ~30 min |
| Run combine script + verify | Automatic | ~10 min |
| **Total** | | **~4.5–5 hours** |

After this, the training dataset is complete and ready for `notebooks/02_finetune_xtts_colab.ipynb`.

---

## Expected final dataset size

| Speaker | Domain | Est. clips | Est. minutes |
|---|---|---|---|
| bib | Bible | ~320 | ~52 |
| dav | Short stories | ~60 | ~11 |
| dav | Numbers | ~30 | ~4 |
| dav | Family | ~20 | ~3 |
| dav | Calendar | ~25 | ~4 |
| mrl | Time expressions | ~15 | ~8 |
| **Total** | | **~470 clips** | **~82 minutes** |

82 minutes from 3 speakers across 5 domains is a solid training set for a low-resource
TTS bootstrapping experiment. For context: many published low-resource TTS papers
use 1–3 hours. You are within that range with room to add more later.
