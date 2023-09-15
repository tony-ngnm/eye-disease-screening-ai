## Option A — Retrain it yourself

```bash
python -m training.data_prep --input data/raw --output data/processed
python -m training.train --data-dir data/processed --backbone densenet201 --epochs 20
```
## Option B — Download the pretrained checkpoint

URL to the DenseNet101.h5 pretrained model: **https://drive.google.com/file/d/1z67L1ChF5vQxtFJPqhhT7LlfD4hNVoe7/view?usp=sharing**
