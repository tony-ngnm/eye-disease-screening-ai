# Dataset

This project's training data (3,076 labeled eye images across 5 classes:
healthy, red/inflamed eye, cataract, subconjunctival hemorrhage, and
pterygium).

## Download

1. Request/download access to the dataset archive from Google Drive:
   **https://drive.google.com/drive/folders/1ucOaISkRkWNk4fNpg33RMbNEuVdUbIAH?usp=sharing**
2. Unzip it so you end up with one subfolder per class:

## Split into train / validation / test

```bash
python -m training.data_prep --input data/raw --output data/processed
```

## Note

Images were sourced from peer-reviewed publications, ophthalmology
reference texts, and major clinical portals (American Academy of
Ophthalmology, American Optometric Association, Kanski's *Clinical
Ophthalmology*), then **label-verified by a licensed ophthalmologist**
(Ths. Bs. Trần Thủy Trinh, Thu Duc City Hospital) prior to training. See
`docs/report.md` for full citations.