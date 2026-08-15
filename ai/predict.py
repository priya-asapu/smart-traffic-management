import joblib
import pandas as pd

# Load model and encoders
model = joblib.load("models/traffic_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# Sample input
input_data = {
    "Time": "09:00",
    "Day": "Monday",
    "Weather": "Rainy",
    "Vehicle_Count": 220,
    "Speed": 20
}

# Convert categorical values to numbers
for column in ["Time", "Day", "Weather"]:
    input_data[column] = label_encoders[column].transform([input_data[column]])[0]

# Create DataFrame
df = pd.DataFrame([input_data])

# Predict
prediction = model.predict(df)[0]

# Convert prediction back to text
traffic_level = label_encoders["Traffic_Level"].inverse_transform([prediction])[0]

print("Predicted Traffic Level:", traffic_level)