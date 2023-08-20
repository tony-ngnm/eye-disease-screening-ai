"""Splits a flat, per-class image folder (see `data/README.md` for the
expected layout after downloading the dataset) into train / validation /
test subsets, and builds the Keras `ImageDataGenerator` data loaders used
for training and evaluation.

python -m training.data_prep --input data/raw --output data/processed
"""

from __future__ import annotations

import argparse
from pathlib import Path

import splitfolders
from tensorflow.keras.preprocessing.image import (
    DirectoryIterator,
    ImageDataGenerator,
)

from training.utils import BATCH_SIZE, IMG_SIZE

# Train/validation/test proportions used in the original research.
SPLIT_RATIO: tuple[float, float, float] = (0.8, 0.1, 0.1)
SPLIT_SEED: int = 50


def split_dataset(
    input_dir: str | Path,
    output_dir: str | Path,
    ratio: tuple[float, float, float] = SPLIT_RATIO,
    seed: int = SPLIT_SEED,
) -> Path:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        splitfolders.ratio(
            str(input_dir), output=str(output_dir), seed=seed, ratio=ratio
        )
    else:
        print(f"'{output_dir}' already exists — skipping split.")
    return output_dir


def build_data_loaders(
    split_dir: str | Path,
    batch_size: int = BATCH_SIZE,
    img_size: tuple[int, int] = IMG_SIZE,
    seed: int = 42,
) -> tuple[DirectoryIterator, DirectoryIterator, DirectoryIterator]:
    split_dir = Path(split_dir)

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=0.5,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    eval_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_images = train_datagen.flow_from_directory(
        directory=str(split_dir / "train"),
        batch_size=batch_size,
        class_mode="categorical",
        target_size=img_size,
        shuffle=True,
        seed=seed,
    )
    val_images = eval_datagen.flow_from_directory(
        directory=str(split_dir / "val"),
        batch_size=batch_size,
        class_mode="categorical",
        target_size=img_size,
        shuffle=True,
        seed=seed,
    )
    test_images = eval_datagen.flow_from_directory(
        directory=str(split_dir / "test"),
        batch_size=batch_size,
        class_mode="categorical",
        target_size=img_size,
    )
    return train_images, val_images, test_images


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the raw class image dataset folder.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Destination path for the train/val/test split",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = split_dataset(args.input, args.output)
    print(f"Dataset split complete: {output_dir}")


if __name__ == "__main__":
    main()
