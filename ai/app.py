from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Traffic Prediction API")

# Load model and encoders
model = joblib.load("models/traffic_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")


class TrafficInput(BaseModel):
    Time: str
    Day: str
    Weather: str
    Vehicle_Count: int
    Speed: int


@app.get("/")
def home():
    return {"message": "Traffic Prediction API is running"}


@app.post("/predict")
def predict(data: TrafficInput):

    input_data = data.dict()

    for column in ["Time", "Day", "Weather"]:
        input_data[column] = label_encoders[column].transform(
            [input_data[column]]
        )[0]

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    traffic = label_encoders["Traffic_Level"].inverse_transform([prediction])[0]

    return {
        "traffic_level": traffic
    }
@app.post("/predict-future")
def predict_future(data: TrafficInput):

    input_data = data.dict()

    # Simple simulation for next 15 minutes
    input_data["Vehicle_Count"] += 30
    input_data["Speed"] = max(10, input_data["Speed"] - 5)

    for column in ["Time", "Day", "Weather"]:
        input_data[column] = label_encoders[column].transform(
            [input_data[column]]
        )[0]

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    traffic = label_encoders["Traffic_Level"].inverse_transform([prediction])[0]

    return {
        "predicted_traffic_15_min": traffic
    }
@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "AI Traffic Prediction"
    }