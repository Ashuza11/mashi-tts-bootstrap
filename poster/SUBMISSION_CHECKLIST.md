# DLI 2026 RIAD poster — submission checklist

> **⚠️ Deadline: 6 July 2026 (TODAY).** General, publication and dataset
> posters all close today. Contact daphne@deeplearningindaba.com or
> riad@deeplearningindaba.com for clarifications/extensions.

## Format requirements (from the call)

| Requirement | Status |
|---|---|
| Size **A0** (84.1 × 118.8 cm / 33.11 × 46.81 in) | ✅ `dli2026_riad_poster.tex` is `a0paper` |
| Orientation **PORTRAIT** | ✅ set in documentclass |
| Format **PDF** | compile on Overleaf → download PDF |
| Use the official LaTeX template (Drive folder in the call) | ⬜ optional — if reviewers insist, copy blocks 1–8 into it; structure maps 1:1 |
| Unique poster ID inside the poster | ⬜ assigned **after** light review — placeholder box is in the title block |

## Submission steps

1. ⬜ Compile the poster: upload `dli2026_riad_poster.tex` to [Overleaf](https://overleaf.com), compiler **pdfLaTeX** → PDF.
2. ⬜ Fill the **default form** — upload the **poster PDF, not a paper**.
3. ⬜ Fill the **poster submission form** (both forms = complete submission).
4. ⬜ Submit as a **General poster** (dataset posters use pre-assigned IDs; this project's dataset is not separately accepted, so general track applies — likely categorized as a dataset+method showcase).
5. ⬜ After review: insert the assigned unique ID in the title-block placeholder, recompile, and check whether a re-upload is requested.
6. ⬜ Printing is done **for you** by the organizers — no need to print.
7. ⬜ Prepare the short **video pitch** and be ready for the live demo slot (RIAD combines posters + video pitches + demos). A 60–90 s pitch: problem (3M speakers, zero tools) → dataset (723 clips/67 min) → result (play one sample).

## Placeholders to replace before/after the training run

All estimates are marked in **red with a dagger (†)** via `\EST{...}`; hard
placeholders are boxed via `\TODO{...}`:

| Placeholder | Where to get it |
|---|---|
| Poster ID | emailed after light review |
| Train/eval loss curve | Modal run logs → `results/loss_curve.png` |
| MOS naturalness / intelligibility / similarity | native-speaker listening test on generated samples (`results/samples/`) |
| N raters, K utterances | your evaluation design |
| Fine-tune wall-clock + cost | Modal dashboard after `modal run --detach scripts/11_train_modal.py` |
| QR code | link to samples (Drive/HF gated page) — `\usepackage{qrcode}` + `\qrcode{URL}` |
| Mel-spectrograms | ground truth vs. synthesized, e.g. via `librosa.display.specshow` |

When real numbers are in, redefine `\newcommand{\EST}[1]{#1}` to drop the
red marking, and delete the "estimated" note in the Results block title.

## Where the estimates come from (published comparables)

- **BibleTTS** (Interspeech 2022, [arXiv:2207.03546](https://arxiv.org/abs/2207.03546)) — VITS on 33–87 h per African language: in-domain MOS 2.79–4.34, out-of-domain 2.34–3.87. With 1.1 h we should expect the low end or below → estimate MOS 2.5–3.5 in-domain.
- **BnTTS** (NAACL Findings 2025, [arXiv:2502.05729](https://arxiv.org/abs/2502.05729)) — XTTS-based Bangla, 3 850 h pre-training + 20 min/speaker few-shot: SMOS 4.62, CER 0.034. Upper bound of what XTTS adaptation achieves *with* large target-language pre-training, which we don't have.
- **Align2Speak** ([arXiv:2509.21718](https://arxiv.org/abs/2509.21718)) — 30 min of an unseen language already cuts CER from 33 % → 3.9 % (Portuguese); supports the claim that ~1 h can reach *intelligible* speech in an unseen language.
- **ZMM-TTS language adaptation** (Interspeech 2024, [arXiv:2406.08911](https://arxiv.org/abs/2406.08911)) — phonetic similarity between pre-training and target language is a key adaptation factor: the stated rationale for the Spanish vowel/CV proxy.

No Mashi ASR exists, so automatic CER is impossible — the poster commits to
human evaluation only (naturalness MOS, word-level transcription
intelligibility, speaker-similarity MOS). This is the honest, defensible
evaluation story for a zero-resource language.
