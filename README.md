# ⚡ Mini-Micro Machine Learning Projects Hub

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.8-F7931E.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Author](https://img.shields.io/badge/Author-Shyam%20Ranasara-purple.svg)]()

Welcome to the **Mini-Micro Machine Learning Projects Hub** created by **Shyam Ranasara**. This repository serves as a centralized portfolio housing distinct, fully-functional Machine Learning and Data Science applications. 

Each project is designed to solve a specific real-world task — ranging from financial data analytics and NLP text verification to clinical health risk classification and car market price estimation.

---

## 🌟 Key Highlights

- **Central Interactive Dashboard (`app.py`)**: A multi-page Streamlit application that unifies all sub-projects under a single interface.
- **Standalone Sub-Project Dashboards**: Every project folder contains its own dedicated `app.py` and `README.md`, allowing each project to run independently.
- **Pre-Trained Machine Learning Models**: All ML models are serialized (`.pkl`) and ready for immediate, low-latency offline inference.
- **Rich Visualizations**: Interactive Plotly charts, risk gauges, metric cards, and correlation heatmaps.

---

## 📂 Repository Sitemap & Project Breakdown

```
mini-micro-project/
├── app.py                         # ⚡ Central Multi-Project Streamlit Hub
├── requirements.txt               # 📦 Global Dependencies
├── README.md                      # 📖 Repository Master Documentation
│
├── Election Bonds/                # 🗳️ Project 1: Electoral Bonds Data Analytics
│   ├── app.py                     # Standalone Dashboard
│   ├── README.md                  # Project Documentation
│   ├── df.csv                     # Merged Bond Purchase & Encashment Dataset
│   ├── Company.csv                # Purchasers Raw Dataset
│   └── Party.csv                  # Political Parties Raw Dataset
│
├── Fake News Detection/           # 📰 Project 2: Fake News Classification AI
│   ├── app.py                     # Standalone Dashboard
│   ├── train_model.py             # NLP Model Training Script
│   ├── model.pkl                  # Serialized Logistic Regression Classifier
│   ├── vectorizer.pkl             # Serialized TF-IDF Vectorizer
│   └── README.md                  # Project Documentation
│
├── Heart Attack Analysis/         # ❤️ Project 3: Clinical Heart Risk Predictor
│   ├── app.py                     # Standalone Dashboard
│   ├── train_model.py             # Random Forest Model Training Script
│   ├── heart.csv                  # Heart Disease Vitals Dataset
│   ├── heart_model.pkl            # Serialized Random Forest Model (80.3% Acc)
│   ├── scaler.pkl                 # StandardScaler Artifact
│   └── README.md                  # Project Documentation
│
└── car_price/                     # 🚗 Project 4: Used Car Resale Price Valuation
    ├── app.py                     # Standalone Dashboard
    ├── train_model.py             # Gradient Boosting Training Script
    ├── README.md                  # Project Documentation
    ├── data/                      # Model Checkpoints & Label Encoders
    │   ├── HistGradientBoostingRegressor.pkl
    │   ├── Location_LabelEncoder.pkl
    │   ├── pame_LabelEncoder.pkl
    │   └── pred_price.py
    └── manage.py                  # Legacy Django Web Server
```

---

## 📊 Summary of Projects

| Icon | Project Name | Domain | ML Algorithm / Method | Key Output / Metric | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 🗳️ | **[Election Bonds](./Election%20Bonds)** | Financial EDA | Merged Linkage & Aggregations | Donors, Party Encashed Amounts, Search | ✅ Active |
| 📰 | **[Fake News Detection](./Fake%20News%20Detection)** | NLP Classification | TF-IDF + Logistic Regression | Real vs Fake Risk Gauge & Token Weights | ✅ Active |
| ❤️ | **[Heart Attack Analysis](./Heart%20Attack%20Analysis)** | Clinical ML | Random Forest Classifier | **80.3% Acc**, **0.911 ROC-AUC** Gauge | ✅ Active |
| 🚗 | **[Car Price Valuation](./car_price)** | Price Regression | `HistGradientBoostingRegressor` | Estimated Price (Lakhs INR) & Resale Range | ✅ Active |

---

## 🚀 Quickstart Guide

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/shyamranasara/mini-micro-project.git
cd mini-micro-project

# Install required Python packages
pip install -r requirements.txt
```

### 2. Launch Central Hub Dashboard
To open the multi-project portfolio hub:
```bash
streamlit run app.py
```

### 3. Run Individual Projects Standalone
You can also run any sub-project dashboard directly:
```bash
# 🗳️ Electoral Bonds Dashboard
streamlit run "Election Bonds/app.py"

# 📰 Fake News Detection Dashboard
streamlit run "Fake News Detection/app.py"

# ❤️ Heart Attack Risk Predictor Dashboard
streamlit run "Heart Attack Analysis/app.py"

# 🚗 Car Price Valuation Dashboard
streamlit run "car_price/app.py"
```

---

## 🛠️ Technology Stack

- **Primary Language**: Python 3.14
- **Web App Framework**: Streamlit
- **Machine Learning**: Scikit-Learn (RandomForest, HistGradientBoosting, LogisticRegression, TF-IDF)
- **Data Manipulation**: Pandas, NumPy
- **Interactive Plotting**: Plotly, Seaborn, Matplotlib
- **Model Persistence**: Joblib, Pickle

---

## 👤 Author & Acknowledgments

Developed with ❤️ by **Shyam Ranasara**.  
Feel free to fork this repository, explore the interactive dashboards, and build upon these machine learning models!