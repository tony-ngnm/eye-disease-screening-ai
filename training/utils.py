from __future__ import annotations

import os
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

IMG_SIZE: tuple[int, int] = (180, 180)
IMG_SHAPE: tuple[int, int, int] = (*IMG_SIZE, 3)
BATCH_SIZE: int = 64
DEFAULT_EPOCHS: int = 20
DEFAULT_SEED: int = 100

# Backbones evaluated in the original research (see docs/report.md, section
SUPPORTED_BACKBONES: tuple[str, ...] = (
    "vgg16",
    "vgg19",
    "densenet201",
    "xception",
    "resnet152",
)


def seed_everything(seed: int = DEFAULT_SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    os.environ["TF_CUDNN_DETERMINISM"] = "1"
    os.environ["PYTHONHASHSEED"] = str(seed)


def plot_learning_curve(
    history: tf.keras.callbacks.History,
    key: str,
    model_name: str,
    output_dir: str | Path,
    ylim: tuple[float, float] = (0.0, 1.01),
) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(history.history[key], label="train")
    plt.plot(history.history[f"val_{key}"], label="val")
    plt.title(model_name)
    plt.ylabel(key.title())
    plt.xlabel("Epoch")
    plt.ylim(ylim)
    plt.legend(loc="best")

    out_path = output_dir / f"{model_name.lower()}_{key}.png"
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return out_path
