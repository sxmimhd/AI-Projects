# 🧠 Deep Learning Intelligence Platform

An extensible deep learning platform built with **PyTorch** that automates the complete workflow of training, evaluating, and deploying deep learning models for both **Computer Vision** and **Natural Language Processing** tasks.

Unlike a project designed for a single dataset, this platform dynamically analyzes the provided dataset, detects its task, prepares the data automatically, builds the appropriate neural network, trains the model, evaluates its performance, and exports everything required for inference.

The project was designed as a reusable deep learning framework rather than a one-time experiment.

---

## Features

### Automatic Dataset Detection

The platform automatically determines the dataset type.

- Image datasets
- Text datasets (CSV)

---

### Dataset Validation

Before training, the platform validates the dataset by checking:

- Dataset structure
- Missing values
- Corrupted images
- Empty classes
- Duplicate records
- Class distribution
- Dataset statistics

---

### Automatic Task Detection

The platform automatically detects the machine learning task.

Current supported tasks:

- Image Classification
- Binary Text Classification

The architecture allows additional tasks to be added later.

---

### Intelligent Model Selection

Depending on the detected task, users can select different neural network architectures.

### Computer Vision

- Transfer Learning (ResNet18)
- Custom CNN

### Natural Language Processing

- Sentiment Classification Network
    - Embedding Layer
    - Global Average Pooling
    - Fully Connected Layers

---

## Supported Deep Learning Pipelines

### Computer Vision Pipeline

```text
Image Dataset
        │
        ▼
Dataset Validation
        │
        ▼
Dataset Analysis
        │
        ▼
Task Detection
        │
        ▼
Model Selection
        │
        ▼
Image Preprocessing
        │
        ▼
Dataset Split
        │
        ▼
Model Creation
        │
        ▼
Training
        │
        ▼
Evaluation
        │
        ▼
Prediction
        │
        ▼
Model Export
```

---

### NLP Pipeline

```text
CSV Dataset
        │
        ▼
Dataset Validation
        │
        ▼
Column Selection
        │
        ▼
Text Cleaning
        │
        ▼
Tokenizer
        │
        ▼
Vocabulary Builder
        │
        ▼
Dataset Split
        │
        ▼
Sentiment Network
        │
        ▼
Training
        │
        ▼
Evaluation
        │
        ▼
Model Export
```

---

# Computer Vision

The platform supports image classification using multiple architectures.

## Available Models

### Transfer Learning

- ResNet18 Backbone
- Frozen Feature Extractor
- Custom Classification Head
- Fine-tuning Ready

### Custom CNN

The framework also includes a fully custom convolutional neural network built entirely with PyTorch.

Typical architecture:

```text
Input Image
      │
      ▼
Conv Block
      │
      ▼
Conv Block
      │
      ▼
Conv Block
      │
      ▼
Adaptive Pooling
      │
      ▼
Fully Connected Layers
      │
      ▼
Predicted Class
```

---

# Natural Language Processing

The platform supports binary sentiment classification.

Pipeline:

```text
Raw Text
      │
      ▼
Cleaning
      │
      ▼
Tokenization
      │
      ▼
Vocabulary Encoding
      │
      ▼
Embedding Layer
      │
      ▼
Average Pooling
      │
      ▼
Fully Connected Layers
      │
      ▼
Sentiment Prediction
```

---

# Training Features

The framework includes:

- Automatic train/validation/test splitting
- Adam Optimizer
- Learning Rate Scheduler
- Best model checkpointing
- Training history export
- Automatic device detection (CPU/CUDA)
- Model summary generation

---

# Evaluation

Generated evaluation metrics include:

### Vision

- Accuracy
- Top-5 Accuracy
- Classification Report
- Confusion Matrix
- Confidence Scores

### NLP

- Accuracy
- Classification Report
- Prediction Confidence

---

# Prediction System

The framework supports inference after training.

### Vision

- Single image prediction
- Batch folder prediction
- Confidence estimation

### NLP

- Binary sentiment prediction
- Confidence estimation

---

# Model Persistence

Every trained model is automatically exported.

Generated artifacts include:

```text
models/
│
├── best_model.pth
├── config.json
├── class_names.pkl        (Vision)
└── vocabulary.pkl         (NLP)
```

This allows trained models to be restored without retraining.

---

# Project Structure

```text
src/
│
├── dataset/
├── preprocessing/
├── models/
├── training/
├── prediction/
├── persistence/
├── visualization/
├── explainability/
├── tasks/
└── utils/
```

---

# Technologies

- Python
- PyTorch
- TorchVision
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Pillow

---

# Supported Tasks

| Task | Status |
|-------|--------|
| Image Classification | ✅ |
| Binary Sentiment Classification | ✅ |
| Transfer Learning | ✅ |
| Custom CNN | ✅ |
| Dataset Validation | ✅ |
| Dataset Analysis | ✅ |
| Automatic Task Detection | ✅ |
| Model Selection | ✅ |
| Training | ✅ |
| Evaluation | ✅ |
| Prediction | ✅ |
| Model Persistence | ✅ |

---

# Testing

The framework has been tested on multiple datasets covering both supported domains.

### Computer Vision

- Multi-class image classification datasets
- Custom CNN
- Transfer Learning (ResNet18)

### Natural Language Processing

- Large-scale review datasets
- Binary sentiment classification
- Automatic vocabulary generation
- Tokenization pipeline

All core modules—including dataset loading, preprocessing, training, evaluation, prediction, and model persistence—have been successfully validated during development.

---

# Future Improvements

The current architecture was intentionally designed to be extensible.

Potential future additions include:

- Multi-label image classification
- Multi-class text classification
- Regression models
- Object detection
- Semantic segmentation
- Transformer-based NLP models
- Vision Transformers (ViT)
- Grad-CAM integration
- NLP explainability
- ONNX and TorchScript export
- Hyperparameter optimization
- Distributed training

---

## License

This project is intended for educational purposes, research, and portfolio demonstration.