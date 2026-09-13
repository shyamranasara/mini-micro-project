# 📰 Fake News Detection AI

An NLP-powered machine learning application designed to classify news headlines and articles into **Real** vs **Fake** content.

## 📌 Overview
- **Objective**: Automate content verification using Natural Language Processing (NLP) and TF-IDF feature extraction.
- **Model**: Scikit-Learn TF-IDF Vectorizer + Logistic Regression Classifier trained on benchmark text features.
- **Key Output**: Binary Classification (Fake vs Real), Confidence Score Gauge, and TF-IDF Token Analysis.

## 🚀 Key Features
- **Instant NLP Inference**: Real-time evaluation of raw text snippets or article bodies.
- **Interactive Gauge Chart**: Visual probability score indicating fake news likelihood.
- **TF-IDF Keyword Extraction**: Identifies key vocabulary tokens driving model decisions.
- **Sample Benchmark Testing**: Built-in interactive preset news samples for immediate testing.

## 🛠️ How to Run
```bash
# 1. Train Model (Optional, pre-trained files included)
python "Fake News Detection/train_model.py"

# 2. Run Dashboard Standalone
streamlit run "Fake News Detection/app.py"
```

## 📐 NLP Pipeline Architecture
1. **Text Normalization**: Lowercasing, removal of punctuation, special characters, URLs, and numbers.
2. **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency) unigram & bigram vectorization.
3. **Classification**: Calibrated Logistic Regression scoring probability of disinformation.
