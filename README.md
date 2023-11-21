# Fine-tune any LLM in minutes (ft. LLaMA, CodeLlama, Mistral)

### Tired of prompt engineering? You've come to the right place.

This no-frills guide will take you from a dataset to using a fine-tuned LLM model for inference in the matter of minutes. The heavy lifting is done by the [`axolotl` framework](https://github.com/OpenAccess-AI-Collective/axolotl).

<details>
  <summary>We use all the recommended, start-of-the-art optimizations for fast results.</summary>
  
<br>
  
- *Deepspeed ZeRO-3* to efficiently shard the base model and training state across multiple GPUs [more info](https://www.deepspeed.ai/2021/03/07/zero3-offload.html)
- *Parameter-efficient fine-tuning* via LoRa adapters for faster convergence
- *Gradient checkpointing* to reduce VRAM footprint, fit larger batches and get higher training throughput
</details>


Using Modal for fine-tuning means you never have to worry about infrastructure headaches like building images and provisioning GPUs. If a training script runs on Modal, it's reproducible and scalable enough to ship to production right away.

### Just one local dependency - a Modal account

1. Create a [Modal](https://modal.com/) account.
2. Install `modal` in your current Python virtual environment (`pip install modal`)
3. Set up a Modal token in your environment (`python3 -m modal setup`)
4. You need to have a [secret](https://modal.com/secrets) named `huggingface` in your workspace. Populate both `HUGGING_FACE_HUB_TOKEN` and `HUGGINGFACE_TOKEN` with the same key from HuggingFace (settings under API tokens).
5. For some LLaMA models, you need to go to the [Hugging Face page](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf) and agree to the terms and conditions for access (granted instantly).

### Code overview

All the logic lies in `train.py`. Three business Modal functions run in the cloud:

* `launch` prepares a new folder in the `/runs` volume with the training config and data for a new training job. It also ensures the base model is downloaded from HuggingFace.
* `train` takes a prepared folder and performs the training job using the config and data.
* `Inference.completion` can spawn a [vLLM](https://modal.com/docs/examples/vllm_inference#fast-inference-with-vllm-mistral-7b) inference container for any pre-trained or fine-tuned model from a previous training job.

The rest of the code are helpers for _calling_ these three functions. There are two main ways to train:

* Use the GUI to familiarize with the system (recommended for new fine-tuners!)
* Use CLI commands (recommended for power users)

### Using the GUI

Deploy the training backend with three business functions (`launch`, `train`, `completion` in `__init__.py`). Then run the Gradio GUI.

```bash
modal deploy src
modal run src.gui
```

The `*.modal.host` link from the latter will take you to the Gradio GUI. There will be three tabs: launch training runs, test out trained models and explore the files on the volume.


**What is the difference between `deploy` and `run`?**

- `modal deploy`: a deployed app remains ready on the cloud for invocations anywhere, anytime. This means your training jobs continue without your laptop being connected.
- `modal run`: am ephemeral app shuts down once your local command exits. Your GUI (ephemeral app) does not waste resources when your terminal disconnects.


**How do I change the GPU configuration?**

The training GPU configuration can be specified as environment variables. Keep in mind that this would affect all runs spawned from the GUI, since it is a backend parameter.

```bash
N_GPUS=2 GPU_MEM=80 modal deploy src
```

### Using the CLI

**Training**

A simple training job can be started with

```bash
modal run --detach src.train --cfg config.yml
```

_`--detach` lets the app continue running even if your client disconnects_.

The script reads two local files: `config.yml` and `my_data.jsonl`. The contents passed as arguments to the remote `launch` function, which will write them to the `/runs` volume. Next, `train` will read the config and data from the new folder for reproducible training runs.

When you make local changes to either `config.yml` or `my_data.jsonl`, they will be used for your next training run.

The default configuration fine-tunes CodeLlama Instruct 7B to understand Modal documentation for one epoch (takes a few minutes) as a proof of concept only. It uses DeepSpeed ZeRO-3 to shard the model state. To achieve better results, you would need to use more data and train for more epochs.

**Inference**

To try a model from a completed run, you can select a folder via `modal volume ls examples-runs-vol`, and then specify the training folder for inference:

```bash
modal run -q src.inference --run-folder /runs/axo-2023-11-24-17-26-66e8
```
