"""
python -m training.evaluate --model models/densenet201.h5 --data-dir data/processed
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tensorflow as tf

from training.utils import BATCH_SIZE, IMG_SIZE


def evaluate(model_path: str | Path, data_dir: str | Path) -> tuple[float, float]:
    model = tf.keras.models.load_model(str(model_path))

    test_path = Path(data_dir) / "test"
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        str(test_path),
        labels="inferred",
        label_mode="categorical",
        color_mode="rgb",
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE,
        shuffle=False,
    )

    test_loss, test_accuracy = model.evaluate(test_dataset)
    print(f"Test loss: {test_loss:.4f} | Test accuracy: {test_accuracy:.4%}")
    return test_loss, test_accuracy


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Saved .h5 model.")
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Path to the split dataset.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    evaluate(args.model, args.data_dir)


if __name__ == "__main__":
    main()
