import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder

def train_and_save_car_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    loc_path = os.path.join(data_dir, "Location_LabelEncoder.pkl")
    name_path = os.path.join(data_dir, "pame_LabelEncoder.pkl")
    
    if os.path.exists(loc_path) and os.path.exists(name_path):
        with open(loc_path, 'rb') as f:
            loc_le = pickle.load(f)
        with open(name_path, 'rb') as f:
            name_le = pickle.load(f)
    else:
        # Fallback list of locations & popular car names
        loc_le = LabelEncoder()
        loc_le.fit(['Ahmedabad', 'Bangalore', 'Chennai', 'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur', 'Kochi', 'Kolkata', 'Mumbai', 'Pune'])
        name_le = LabelEncoder()
        name_le.fit(['Maruti Wagon R', 'Maruti Swift', 'Hyundai i20', 'Honda City', 'Toyota Fortuner', 'BMW 3 Series', 'Audi A4', 'Mercedes-Benz C-Class'])
        with open(loc_path, 'wb') as f:
            pickle.dump(loc_le, f)
        with open(name_path, 'wb') as f:
            pickle.dump(name_le, f)

    loc_count = len(loc_le.classes_)
    name_count = len(name_le.classes_)
    
    # Generate realistic training data to train HistGradientBoostingRegressor
    np.random.seed(42)
    n_samples = 3000
    
    names = np.random.randint(0, name_count, n_samples)
    locations = np.random.randint(0, loc_count, n_samples)
    years = np.random.randint(2005, 2024, n_samples)
    kd = np.random.randint(5000, 180000, n_samples)
    fuel = np.random.choice([1, 2, 3, 4], n_samples, p=[0.45, 0.45, 0.07, 0.03]) # 1: Diesel, 2: Petrol, 3: CNG, 4: LPG
    trans = np.random.choice([1, 2], n_samples, p=[0.75, 0.25]) # 1: Manual, 2: Automatic
    owner = np.random.choice([1, 2, 3, 4], n_samples, p=[0.7, 0.2, 0.08, 0.02])
    mileage = np.random.uniform(10.0, 28.0, n_samples)
    engine = np.random.uniform(796, 3000, n_samples)
    power = np.random.uniform(40, 250, n_samples)
    seats = np.random.choice([4, 5, 7, 8], n_samples, p=[0.05, 0.8, 0.12, 0.03])
    
    # Formula for realistic target price in Lakhs (INR)
    base_price = (power * 0.08) + (engine * 0.003) + (trans * 2.5) + (name_le.classes_.size / (names + 1)) * 0.1
    age = 2024 - years
    depreciation = (1.0 - 0.07) ** age
    
    price = np.maximum(0.5, (base_price * depreciation) - (kd * 0.000015) + np.random.normal(0, 0.5, n_samples))
    price = np.round(price, 2)
    
    X = np.column_stack([names, locations, years, kd, fuel, trans, owner, mileage, engine, power, seats])
    y = price
    
    model = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.08, random_state=42)
    model.fit(X, y)
    
    model_path = os.path.join(data_dir, 'HistGradientBoostingRegressor.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"Car Price Prediction Model trained & serialized to {model_path} successfully!")

if __name__ == '__main__':
    train_and_save_car_model()
