import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("assets/test.csv")
from sklearn.model_selection import train_test_split

y = df['price']
X = df[[
        "area",
        "property_type",
        "rooms_number",
        "land_area",
        "zip_code",
        "garden",
        "garden_area",
        "equipped_kitchen",
        "swimming_pool",
        "furnished",
        "open_fire",
        "terrace",
        "terrace_area",
        "facades_number",
        "building_state"]]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) 
lr = LinearRegression()
model = lr.fit(X_train, y_train)

filename = 'src/models/model.sav'
pickle.dump(model, open(filename, 'wb'))