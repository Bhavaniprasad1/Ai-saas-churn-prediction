import pickle

import pandas as pd
from fastapi import APIRouter

router = APIRouter()


# Load model + encoders
model = pickle.load(open("backend/model/churn_model.pkl", "rb"))
encoders = pickle.load(open("backend/model/label_encoders.pkl", "rb"))


@router.post("/predict")
def predict_churn(data: dict):
    df = pd.DataFrame([data])

    # Encode categorical columns using saved encoders
    for col, encoder in encoders.items():
        if col in df.columns:

            # Clean the input to avoid case / space mismatch
            df[col] = df[col].astype(str).str.strip().str.upper()

            # Replace unseen categories with the encoder's first known class
            df[col] = df[col].apply(
                lambda x: x if x in encoder.classes_ else encoder.classes_[0]
            )

            # Transform after fixing unseen labels
            df[col] = encoder.transform(df[col])

    # Make prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0].max()

    return {
        "churn_prediction": int(prediction),
        "confidence": float(probability)
    }
