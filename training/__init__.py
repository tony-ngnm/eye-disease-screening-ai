"""Training pipeline for the eye-disease screening classifier.
- `utils`: seeding, config constants, learning-curve plotting.
- `data_prep`: dataset splitting and augmented data loaders.
- `model`: transfer-learning model factory (VGG16/19, DenseNet201,
  Xception, ResNet152).
- `train`: CLI entrypoint for training a single backbone.
- `evaluate`: CLI entrypoint for evaluating a saved checkpoint.
"""
