"""
FastAPI Application for Breast Cancer Survival Prediction
Mission: Transform breast cancer care in Africa with AI and community support
"""

import os
import sys
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, ConfigDict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'linear-regression')

app = FastAPI(
    title="Breast Cancer Survival Prediction API",
    description="API for predicting breast cancer patient survival times using machine learning",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading model and preprocessing components...")
try:
    model = joblib.load(os.path.join(
        MODEL_DIR, 'best_breast_cancer_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    label_encoders = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))

    with open(os.path.join(MODEL_DIR, 'model_metadata.json'), 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    print("✓ All components loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    print("Please ensure model files are in the linear-regression directory")
    sys.exit(1)


class PatientData(BaseModel):
    """Patient data model with validation"""
    Age: int = Field(..., ge=18, le=100,
                     description="Patient age in years (18-100)")
    Gender: str = Field(..., description="Patient gender")
    Protein1: float = Field(..., ge=-5.0, le=5.0,
                            description="Protein1 marker level (-5.0 to 5.0)")
    Protein2: float = Field(..., ge=-5.0, le=5.0,
                            description="Protein2 marker level (-5.0 to 5.0)")
    Protein3: float = Field(..., ge=-5.0, le=5.0,
                            description="Protein3 marker level (-5.0 to 5.0)")
    Protein4: float = Field(..., ge=-5.0, le=5.0,
                            description="Protein4 marker level (-5.0 to 5.0)")
    Tumour_Stage: str = Field(..., description="Tumour stage (I, II, or III)")
    Histology: str = Field(..., description="Type of cancer histology")
    ER_status: str = Field(..., alias="ER status",
                           description="ER status (Positive or Negative)")
    PR_status: str = Field(..., alias="PR status",
                           description="PR status (Positive or Negative)")
    HER2_status: str = Field(..., alias="HER2 status",
                             description="HER2 status (Positive or Negative)")
    Surgery_type: str = Field(..., description="Type of surgery performed")

    @field_validator('Gender')
    @classmethod
    def validate_gender(cls, v: str) -> str:
        allowed = ['MALE', 'FEMALE', 'Male', 'Female', 'male', 'female']
        if v.upper() not in [g.upper() for g in allowed]:
            raise ValueError(f"Gender must be one of: {allowed}")
        return v.upper()

    @field_validator('Tumour_Stage')
    @classmethod
    def validate_tumour_stage(cls, v: str) -> str:
        allowed = ['I', 'II', 'III']
        if v.upper() not in allowed:
            raise ValueError(f"Tumour_Stage must be one of: {allowed}")
        return v.upper()

    @field_validator('ER_status', 'PR_status', 'HER2_status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = ['Positive', 'Negative', 'positive',
                   'negative', 'POSITIVE', 'NEGATIVE']
        if v not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return v.capitalize()

    def to_model_dict(self) -> dict:
        """Convert to dictionary with model-expected field names"""
        data = self.model_dump(by_alias=False)
        # Map field names to match model expectations
        data['ER status'] = data.pop('ER_status')
        data['PR status'] = data.pop('PR_status')
        data['HER2 status'] = data.pop('HER2_status')
        return data

    model_config = ConfigDict(populate_by_name=True)


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predicted_days: float = Field(...,
                                  description="Predicted survival time in days")
    predicted_months: float = Field(...,
                                    description="Predicted survival time in months")
    predicted_years: float = Field(...,
                                   description="Predicted survival time in years")
    risk_category: str = Field(..., description="Risk category classification")
    risk_color: str = Field(..., description="Risk color indicator")
    recommendation: str = Field(..., description="Clinical recommendation")


def predict_survival(patient_data: dict) -> dict:
    """
    Predict survival time for a breast cancer patient

    Parameters:
    -----------
    patient_data : dict
        Dictionary containing patient features

    Returns:
    --------
    dict : Prediction results
    """
    # Create DataFrame
    df = pd.DataFrame([patient_data])

    # Ensure all required features are present
    for feature in metadata['features']:
        if feature not in df.columns:
            df[feature] = 0

    # Encode categorical features
    for col, le in label_encoders.items():
        if col in df.columns:
            try:
                df[col] = le.transform(df[col].astype(str))
            except ValueError:
                # Unknown category - use first known class
                df[col] = 0

    # Reorder columns
    df = df[metadata['features']]

    # Scale features
    df_scaled = scaler.transform(df)

    # Predict
    predicted_days = model.predict(df_scaled)[0]
    predicted_months = predicted_days / 30
    predicted_years = predicted_days / 365

    # Risk stratification
    if predicted_days < 180:  # Less than 6 months
        risk = "HIGH RISK"
        color = "🔴"
        action = "Immediate intensive care and close monitoring required"
    elif predicted_days < 365:  # 6-12 months
        risk = "ELEVATED RISK"
        color = "🟠"
        action = "Enhanced monitoring and aggressive treatment recommended"
    elif predicted_days < 730:  # 1-2 years
        risk = "MODERATE RISK"
        color = "🟡"
        action = "Standard treatment protocol with regular follow-ups"
    else:  # More than 2 years
        risk = "LOWER RISK"
        color = "🟢"
        action = "Standard care with routine monitoring"

    return {
        'predicted_days': round(predicted_days, 0),
        'predicted_months': round(predicted_months, 1),
        'predicted_years': round(predicted_years, 2),
        'risk_category': risk,
        'risk_color': color,
        'recommendation': action
    }


# API Endpoints
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Breast Cancer Survival Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "mission": "Transform breast cancer care in Africa with AI and community support"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_name": metadata.get('model_name', 'Unknown'),
        "test_r2": metadata.get('test_r2', 0),
        "test_rmse": metadata.get('test_rmse', 0)
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(patient_data: PatientData):
    """
    Predict breast cancer patient survival time

    Accepts patient data and returns survival prediction with risk stratification
    """
    try:
        # Convert Pydantic model to dict with correct field names
        patient_dict = patient_data.to_model_dict()

        # Make prediction
        result = predict_survival(patient_dict)

        return PredictionResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction error: {str(e)}") from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
