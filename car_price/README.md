# 🚗 Used Car Price Valuation AI

A machine learning regression model designed to predict market resale prices of used cars in India based on vehicle parameters, specifications, and mileage history.

## 📌 Overview
- **Objective**: Estimate secondhand vehicle market price in **Lakhs INR** (₹ 1 Lakh = ₹ 100,000).
- **Algorithm**: `HistGradientBoostingRegressor` (Scikit-Learn).
- **Categorical Encoders**: Scikit-Learn `LabelEncoder` for Car Brand/Model (`pame_LabelEncoder.pkl`) and Metropolitan City (`Location_LabelEncoder.pkl`).

## ⚙️ Features Used in Prediction
1. `Name`: Car Make & Model name label index.
2. `Location`: City where vehicle is registered/sold.
3. `Year`: Year of manufacture / registration.
4. `Kilometers Driven`: Total distance covered in kilometers.
5. `Fuel Type`: 1: Diesel, 2: Petrol, 3: CNG, 4: LPG.
6. `Transmission`: 1: Manual, 2: Automatic.
7. `Owner History`: 1: First Owner, 2: Second Owner, 3: Third Owner, 4: Fourth & Above.
8. `Mileage`: Fuel efficiency in km/l or km/kg.
9. `Engine`: Engine displacement capacity in CC.
10. `Power`: Maximum engine power in BHP.
11. `Seats`: Total passenger seating capacity.

## 🚀 How to Run
```bash
# 1. Train Model (Optional, pre-trained files included in car_price/data/)
python "car_price/train_model.py"

# 2. Launch Dashboard Standalone
streamlit run "car_price/app.py"

# 3. (Optional) Launch legacy Django app
python "car_price/manage.py" runserver
```
