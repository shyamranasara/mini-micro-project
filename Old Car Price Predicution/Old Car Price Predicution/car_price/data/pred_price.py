import pickle
import numpy as np

path ='data\HistGradientBoostingRegressor.pkl'
path1 = "data\Location_LabelEncoder.pkl"
path2 = "data\pame_LabelEncoder.pkl"


# path ='HistGradientBoostingRegressor.pkl'
# path1 = "Location_LabelEncoder.pkl"
# path2 = "pame_LabelEncoder.pkl"






with open( path, "rb")as f1:
    model  = pickle.load(f1)


with open( path1, "rb")as f2:
    location_le  = pickle.load(f2)

with open( path2, "rb")as f:
    name_le  = pickle.load(f)




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

def pred(name,location,year, kd ,fuel , trans , owner , milage , engine, power, seats ):
    int_name = name_le.transform([name])
    int1 = int(int_name)
    int_location = location_le.transform([location])
    int2 = int(int_location)
    # int_fuel = fuel_dic1[fuel]
    # int_trans = transm_dic1[trans]
    # int_owner = owner_dic1[owner]
    price = model.predict([[int1,int2, year,kd,fuel,trans,owner, milage, engine, power, seats]])
    print(price)
    return price

