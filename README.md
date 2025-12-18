# Email-Phishing-Check

A FastAPI-based REST API that detects whether an email is phishing or legitimate using a machine learning model.
The API supports single email prediction as well as batch email classification, returning class probabilities when available.

 Features:

🔍 Detects phishing emails using a trained ML pipeline

⚡ FastAPI backend for high performance

📊 Returns prediction with probabilities

📦 Supports single email and batch prediction



 Tech Stack:

Python
FastAPI
Scikit-learn
Joblib
NumPy
Pydantic
Uvicorn

📁 Project Structure
email_phishing/
│
├── server/
│   ├── app.py                  # FastAPI application
│   └── email_phishing_model.joblib  # Trained ML model
│
├── requirements.txt
├── README.md
└── ...

 Model Details

The model is loaded from a serialized file:
email_phishing_model.joblib

The artifact contains:
pipeline: preprocessing + classifier
label_encoder: class labels (e.g., phishing / legitimate)

Predictions are generated using:
predict_proba() (if supported),

fallback to predict() otherwise


🔧 Installation & Setup

1️⃣ Clone the repository
git clone https://github.com/rishab-1718/Email-Phishing-Check.git

cd Email-Phishing-Check

 Install dependencies
pip install -r requirements.txt

▶️ Run the API Server
uvicorn server.app:app --reload


The server will start at:
http://127.0.0.1:8000

 API Endpoints:
🩺 Health Check

GET /health
Response:
{
  "status": "ok",
  "classes": ["phishing", "legitimate"]
}

📩 Predict Single Email
POST /predict_email
Request Body:

{
  "subject": "Urgent: Verify your account",
  "body": "Click the link below to avoid suspension."
}


Response:

{
  "prediction": "phishing",
  "probabilities": {
    "legitimate": 0.12,
    "phishing": 0.88
  }
}

Future Improvements:
Authentication & rate limiting
Model retraining pipeline
Frontend integration (React / Next.js)

License
This project is for educational and research purposes.
Add a license file if you plan public or commercial use.
