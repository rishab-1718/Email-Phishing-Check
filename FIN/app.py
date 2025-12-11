# server/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import joblib
import numpy as np

# Load model artifact (ensure email_phishing_model.joblib is in same folder)
ART = joblib.load("email_phishing_model.joblib")
PIPELINE = ART["pipeline"]
LE = ART["label_encoder"]
CLASSES = list(LE.classes_)

app = FastAPI(title="Email Phishing Detector API")

# Allow local dev origin (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailIn(BaseModel):
    subject: Optional[str] = ""
    body: Optional[str] = ""

class BatchIn(BaseModel):
    emails: List[EmailIn]

@app.get("/health")
def health():
    return {"status": "ok", "classes": CLASSES}

@app.post("/predict_email")
def predict_email(email: EmailIn):
    text = (email.subject or "") + " " + (email.body or "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty subject and body")
    try:
        # If pipeline supports predict_proba
        if hasattr(PIPELINE, "predict_proba"):
            probs = PIPELINE.predict_proba([text])[0].tolist()
            idx = int(np.argmax(probs))
            return {
                "prediction": CLASSES[idx],
                "probabilities": {CLASSES[i]: float(probs[i]) for i in range(len(CLASSES))}
            }
        else:
            pred = PIPELINE.predict([text])[0]
            return {"prediction": CLASSES[int(pred)], "probabilities": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_batch")
def predict_batch(batch: BatchIn):
    texts = [ (e.subject or "") + " " + (e.body or "") for e in batch.emails ]
    if hasattr(PIPELINE, "predict_proba"):
        probs = PIPELINE.predict_proba(texts)
        preds = probs.argmax(axis=1)
        out = []
        for t, pvec, p in zip(texts, probs, preds):
            out.append({
                "text": t,
                "prediction": CLASSES[int(p)],
                "probabilities": {CLASSES[i]: float(pvec[i]) for i in range(len(CLASSES))}
            })
        return {"results": out}
    else:
        preds = PIPELINE.predict(texts)
        return {"results": [{"text": t, "prediction": CLASSES[int(p)], "probabilities": None} for t,p in zip(texts, preds)]}
