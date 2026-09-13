# ❤️ Heart Attack Analysis & Prediction

A machine learning clinical risk predictor designed to estimate heart disease risk based on patient vital metrics and diagnostic parameters.

## 📌 Overview
- **Dataset**: UCI Heart Disease dataset (`heart.csv`), containing 303 patient health entries.
- **Model**: Scikit-Learn Random Forest Classifier (100 estimators) tuned for high sensitivity and ROC-AUC.
- **Metrics Achieved**: **80.33% Accuracy**, **0.9113 ROC-AUC Score**.

## 🔬 Clinical Parameters Modeled
| Parameter | Technical Code | Description | Range / Categories |
|---|---|---|---|
| Age | `age` | Patient age in years | 29 - 77 |
| Sex | `sex` | Biological sex | 1 = Male, 0 = Female |
| Chest Pain Type | `cp` | Angina severity level | 0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic |
| Resting BP | `trtbps` | Resting blood pressure | mm Hg |
| Cholesterol | `chol` | Serum cholesterol | mg/dl |
| Fasting Sugar | `fbs` | Fasting blood sugar > 120 mg/dl | 1 = True, 0 = False |
| Resting ECG | `restecg` | Resting electrocardiographic results | 0: Normal, 1: ST-T wave, 2: Hypertrophy |
| Max Heart Rate | `thalachh` | Maximum heart rate achieved | bpm |
| Exercise Angina | `exng` | Exercise-induced angina | 1 = Yes, 0 = No |
| ST Depression | `oldpeak` | ST depression induced by exercise | 0.0 - 6.2 |
| ST Slope | `slp` | Slope of peak exercise ST segment | 0: Upsloping, 1: Flat, 2: Downsloping |
| Major Vessels | `caa` | Number of major vessels colored by fluoroscopy | 0 - 4 |
| Thalassemia | `thall` | Blood disorder test result | 0: Null, 1: Fixed, 2: Normal, 3: Reversable |

## 🚀 How to Run
```bash
# 1. Train Model
python "Heart Attack Analysis/train_model.py"

# 2. Launch Dashboard Standalone
streamlit run "Heart Attack Analysis/app.py"
```
