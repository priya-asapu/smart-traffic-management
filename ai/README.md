# AI Traffic Prediction Module

## Project Overview

This module is part of the Smart Traffic Management System. It predicts the current traffic level and future traffic conditions using Machine Learning.

---

## Features

- Predict Current Traffic (Low, Medium, High)
- Predict Future Traffic (10–15 minutes)
- Health Check API
- FastAPI Integration
- Machine Learning using Random Forest

---

## Technologies Used

- Python
- FastAPI
- Pandas
- NumPy
- Scikit-learn
- Joblib

---

## Folder Structure

ai/
├── api/
├── dataset/
├── models/
├── utils/
├── train_model.py
├── predict.py
├── app.py
├── requirements.txt
└── README.md

---

## API Endpoints

### GET /

Returns a welcome message.

### GET /health

Checks whether the AI service is running.

### POST /predict

Predicts the current traffic level.

### POST /predict-future

Predicts the traffic level after 10–15 minutes.

---

## How to Run

1. Activate virtual environment

```
venv\Scripts\activate
```

2. Run the API

```
python -m uvicorn app:app --reload
```

3. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Output

The API predicts one of the following:

- Low Traffic
- Medium Traffic
- High Traffic

---

## Team

Project: Smart Traffic Management System

Module: AI Traffic Prediction