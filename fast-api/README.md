# Breast Cancer Survival Prediction API

FastAPI application for predicting breast cancer patient survival times using machine learning.

## Features

- **POST /predict** - Predict survival time for breast cancer patients
- **GET /health** - Health check endpoint
- **GET /docs** - Interactive Swagger UI documentation
- **CORS enabled** - Cross-origin resource sharing for web applications
- **Pydantic validation** - Data type and range constraints for all inputs

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure model files are in the `../linear-regression/` directory:
   - `best_breast_cancer_model.pkl`
   - `scaler.pkl`
   - `label_encoders.pkl`
   - `model_metadata.json`

## Running Locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables if needed
5. Deploy!

After deployment, your Swagger UI will be available at:
**https://your-app-name.onrender.com/docs**

## API Endpoints

### POST /predict

Predict breast cancer patient survival time.

**Request Body:**

```json
{
  "Age": 52,
  "Gender": "FEMALE",
  "Protein1": 0.5,
  "Protein2": 1.2,
  "Protein3": -0.1,
  "Protein4": 0.05,
  "Tumour_Stage": "II",
  "Histology": "Infiltrating Ductal Carcinoma",
  "ER status": "Positive",
  "PR status": "Positive",
  "HER2 status": "Negative",
  "Surgery_type": "Lumpectomy"
}
```

**Response:**

```json
{
  "predicted_days": 365.0,
  "predicted_months": 12.2,
  "predicted_years": 1.0,
  "risk_category": "ELEVATED RISK",
  "risk_color": "🟠",
  "recommendation": "Enhanced monitoring and aggressive treatment recommended"
}
```

### GET /health

Check API health and model status.

## Input Validation

- **Age**: Integer between 18 and 100
- **Gender**: MALE or FEMALE
- **Protein1-4**: Float between -5.0 and 5.0
- **Tumour_Stage**: I, II, or III
- **ER/PR/HER2 status**: Positive or Negative
- **Histology**: String (e.g., "Infiltrating Ductal Carcinoma")
- **Surgery_type**: String (e.g., "Lumpectomy", "Mastectomy")

## Mission

Transform breast cancer care in Africa with AI and community support.
