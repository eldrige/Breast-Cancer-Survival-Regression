# 🎗️ Breast Cancer Survival Prediction - ML Formative Assessment

**Mission:** Transform breast cancer care in Africa with artificial intelligence and community support

---

## 📋 Project Overview

This project implements a complete machine learning pipeline to predict breast cancer patient survival times using clinical and pathological data. The system is designed to support healthcare delivery in resource-limited settings across Africa.

### ✅ Assignment Requirements Fulfilled

1. **✓ Dataset Selection** - Breast Cancer Survival Dataset (Regression)
2. **✓ Data Visualizations** - 7 comprehensive visualizations with interpretations
3. **✓ Feature Engineering** - Complete analysis and feature selection
4. **✓ Numeric Conversion** - All categorical features encoded
5. **✓ Data Standardization** - StandardScaler applied
6. **✓ Three Models Implemented:**
   - Linear Regression (standard + gradient descent)
   - Decision Tree Regressor
   - Random Forest Regressor
7. **✓ Gradient Descent Optimization** - Loss curves plotted
8. **✓ Before/After Scatter Plots** - Model performance visualization
9. **✓ Best Model Saved** - Automated selection and saving
10. **✓ Prediction Script** - Complete deployment-ready script

---

## 📊 Dataset Information

### Breast Cancer Survival Dataset

**Source:** [Kaggle - Breast Cancer Survival Dataset](https://www.kaggle.com/datasets/kreeshrajani/breast-cancer-survival-dataset)

**Why This Dataset?**

- ✅ **Regression-appropriate:** Contains continuous target variable (survival months)
- ✅ **Clinically relevant:** Real patient data with comprehensive features
- ✅ **Well-documented:** Widely used in medical research
- ✅ **Africa-relevant:** Features available in resource-limited settings

**Key Features:**

- Age at diagnosis
- Tumor size
- Lymph node status
- Histologic grade
- ER/HER2 status
- Tumor stage
- Survival time (TARGET VARIABLE)

## 🚀 Getting Started

### Prerequisites

```bash
# Required Python version
Python 3.8+

# Required libraries
pip install pandas numpy matplotlib seaborn scikit-learn joblib
```

## 📁 Project Structure

```
linear-regression/
│
├── breast_cancer_ml_training.py    # Main training script
├── predict_survival.py              # Prediction script
├── breast_cancer_survival.csv       # Dataset (download separately)
│
├── Generated Files:
│   ├── best_breast_cancer_model.pkl    # Trained model
│   ├── scaler.pkl                       # Feature scaler
│   ├── label_encoders.pkl               # Categorical encoders
│   ├── model_metadata.json              # Model information
│   │
│   └── Visualizations:
│       ├── 01_survival_distribution.png
│       ├── 02_correlation_matrix.png
│       ├── 03_feature_distributions.png
│       ├── 04_loss_curve.png
│       ├── 05_before_after_scatter.png
│       ├── 06_feature_importance.png
│       └── 07_model_comparison.png
```

---

## 🔬 Methodology

### 1. Data Preprocessing

- **Missing Value Handling:** Median imputation for numeric features
- **Categorical Encoding:** Label encoding for categorical variables
- **Feature Scaling:** StandardScaler (mean=0, std=1)
- **Train-Test Split:** 80-20 split with random_state=42

### 2. Models Implemented

#### a) Linear Regression (Standard)

```python
LinearRegression()
```

- Baseline model using normal equation
- Fast training, interpretable coefficients

#### b) Linear Regression (Gradient Descent)

```python
SGDRegressor(max_iter=2000, learning_rate='adaptive')
```

- Iterative optimization
- Loss curve tracking
- Demonstrates convergence

#### c) Decision Tree Regressor

```python
DecisionTreeRegressor(max_depth=10, min_samples_split=10)
```

- Non-linear relationship capturing
- Feature importance analysis
- Handles complex patterns

#### d) Random Forest Regressor

```python
RandomForestRegressor(n_estimators=100, max_depth=15)
```

- Ensemble method
- Robust to overfitting
- Best overall performance

### 3. Model Evaluation Metrics

- **RMSE (Root Mean Squared Error):** Prediction accuracy in months
- **R² Score:** Proportion of variance explained
- **MAE (Mean Absolute Error):** Average prediction error

---

## 📈 Visualizations & Interpretations

### 1. Survival Distribution

**Purpose:** Understand the target variable distribution
**Interpretation:**

- Shows the range and frequency of survival times
- Identifies outliers and skewness
- Validates suitability for regression

### 2. Correlation Matrix

**Purpose:** Identify feature relationships
**Interpretation:**

- Highlights features strongly correlated with survival
- Detects multicollinearity issues
- Guides feature selection

### 3. Feature Distributions

**Purpose:** Analyze key predictors
**Interpretation:**

- Tumor size vs survival relationship
- Age distribution patterns
- Identifies data quality issues

### 4. Loss Curve (Gradient Descent)

**Purpose:** Monitor model training
**Interpretation:**

- Shows convergence of optimization
- Indicates if model is learning
- Detects overfitting (gap between train/test loss)

### 5. Before/After Scatter Plots

**Purpose:** Visualize model improvement
**Interpretation:**

- Before: Raw data relationships
- After: Prediction accuracy vs actual values
- Points near diagonal = good predictions

### 6. Feature Importance

**Purpose:** Identify key predictors
**Interpretation:**

- Ranks features by importance
- Guides clinical focus areas
- Supports model explainability

### 7. Model Comparison

**Purpose:** Compare all models
**Interpretation:**

- Visual comparison of RMSE, R², MAE
- Identifies best-performing model
- Supports model selection decision

---

## 🎯 Results & Performance

### Expected Performance Range

| Model               | Test RMSE         | Test R²       | Test MAE          |
| ------------------- | ----------------- | ------------- | ----------------- |
| Linear Regression   | ~40-60 months     | 0.40-0.60     | ~30-45 months     |
| Gradient Descent LR | ~40-60 months     | 0.40-0.60     | ~30-45 months     |
| Decision Tree       | ~35-55 months     | 0.45-0.65     | ~28-42 months     |
| **Random Forest**   | **~30-50 months** | **0.50-0.70** | **~25-40 months** |

_Note: Actual results depend on the dataset used_

---

## 🔮 Making Predictions

### Using the Prediction Script

The `predict_survival.py` script offers three modes:

#### 1. View Example Predictions

- Pre-configured patient scenarios
- High-risk, moderate-risk, and low-risk profiles
- Demonstrates risk stratification

#### 2. Interactive Mode

- Enter patient data manually
- Real-time prediction
- Immediate risk assessment

#### 3. Batch Mode

- Process multiple patients from CSV
- Generates summary report
- Risk distribution analysis

### Example Usage

```python
# Example patient data
patient = {
    'age_at_diagnosis': 55,
    'tumor_size': 35.2,
    'lymph_nodes_examined_positive': 3,
    'neoplasm_histologic_grade': 2,
    'er_status': 'Positive',
    'her2_status': 'Negative',
    'tumor_stage': 2
}

# Output:
# Predicted Survival: 65.3 months (5.44 years)
# Risk Category: Moderate Risk
# Recommendation: Regular monitoring and standard treatment protocol
```

---

## 👥 Contributing

This project is developed as a formative assessment but can be extended:

- Improve model performance with hyperparameter tuning
- Add cross-validation
- Implement deep learning models
- Create web interface
- Develop mobile app for field deployment
