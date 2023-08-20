"""
    python -m training.train \\
        --data-dir data/processed \\
        --backbone densenet201 \\
        --epochs 20 \\
        --output-dir models
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tensorflow.keras.callbacks import ModelCheckpoint

from training.data_prep import build_data_loaders
from training.model import build_model
from training.utils import (
    DEFAULT_EPOCHS,
    DEFAULT_SEED,
    SUPPORTED_BACKBONES,
    plot_learning_curve,
    seed_everything,
)


def train(
    data_dir: str | Path,
    backbone: str,
    epochs: int = DEFAULT_EPOCHS,
    output_dir: str | Path = "models",
    plots_dir: str | Path = "docs/assets",
    seed: int = DEFAULT_SEED,
) -> Path:

    seed_everything(seed)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_images, val_images, _ = build_data_loaders(data_dir)
    num_classes = train_images.num_classes

    model = build_model(backbone, num_classes)

    checkpoint_path = output_dir / f"{backbone.lower()}.h5"
    checkpoint_callback = ModelCheckpoint(
        filepath=str(checkpoint_path),
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
    )

    history = model.fit(
        train_images,
        epochs=epochs,
        validation_data=val_images,
        callbacks=[checkpoint_callback],
        verbose=1,
    )

    plot_learning_curve(history, "accuracy", backbone, plots_dir, ylim=(0, 1))
    plot_learning_curve(history, "loss", backbone, plots_dir, ylim=(0, 1))

    print(f"Best checkpoint saved to: {checkpoint_path}")
    return checkpoint_path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Path to the split dataset (output of training/data_prep.py).",
    )
    parser.add_argument(
        "--backbone",
        required=True,
        choices=SUPPORTED_BACKBONES,
        help="Backbone to fine-tune.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=DEFAULT_EPOCHS,
        help=f"Number of training epochs (default: {DEFAULT_EPOCHS}).",
    )
    parser.add_argument(
        "--output-dir",
        default="models",
        help="Dir to save the best model checkpoint.",
    )
    parser.add_argument(
        "--plots-dir",
        default="docs/assets",
        help="Dir to save learning-curve plots.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Random seed (default: {DEFAULT_SEED}).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    train(
        data_dir=args.data_dir,
        backbone=args.backbone,
        epochs=args.epochs,
        output_dir=args.output_dir,
        plots_dir=args.plots_dir,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
