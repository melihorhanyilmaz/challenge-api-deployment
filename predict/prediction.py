import pickle

with open("./models/model.sav", 'rb') as file:
    loaded_model = pickle.load(file)
    

def predict(df):
    return loaded_model.predict(df)



