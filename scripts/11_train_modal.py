"""
Fine-tune XTTS v2 on the Mashi dataset using a Modal A100 GPU.

One-time setup (local machine):
  pip install modal
  modal setup                                   # opens browser to authenticate
  modal volume create mashi-dataset
  modal volume put mashi-dataset data/mashi_dataset mashi_dataset

Train (detached — survives closing the terminal):
  modal run --detach scripts/11_train_modal.py

Download the generated samples + checkpoint when done:
  modal volume get mashi-models samples ./results/samples
  modal volume get mashi-models checkpoints ./models/checkpoints   # optional, large

The dataset volume is read at /data/mashi_dataset; checkpoints and samples
persist in the mashi-models volume across runs (the ~2 GB XTTS base download
is cached there too, so only the first run pays it).
"""

import modal

app = modal.App("mashi-tts-xtts")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install("torch==2.7.1", "torchaudio==2.7.1")   # coqui-tts does not pull torch itself
    .pip_install("coqui-tts==0.27.5", "transformers<5") # transformers 5.x removed APIs coqui needs
    .env({
        "TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD": "1",   # TTS checkpoints predate torch 2.6 safe-loading
        "COQUI_TOS_AGREED": "1",
    })
)

data_vol  = modal.Volume.from_name("mashi-dataset", create_if_missing=True)
model_vol = modal.Volume.from_name("mashi-models",  create_if_missing=True)

DATA_DIR   = "/data/mashi_dataset"
OUT_DIR    = "/models/checkpoints"
SAMPLE_DIR = "/models/samples"
LANGUAGE   = "es"   # phonetic proxy — XTTS v2 has no Bantu language


@app.function(
    image=image,
    gpu="A100",
    cpu=8.0,
    memory=16384,
    timeout=2 * 3600,
    volumes={"/data": data_vol, "/models": model_vol},
)
def train(num_epochs: int = 10, batch_size: int = 8, grad_acumm: int = 2):
    """Fine-tune the XTTS GPT on the Mashi clips. Returns paths on the volume."""
    import os
    from TTS.demos.xtts_ft_demo.utils.gpt_train import train_gpt

    assert os.path.exists(f"{DATA_DIR}/metadata_train.csv"), \
        "dataset not found — run: modal volume put mashi-dataset data/mashi_dataset mashi_dataset"
    for s_ in ("bib", "dav", "mrl"):
        assert os.path.exists(f"{DATA_DIR}/speaker_references/ref_{s_}.wav"), \
            f"missing speaker reference ref_{s_}.wav — sample generation would fail after paid training"

    config_path, original_ckpt, vocab_file, exp_path, speaker_ref = train_gpt(
        language=LANGUAGE,
        num_epochs=num_epochs,
        batch_size=batch_size,       # A100 has headroom; effective batch = 8 x 2 = 16
        grad_acumm=grad_acumm,
        train_csv=f"{DATA_DIR}/metadata_train.csv",
        eval_csv=f"{DATA_DIR}/metadata_eval.csv",
        output_path=OUT_DIR,
        max_audio_length=255995,     # 11.6 s at 22050 Hz — longest clip is 11.3 s
    )

    ft_checkpoint = os.path.join(exp_path, "best_model.pth")
    assert os.path.exists(ft_checkpoint), f"training finished but {ft_checkpoint} missing"
    model_vol.commit()
    print(f"config : {config_path}")
    print(f"ckpt   : {ft_checkpoint}")
    return config_path, ft_checkpoint, vocab_file


@app.function(
    image=image,
    gpu="A100",
    cpu=4.0,
    timeout=1800,
    volumes={"/data": data_vol, "/models": model_vol},
)
def generate_samples(config_path: str, ft_checkpoint: str, vocab_file: str):
    """Synthesize per-speaker test sentences with the fine-tuned model."""
    import os
    import torch
    import torchaudio
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts

    config = XttsConfig()
    config.load_json(config_path)
    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_path=ft_checkpoint,
                          vocab_path=vocab_file, use_deepspeed=False)
    model.cuda()

    tests = {
        "bib": ["Nnâmahanga alema amalunga n'igulu.",
                "Obulangashane bwanaciba."],
        "dav": ["Mbwira ngahi abantu barhengaga?",
                "Muguma, babirhi, basharhu, bani, barhanu."],
        "mrl": ["9:05",
                "16:35"],
    }

    os.makedirs(SAMPLE_DIR, exist_ok=True)
    for spk, sentences in tests.items():
        ref = f"{DATA_DIR}/speaker_references/ref_{spk}.wav"
        gpt_cond, speaker_emb = model.get_conditioning_latents(audio_path=[ref])
        for i, text in enumerate(sentences):
            out = model.inference(text, LANGUAGE, gpt_cond, speaker_emb, temperature=0.7)
            path = f"{SAMPLE_DIR}/{spk}_sample_{i+1:02d}.wav"
            torchaudio.save(path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
            print("saved", path)

    model_vol.commit()


@app.local_entrypoint()
def main(epochs: int = 10):
    config_path, ft_checkpoint, vocab_file = train.remote(num_epochs=epochs)
    generate_samples.remote(config_path, ft_checkpoint, vocab_file)
    print("\nDone. Download the samples with:")
    print("  modal volume get mashi-models samples ./results/samples")
