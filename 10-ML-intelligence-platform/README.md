# ML Intelligence Platform

A modular Python application that automates end-to-end Machine Learning workflows, from dataset validation and preprocessing to model training, optimization, explainability, prediction, and report generation.

Unlike traditional Jupyter Notebook projects, this application is built using a production-style architecture with reusable classes and modular components, making it easy to extend for different machine learning tasks.

---

## Overview

The ML Intelligence Platform provides a complete machine learning pipeline that guides a dataset through every major stage of a professional ML workflow.

Instead of manually writing preprocessing, model training, validation, optimization, and evaluation code for every project, the platform automates the entire process through a structured architecture.

The application supports both Regression and Classification problems and automatically adapts its workflow based on the selected target variable.

---

## Features

### Dataset Loading

- Load any CSV dataset
- Automatic dataset information
- Memory usage
- Dataset dimensions
- Numeric column detection
- Categorical column detection

---

### Dataset Validation

Automatically checks dataset quality by detecting:

- Missing values
- Duplicate rows
- Constant columns
- Empty columns
- Invalid numeric columns
- High-cardinality categorical features

Generates a dataset quality score with quality labels.

---

### Dataset Profiling

Generates detailed exploratory statistics including:

- Descriptive statistics
- Correlation matrix
- Skewness
- Kurtosis
- Outlier detection

---

### Automatic Problem Detection

After selecting the target column, the platform automatically determines whether the problem is:

- Regression
- Classification

No manual configuration is required.

---

### Feature Engineering

Automatic preprocessing includes:

#### Numeric Features

- Median imputation
- StandardScaler

#### Categorical Features

- Most frequent imputation
- OneHotEncoder

The preprocessing pipeline is fully reusable using Scikit-Learn Pipelines.

---

### Model Training

## Regression

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Classification

- Logistic Regression
- Decision Tree
- Random Forest Classifier
- Gradient Boosting Classifier

Each model is trained inside an independent machine learning pipeline.

---

### Model Comparison

Automatically compares trained models using appropriate evaluation metrics.

Regression

- MAE
- RMSE
- R² Score

Classification

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

Results are ranked from best to worst.

---

### Cross Validation

Performs automated 5-Fold Cross Validation.

Reports:

- Mean Score
- Standard Deviation

This provides a better estimate of model generalization than a single train/test split.

---

### Hyperparameter Optimization

Supports automated model optimization using:

- GridSearchCV

The platform automatically finds:

- Best hyperparameters
- Best validation score
- Best estimator

---

### Feature Selection

Multiple feature selection techniques are included:

#### SelectKBest

Ranks the most informative features statistically.

#### Recursive Feature Elimination (RFE)

Iteratively removes less important variables until the optimal subset is obtained.

---

### Model Explainability

Provides multiple explainability techniques.

Feature Importance

- Tree-based importance

Permutation Importance

- Model-agnostic importance estimation

Business Insights

The platform automatically converts feature importance into simple business-oriented explanations.

Example:

> Monthly Charges has a strong influence on customer churn.

---

### Error Analysis

Regression

- Prediction errors
- Residual analysis

Classification

- False Positives
- False Negatives
- Misclassified samples

Reports are automatically exported for further inspection.

---

### Model Persistence

Automatically saves trained assets using Joblib.

Saved components include:

- Trained model
- Preprocessing pipeline

Models can later be loaded without retraining.

---

### Prediction Mode

A prediction interface demonstrates how saved models can be used for inference on new data.

---

### Report Generation

The platform exports machine learning artifacts including:

- Cross Validation Results
- Grid Search Results
- Feature Importance
- Permutation Importance
- Feature Selection Results
- Error Analysis

All reports are saved inside the project outputs directory.

---

## Project Structure

```
ml-intelligence-platform/

├── app.py
├── config/
│
├── src/
│   ├── loader.py
│   ├── validator.py
│   ├── profiler.py
│   ├── preprocessing.py
│   ├── problem_detector.py
│   ├── feature_engineering.py
│   ├── model_selector.py
│   ├── cross_validator.py
│   ├── optimizer.py
│   ├── feature_selector.py
│   ├── explainability.py
│   ├── error_analysis.py
│   ├── persistence.py
│   ├── predictor.py
│   └── exporter.py
│
├── data/
├── models/
├── outputs/
│   ├── reports/
│   ├── charts/
│   └── predictions/
│
└── README.md
```

---

## Workflow

```
Load Dataset
        │
        ▼
Dataset Validation
        │
        ▼
Dataset Profiling
        │
        ▼
Target Selection
        │
        ▼
Automatic Problem Detection
        │
        ▼
Feature Engineering
        │
        ▼
Preprocessing Pipeline
        │
        ▼
Model Training
        │
        ▼
Model Comparison
        │
        ▼
Cross Validation
        │
        ▼
Hyperparameter Optimization
        │
        ▼
Feature Selection
        │
        ▼
Model Explainability
        │
        ▼
Error Analysis
        │
        ▼
Model Persistence
        │
        ▼
Prediction
        │
        ▼
Export Reports
```

---

## Technologies

- Python
- Pandas
- NumPy
- Scikit-Learn
- Plotly
- Joblib

---

## Machine Learning Concepts

This project demonstrates practical implementation of:

### Data Preparation

- Missing Value Imputation
- One-Hot Encoding
- Standard Scaling
- Feature Engineering
- Train/Test Split
- Pipelines

### Regression

- Linear Regression
- Random Forest Regression
- Gradient Boosting Regression

### Classification

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

### Model Validation

- Cross Validation
- Performance Comparison
- Model Ranking

### Model Optimization

- GridSearchCV
- Hyperparameter Tuning

### Feature Engineering

- SelectKBest
- Recursive Feature Elimination

### Explainability

- Feature Importance
- Permutation Importance
- Business Interpretation

### Evaluation

Regression

- MAE
- RMSE
- R²

Classification

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

### Engineering

- Modular Architecture
- Reusable Pipelines
- Model Persistence
- Automatic Report Generation

---

## Example Dataset

The repository includes a sample video game sales dataset to demonstrate the platform.

The application is dataset-agnostic and can be adapted to many regression and classification problems by selecting a different CSV file and target column.

---

## Future Improvements

Planned enhancements include:

- RandomizedSearchCV
- XGBoost
- LightGBM
- CatBoost
- SHAP Explainability
- Optuna Hyperparameter Optimization
- FastAPI REST API
- Streamlit Dashboard
- PDF Report Generation
- Automated Chart Export
- Interactive Prediction Interface

---

## License

This project is intended for educational, portfolio, and research purposes.