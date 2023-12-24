# Recognizing Functional Signs in Ocular Diseases via Transfer Learning (English-translated)

**Ho Chi Minh City Department of Education and Training — Science & Engineering Fair for High School Students, 2023–2024**
**Category:** Software Systems · **Project code:** 21_1033_09 (Le Hong Phong High School for The Gifted, HCMC)
**Research period:** From Feb 2023
---

## Abstract

Vietnam is estimated to have around 2 million people living with blindness or serious eye disease, a number worsened by recurring conjunctivitis (pink eye) outbreaks. This project set out to build an AI-assisted screening tool that helps people recognize functional signs of common, potentially dangerous eye conditions from home.

The team collected a dataset of 3,076 images spanning a healthy eye and four conditions — red/inflamed eye, cataract, subconjunctival hemorrhage, and pterygium — then fine-tuned five ImageNet-pretrained CNN backbones (VGG16, VGG19, DenseNet201, ResNet152, Xception) on Google Colaboratory. **DenseNet201** achieved the best validation accuracy (94.12%) and was selected for deployment. A set of clinically-informed multiple-choice questions was then layered on top of the image classifier, and the combined system was deployed as a web application.

The resulting tool can currently suggest six conditions — conjunctivitis, dry eye, corneal ulcer, cataract, subconjunctival hemorrhage, and pterygium — alongside a healthy-eye baseline, through an interface designed to be accessible to non-specialist users.

---

## 1. Background

### 1.1 International Context

AI-assisted eye-disease recognition has been an active research and product area internationally, with tools such as ScanMyEye and the Cradle White Eye Detector already in use. According to the WIPS Global patent database, the first AI application for eye-disease diagnosis dates to 2010, in University of Pittsburgh patent US8831304B2, which used machine-learning algorithms to automatically identify blood vessels in 3D OCT imagery for retinal analysis and early detection of glaucoma, diabetic retinopathy, and other conditions. Google's DeepMind has separately developed a deep-learning system for detecting glaucoma, age-related macular degeneration, and diabetic retinopathy, trained on thousands of 3D retinal scans provided by Moorfields Eye Hospital.

A common limitation across these systems: most are single-condition detectors built for specialist clinical use, and are not designed to be accessible to the general public.

### 1.2 Domestic (Vietnam) Context

Vietnamese medical institutions and researchers have increasingly explored AI-assisted diagnosis, including a 2022 study on staging diabetic retinopathy from standard fundus photography (Trần Thị Hải Linh & Vũ Tuấn Anh, *Vietnam Medical Journal*, Issue 01/2022), and the EyeDr glaucoma-screening system developed by Dr. Phạm Thị Thủy Tiên and colleagues at Ho Chi Minh City Eye Hospital (accepted by the HCMC Department of Science and Technology, October 2022), which estimates cup-to-disc ratio and applies the ISNT rule for community glaucoma screening.

As with the international examples, these tools are generally built for specialist use and are not designed for direct use by the general public.

---

## 2. Introduction

### 2.1 Motivation

The World Health Organization estimates roughly 2 billion people worldwide live with a vision-impairing condition, of which around 1 billion involve preventable or not-yet-addressed deterioration. Many people underestimate early symptoms or lack easy, affordable access to specialist eye care — a gap compounded by the cost of medical equipment and specialist consultations. This project aims to help people recognize dangerous warning signs earlier, reducing the risk of serious downstream complications.

### 2.2 Research Objective

To build a convenient, fast, and reasonably accurate at-home screening aid for common eye conditions — one that can, in specific situations, reduce reliance on specialized medical equipment — and in doing so provide early warnings and concrete at-home guidance.

### 2.3 Research Question

How can machine learning models be applied to help recognize the signs of dangerous eye conditions?

### 2.4 Hypothesis

Common eye conditions tend to present with functional symptoms characteristic of each condition. Combining an image-recognition model with a symptom-based questionnaire, both grounded in curated clinical data, should let the system distinguish between conditions more reliably than either signal alone.

### 2.5 Objectives

- Design software capable of distinguishing six common, potentially serious eye conditions using a combination of an image-recognition model and a symptom questionnaire.
- Package the tool as an accessible, easy-to-use web application to reach as many users as possible.

### 2.6 Scope

The intended audience is the **general public** — not medical specialists.

---

## 3. Theoretical Background

### 3.1 Convolutional Neural Networks (CNN)

CNNs are among the most widely used image-classification models for building high-accuracy intelligent systems. A CNN is a stack of convolutional layers using activation functions such as ReLU and Tanh; each layer produces increasingly abstract representations for subsequent layers in the network.

### 3.2 Transfer Learning

Transfer learning improves the performance of neural networks on small datasets by reusing knowledge from models pretrained on large datasets. VGG16, VGG19, DenseNet201, ResNet152, and Xception are common pretrained CNN backbones used for this purpose.

The team froze the convolutional base of each pretrained backbone and trained a new 4-layer dense classification head on top, specifically for eye-condition recognition:

- `Dense(1024, activation='relu')`
- `Dense(512, activation='relu')`
- `Dense(256, activation='relu')`
- `Dense(num_classes, activation='softmax')`

### 3.3 Target eye Conditions

| Condition | Summary |
|---|---|
| Conjunctivitis | Inflammation of the clear membrane covering the sclera (the white of the eye). |
| Dry eye | An imbalance between tear production and tear-film evaporation. |
| Corneal ulcer | Corneal abrasion combined with infection; the cornea is the transparent tissue at the front of the eye that light passes through first. |
| Cataract | Clouding of the lens that blocks light from reaching the retina, progressively reducing vision and potentially leading to blindness. |
| Subconjunctival hemorrhage | Rupture of one or more small blood vessels beneath the sclera. |
| Pterygium | Growth of a thin, fleshy layer of conjunctival tissue over part of the sclera, at one or both corners of the eye. |

---

## 4. Methodology

### 4.1 Dataset Collection Standards

- Images show a single eye and its immediate surrounding area.
- Sourced from scientific papers, medical handbooks, research institutes, universities, and major clinical portals (AAO, AOA, and others).
- At least 500 images per class.
- Standardized to 180×180 pixels.

### 4.2 Data Split & Class Sizes

3,076 labeled images (labels verified with support from Ths. Bs. Trần Thủy Trinh) were split 80% / 10% / 10% into train / validation / test **per class**:

| Class | Total | Train | Val | Test |
|---|---|---|---|---|
| Healthy eye | 661 | 528 | 66 | 67 |
| Red-eye symptoms | 666 | 532 | 66 | 68 |
| Cataract | 612 | 489 | 61 | 62 |
| Subconjunctival hemorrhage | 630 | 506 | 63 | 61 |
| Pterygium | 504 | 403 | 50 | 51 |

### 4.3 Data Augmentation

Standard geometric augmentations (translation, rotation, zoom) were applied to expand the effective training set. Photometric transforms (brightness, contrast, sharpness) were deliberately **excluded**, since they can distort clinically relevant visual features of the eye.

### 4.4 Model Selection

All five backbones were trained for 20 epochs under identical conditions and compared on validation accuracy/loss:

| Model | Best epoch | Validation accuracy | Validation loss | Avg. time/epoch |
|---|---|---|---|---|
| VGG16 | 19 | 88.89% | 0.4663 | 76s |
| VGG19 | 19 | 86.27% | 0.5479 | 81s |
| **DenseNet201** | **10** | **94.12%** | **0.19** | 82s |
| Xception | 20 | 87.25% | 0.4733 | 96s |
| ResNet152 | 20 | 49.35% | 1.2645 | 89s |

DenseNet201 was selected for having both the highest validation accuracy and the lowest validation loss. Its accuracy and loss curves stabilize after epoch 2, with validation accuracy consistently above ~90% and validation loss settling in the 0.19–0.29 range — indicating reasonable generalization given the dataset size (see `docs/assets/accuracy_curve.png` and `docs/assets/loss_curve.png`).

### 4.5 Questionnaire Design

Symptom questions were authored with guidance from Ths. Bs. Trần Thủy Trinh and cross-referenced against Ho Chi Minh City Eye Hospital's internal ophthalmology practice handbook (*Cẩm Nang Thực Hành Nhãn Khoa*, 2014) — not redistributed in this repository. When a user finishes the relevant questionnaire, the app returns a suggested condition and severity tier.

### 4.6 System Workflow

```
Image capture/upload → CNN classification → Condition-specific questionnaire
→ Combined suggestion + condition info + at-home guidance
```

1. User uploads or captures a close-up eye photo.
2. The image is cropped/preprocessed and classified by the DenseNet201 model.
3. Based on the predicted class, the user answers a short symptom questionnaire.
4. The app combines both signals into a severity-aware suggestion, background information about the condition, and at-home care / red-flag guidance.

---

## 5. Discussion

| Problem | Challenge | Solution |
|---|---|---|
| Limited dataset size (some classes as low as ~500 images) | Class imbalance can hurt training stability and accuracy | Kept per-class counts in a consistent 500–650 range; manually filtered out low-quality/duplicate images |
| Streamlit's rerun-on-every-interaction model | The deployed web app felt slow, since every UI interaction reruns the whole script | Used `st.cache_resource` / caching strategies to reduce redundant reruns |

---

## 6. Conclusions & Future Work

### What was achieved

- A working screening tool that recognizes a healthy eye and six eye conditions: conjunctivitis, dry eye, corneal ulcer, cataract, subconjunctival hemorrhage, and pterygium.

### What's notable about the project

- Delivered as a free web app with a simple, accessible interface.
- Positioned as a potential early-detection aid in place of specialized equipment or an initial clinical opinion, in specific at-home scenarios.
- Can support recognition of functional signs for six eye conditions from a smartphone photo.
---

## References

The full citation list (17 references spanning international patents, WHO reports, Vietnamese hospital publications, and ophthalmology textbooks) is preserved in the original submitted PDF report. Key sources include the WHO's *World Report on Vision* (2021), Ho Chi Minh City Eye Hospital's practice handbook, and clinical information pages from Bệnh Viện Mắt Sài Gòn, Vinmec, and MEDLATEC — see the original PDF for the complete, numbered bibliography.

## Acknowledgments

The team thanks Ths. Bs. Trần Thủy Trinh (Ophthalmology Department, Thu Duc City Hospital) for clinical guidance throughout the project, and the school's science research faculty and leadership for their support.
