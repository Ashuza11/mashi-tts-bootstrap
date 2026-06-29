Manual segmentation output — Track B of the experiment.

Naming convention for clips:
  shi_bible_bib_{chapter}_{speaker}_seg{NNN}.wav
  e.g.  shi_bible_bib_ch01_bib_seg001.wav

Matching transcript (one sentence per file):
  shi_bible_bib_ch01_bib_seg001.txt

After completing manual segmentation, run:
  python scripts/03_build_metadata.py --track manual
to generate metadata.csv for TTS training.
