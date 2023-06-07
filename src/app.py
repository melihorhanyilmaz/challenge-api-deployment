from fastapi import FastAPI, HTTPException
import uvicorn
from predict.prediction import predict
from preprocessing.cleaning_data import preprocess
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import Literal, Optional

app = FastAPI()

class Data1(BaseModel):

    area: int
    property_type: Literal["APARTMENT", "HOUSE", "OTHERS"]
    rooms_number: int
    zip_code: int | None = 0
    land_area: int | None = 0
    garden: bool | None = False
    garden_area: int | None = 0
    equipped_kitchen: bool | None = False
    swimming_pool: bool | None = False
    furnished: bool | None = False
    open_fire: bool | None = False
    terrace: bool | None = False
    terrace_area: int | None = 0
    facades_number: int | None = 0
    building_state: Literal['NEW', 'JUST RENOVATED',
                     'GOOD', 'TO RENOVATE', 'TO REBUILD']

@app.get("/")
async def root():
    return {"Status": "Alive!"}

@app.get("/predict")
async def showing():
    return "Please send a json format house data"

@app.post("/predict")
async def predicting(data: Data1):
    json_data = jsonable_encoder(data)
    print('before process', json_data)
    print(type(json_data))
    processed_data = preprocess(json_data)
    for row in processed_data.iterrows():
        print(row)
    print(type(processed_data))
    final_predict = predict(processed_data)
    return {"prediction": final_predict[0]}



