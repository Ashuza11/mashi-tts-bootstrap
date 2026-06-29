# Manual Segmentation Guide — Track B

## Target
Segment chapters ch01–ch04 into verse-level WAV clips (~4–10 seconds each).
Goal: ~65 minutes of clean audio = ~600–700 clips.

## Tool: Audacity (free, download at audacityteam.org)

## Step-by-step for each chapter

### 1. Open the files
- File → Open → `Dataset_Mashi/Bible/audio/shi_bible_bib_ch01.mp3`
- Open the transcript: `Dataset_Mashi/Bible/transcripts/shi_bible_bib_ch01.txt`
  (keep it open in any text editor beside Audacity)

### 2. Add a Label Track
- Tracks → Add New → Label Track
- Now you can mark boundaries without touching the audio.

### 3. Mark each verse boundary
- Listen to the audio. Each verse ends with a short pause.
- When you hear the pause after a verse: press **Ctrl+B** (or Cmd+B on Mac)
  This places a label at the playhead position.
- Type the label: verse number, e.g. `v001`, `v002` ...
- Continue through the whole chapter.

### 4. Export all clips at once
- File → Export → Export Multiple
- Choose: Split files based on **Labels**
- Format: WAV (16-bit PCM)
- Output folder: `data/manual_segments/audio/`
- Filename template: `shi_bible_bib_ch01_bib_seg[NUMBER]`

### 5. Create the transcript files
For each exported clip, create a matching .txt file in `data/manual_segments/transcripts/`
with the EXACT text of that verse from the transcript.

Example:
  audio file :  shi_bible_bib_ch01_bib_seg001.wav
  text file  :  shi_bible_bib_ch01_bib_seg001.txt
  text content: Aha murhondêro Nnâmahanga alema amalunga n'igulu.

## Chapter breakdown and time estimate

| Chapter | Approx duration | Est. verses | Est. work time |
|---------|----------------|-------------|----------------|
| ch01    | 18 min         | 31          | 40 min         |
| ch02    | 15 min         | 25          | 35 min         |
| ch03    | 17 min         | 24          | 35 min         |
| ch04    | 17 min         | 26          | 35 min         |
| **Total** | **67 min** | **~106**    | **~2.5 hours** |

## Quality rules for each clip
- Minimum length: 2 seconds
- Maximum length: 12 seconds
- No background music, no interruptions
- If a verse is too long (>12s), split it at a natural pause mid-verse
  and label the text accordingly
- If a verse is very short (<2s), merge it with the next one

## After finishing all 4 chapters
Run: python scripts/03_build_metadata.py --track manual
This creates data/manual_segments/metadata.csv for training.
