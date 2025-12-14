from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.predict import router as predict_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all frontends
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Churn Prediction API is running!"}


app.include_router(predict_router, prefix="/api")
