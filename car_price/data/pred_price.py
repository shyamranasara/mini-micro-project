import os
import pickle
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, 'HistGradientBoostingRegressor.pkl')
path1 = os.path.join(base_dir, "Location_LabelEncoder.pkl")
path2 = os.path.join(base_dir, "pame_LabelEncoder.pkl")

with open(path, "rb") as f1:
    model = pickle.load(f1)

with open(path1, "rb") as f2:
    location_le = pickle.load(f2)

with open(path2, "rb") as f:
    name_le = pickle.load(f)






# Helper function to get classes for dropdown options
def get_locations():
    return list(location_le.classes_)

def get_car_names():
    return list(name_le.classes_)

# print(name_le.transform(["Maruti Wagon"]))

# fuel_dic1 ={
#     "Diesel":1,
#     "Petrol":2,
#     "CNG":3,
#     "LPG":4
# }


# owner_dic1 = {
#     "First" : 1,
#     "Secand": 2,
#     "Third": 3,
#     "Fourth & Above": 4
# }

# transm_dic1 ={
#     "Manual":1,
#     "Automatic":2
# }

def pred(name, location, year, kd, fuel, trans, owner, milage, engine, power, seats):
    # Safely transform car name
    if name in name_le.classes_:
        int1 = int(name_le.transform([name])[0])
    else:
        # Fallback to closest match or first index
        matches = [n for n in name_le.classes_ if str(name).lower() in n.lower()]
        matched_name = matches[0] if matches else name_le.classes_[0]
        int1 = int(name_le.transform([matched_name])[0])
        
    # Safely transform location
    if location in location_le.classes_:
        int2 = int(location_le.transform([location])[0])
    else:
        matches = [l for l in location_le.classes_ if str(location).lower() in l.lower()]
        matched_loc = matches[0] if matches else location_le.classes_[0]
        int2 = int(location_le.transform([matched_loc])[0])

    features = [[
        int1,
        int2,
        int(year),
        float(kd),
        int(fuel),
        int(trans),
        int(owner),
        float(milage),
        float(engine),
        float(power),
        float(seats)
    ]]
    
    price = model.predict(features)
    return price


