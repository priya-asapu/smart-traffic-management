import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Load dataset
data = pd.read_csv("dataset/traffic_data.csv")

# Encode categorical columns
label_encoders = {}

for column in ["Time", "Day", "Weather", "Traffic_Level"]:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

X = data[["Time", "Day", "Weather", "Vehicle_Count", "Speed"]]
y = data["Traffic_Level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/traffic_model.pkl")
joblib.dump(label_encoders, "models/label_encoders.pkl")

print("Model saved successfully.")