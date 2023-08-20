from __future__ import annotations

from tensorflow.keras import Model, Sequential
from tensorflow.keras.applications import (
    VGG16,
    VGG19,
    DenseNet201,
    ResNet152,
    Xception,
)
from tensorflow.keras.layers import Dense, Flatten

from training.utils import IMG_SHAPE, SUPPORTED_BACKBONES

# Maps a CLI-friendly backbone name to its Keras Applications constructor.
_BACKBONE_CONSTRUCTORS = {
    "vgg16": VGG16,
    "vgg19": VGG19,
    "densenet201": DenseNet201,
    "xception": Xception,
    "resnet152": ResNet152,
}


def build_model(backbone_name: str, num_classes: int) -> Model:
    key = backbone_name.strip().lower()
    if key not in _BACKBONE_CONSTRUCTORS:
        raise ValueError(
            f"Unsupported backbone '{backbone_name}'. "
            f"Choose one of: {', '.join(SUPPORTED_BACKBONES)}"
        )

    backbone_fn = _BACKBONE_CONSTRUCTORS[key]

    base_model = backbone_fn(
        weights="imagenet", include_top=False, input_shape=IMG_SHAPE
    )
    base_model.trainable = False

    model = Sequential(
        [
            base_model,
            Flatten(),
            Dense(1024, activation="relu"),
            Dense(512, activation="relu"),
            Dense(256, activation="relu"),
            Dense(num_classes, activation="softmax"),
        ],
        name=f"{key}_eye_screening_classifier",
    )

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"],
    )
    return model
