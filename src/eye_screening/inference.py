"""Model loading and image classification for the eye-screening app."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(os.environ.get("EYE_MODEL_PATH", PROJECT_ROOT / "models" / "DenseNet201.h5"))
ASSETS_DIR = Path(os.environ.get("EYE_ASSETS_DIR", PROJECT_ROOT / "docs" / "assets" / "conditions"))

IMG_SIZE: tuple[int, int] = (180, 180)

CLASS_NAMES: tuple[str, ...] = tuple(
    sorted(
        [
            "Conjunctivitis_Dry Eye Syndrome_Uveitis",
            "Cataracts_Glaucoma",
            "Normal",
            "Pterygium",
            "Subconjunctival hemorrhage",
        ]
    )
)

# Maps a raw model class name to the illustrative image filename used on
# its condition card.
CLASS_IMAGE_FILENAMES: dict[str, str] = {
    "Conjunctivitis_Dry Eye Syndrome_Uveitis": "conjunctivitis_dry_eye.jpg",
    "Cataracts_Glaucoma": "cataract.jpg",
    "Pterygium": "pterygium.jpg",
    "Subconjunctival hemorrhage": "subconjunctival_hemorrhage.jpg",
}


@st.cache_resource
def load_model(model_path: str | Path = MODEL_PATH) -> tf.keras.Model:
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"No model checkpoint found at '{model_path}'. "
            "See models/README.md for download instructions, or set the "
            "EYE_MODEL_PATH environment variable to a custom location."
        )
    return tf.keras.models.load_model(str(model_path))


@st.cache_resource
def load_condition_images() -> dict[str, Image.Image]:
    filename_by_condition = {
        "conjunctivitis": "conjunctivitis.jpg",
        "dry_eye": "dry_eye.jpg",
        "corneal_ulcer": "corneal_ulcer.jpg",
        "cataract": "cataract.jpg",
        "subconjunctival_hemorrhage": "subconjunctival_hemorrhage.jpg",
        "pterygium": "pterygium.jpg",
    }
    images: dict[str, Image.Image] = {}
    for condition_id, filename in filename_by_condition.items():
        path = ASSETS_DIR / filename
        if path.exists():
            images[condition_id] = Image.open(path)
    return images


def preprocess_image(image: Image.Image, target_size: tuple[int, int] = IMG_SIZE) -> np.ndarray:
    """Convert a PIL image into the model's expected input tensor.

    Args:
        image: The input eye photo.
        target_size: Target (width, height) for resizing.

    Returns:
        A `(1, H, W, 3)` float32 array scaled to [0, 1].
    """
    image = image.convert("RGB").resize(target_size)
    array = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(array, axis=0)


def classify_image(
    image: Image.Image, model: tf.keras.Model
) -> tuple[str, np.ndarray]:
    input_tensor = preprocess_image(image)
    predictions = model.predict(input_tensor)
    predicted_class = CLASS_NAMES[int(np.argmax(predictions))]
    return predicted_class, predictions
