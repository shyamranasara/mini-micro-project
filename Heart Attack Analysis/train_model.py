import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

def train_and_save_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'heart.csv')
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"heart.csv not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    X = df.drop(columns=['output'])
    y = df['output']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:, 1])
    
    print(f"Heart Attack Prediction Model Trained successfully!")
    print(f"Accuracy: {acc:.4f}")
    print(f"ROC-AUC Score: {roc:.4f}")
    
    joblib.dump(model, os.path.join(script_dir, 'heart_model.pkl'))
    joblib.dump(scaler, os.path.join(script_dir, 'scaler.pkl'))
    print("Model and Scaler saved successfully.")

if __name__ == '__main__':
    train_and_save_model()
