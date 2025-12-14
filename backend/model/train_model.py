import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../../data/churn_data.csv")

df = pd.read_csv(DATA_PATH, sep="\t")

# -----------------------------------------
# FIX COLUMN NAMES FIRST (VERY IMPORTANT)
# -----------------------------------------
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.replace("-", "_")
df.columns = df.columns.str.strip()

selected_columns = [
    "Tenure_Months",
    "Monthly_Charges",
    "Total_Charges",
    "Churn_Score",
    "CLTV",
    "Gender",
    "Senior_Citizen",
    "Partner",
    "Dependents",
    "Internet_Service",
    "Contract",
    "Payment_Method",
]


df = df[selected_columns]

# Handle missing values
df = df.fillna(0)

# Encode categorical variables
label_encoders = {}
for col in df.select_dtypes(include=["object"]).columns:
    if col != "Churn_Label":
        le = LabelEncoder()
        df[col] = df[col].astype(str).str.strip().str.upper()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

# Encode target label
target_encoder = LabelEncoder()
df["Churn_Label"] = target_encoder.fit_transform(df["Churn_Label"])
label_encoders["Churn_Label"] = target_encoder

# Define feature matrix and target
X = df.drop("Churn_Label", axis=1)
y = df["Churn_Label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
pickle.dump(model, open(os.path.join(BASE_DIR, "churn_model.pkl"), "wb"))
pickle.dump(label_encoders, open(
    os.path.join(BASE_DIR, "label_encoders.pkl"), "wb"))

print("MODEL + ENCODERS TRAINED SUCCESSFULLY!")
