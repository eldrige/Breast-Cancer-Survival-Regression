# 🎗️ Breast Cancer Survival Prediction - ML Summative Assessment

## Mission & Problem

Breast cancer is a leading cause of mortality among women in Africa, with limited access to advanced diagnostic tools and specialized healthcare. This project addresses the critical need for accessible, AI-powered survival prediction tools that can support healthcare providers in resource-limited settings. By leveraging machine learning models trained on clinical and pathological data, we enable early risk stratification and personalized treatment recommendations. Our solution transforms complex medical data into actionable insights, empowering healthcare workers to make informed decisions and improve patient outcomes across the continent.

---

## 🌐 Public API Endpoint

**API Base URL:** `https://breast-cancer-survival-regression.onrender.com`  
**Swagger UI Documentation:** `https://breast-cancer-survival-regression.onrender.com/docs`

The API provides a publicly accessible endpoint for breast cancer survival predictions. All endpoints are fully documented and testable through the interactive Swagger UI interface.

### Key Endpoints:

- **POST `/predict`** - Predict survival time for breast cancer patients
- **GET `/health`** - Health check and model status
- **GET `/docs`** - Interactive Swagger UI documentation

### Example API Request:

```json
POST https://breast-cancer-survival-regression.onrender.com/predict
Content-Type: application/json

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

**Note:** The API is publicly accessible and ready for testing via Swagger UI at the link above.

---

## 📹 Video Demo

**YouTube Demo Link:** [https://jam.dev/c/6bac75c9-ddc2-4817-9e9f-91a2631bbca8](https://jam.dev/c/6bac75c9-ddc2-4817-9e9f-91a2631bbca8) (Hosted on Jam.dev)

The video demonstration covers:

- Project overview and mission
- API functionality via Swagger UI
- Mobile app features and user interface
- End-to-end prediction workflow

---

## 📱 Running the Mobile App

The mobile application is built with Flutter and provides an intuitive interface for breast cancer survival predictions.

### Prerequisites

1. **Flutter SDK** (version 3.9.0 or higher)

   ```bash
   flutter --version
   ```

2. **Android Studio** or **Xcode** (for iOS development)

   - Android Studio: For Android development
   - Xcode: For iOS development (macOS only)

3. **Device or Emulator**
   - Android: Android emulator or physical device
   - iOS: iOS Simulator or physical device (macOS only)

### Installation Steps

1. **Navigate to the mobile app directory:**

   ```bash
   cd predictor
   ```

2. **Install Flutter dependencies:**

   ```bash
   flutter pub get
   ```

3. **Update API Configuration:**

   Open `predictor/lib/main.dart` and update the API base URL:

   ```dart
   // Line 6: Update this with your deployed API URL
   const String apiBaseUrl = 'https://breast-cancer-survival-regression.onrender.com';
   ```

   **Important:** The API URL is already configured, but you can verify it matches the deployed endpoint.

4. **Run the app:**

   **For Android:**

   ```bash
   flutter run
   ```

   **For iOS (macOS only):**

   ```bash
   flutter run -d ios
   ```

   **For a specific device:**

   ```bash
   flutter devices  # List available devices
   flutter run -d <device-id>
   ```

### Building for Production

**Android APK:**

```bash
flutter build apk --release
```

**iOS (macOS only):**

```bash
flutter build ios --release
```

### Troubleshooting

- **API Connection Errors:** Ensure the API URL in `main.dart` is correct and the API is publicly accessible
- **Dependencies Issues:** Run `flutter pub get` again
- **Build Errors:** Ensure you have the latest Flutter SDK and all required platform tools installed

---

## 📁 Project Structure

```
ml-summative/
│
├── README.md                          # Main project documentation (this file)
│
├── linear-regression/                 # Machine Learning Model Training
│   ├── README.md                      # Detailed ML pipeline documentation
│   ├── breast_cancer_training.ipynb   # Jupyter notebook for model training
│   ├── predict_survival.py            # Standalone prediction script
│   ├── breast_cancer_survival.csv     # Training dataset
│   │
│   ├── Generated Model Files:
│   ├── best_breast_cancer_model.pkl   # Trained model (Random Forest)
│   ├── scaler.pkl                     # Feature scaler
│   ├── label_encoders.pkl             # Categorical encoders
│   ├── model_metadata.json            # Model metadata and performance metrics
│   │
│   └── Visualizations/                # Training visualizations
│       ├── 01_survival_distribution.png
│       ├── 02_categorical_distributions.png
│       ├── 03_protein_distributions.png
│       ├── 04_correlation_matrix.png
│       ├── 05_age_stage_survival.png
│       ├── 06_feature_importance.png
│       ├── 06_loss_curve.png
│       ├── 07_before_after_scatter.png
│       └── 07_model_comparison.png
│
├── fast-api/                          # FastAPI Backend Service
│   ├── README.md                      # API documentation
│   ├── main.py                        # FastAPI application
│   ├── requirements.txt               # Python dependencies
│   └── runtime.txt                    # Python runtime version
│
└── predictor/                         # Flutter Mobile Application
    ├── README.md                      # Mobile app documentation
    ├── lib/
    │   └── main.dart                  # Main Flutter application code
    ├── pubspec.yaml                   # Flutter dependencies
    ├── android/                       # Android platform files
    ├── ios/                           # iOS platform files
    ├── web/                           # Web platform files
    ├── macos/                         # macOS platform files
    ├── linux/                         # Linux platform files
    └── windows/                       # Windows platform files
```

### Directory Descriptions

#### `linear-regression/`

Contains the complete machine learning pipeline:

- **Training Scripts:** Jupyter notebook and Python scripts for model development
- **Model Files:** Serialized models, scalers, and encoders for deployment
- **Visualizations:** Data analysis and model performance charts
- **Documentation:** Detailed methodology and results

#### `fast-api/`

RESTful API service built with FastAPI:

- **main.py:** API endpoints, request validation, and prediction logic
- **Deployment Ready:** Configured for cloud deployment (Render, Heroku, etc.)
- **Swagger UI:** Automatic interactive API documentation
- **CORS Enabled:** Supports cross-origin requests from web/mobile clients

#### `predictor/`

Cross-platform Flutter mobile application:

- **lib/main.dart:** Complete UI implementation with form validation
- **Platform Support:** Android, iOS, Web, Desktop (Windows, macOS, Linux)
- **API Integration:** HTTP client for prediction requests
- **User Experience:** Intuitive forms, result visualization, and error handling

---

## 🔗 Additional Resources

- **Linear Regression Documentation:** See `linear-regression/README.md` for detailed ML methodology
- **API Documentation:** See `fast-api/README.md` for API usage and deployment instructions
- **Mobile App Documentation:** See `predictor/README.md` for Flutter-specific details

---

## 🎯 Quick Start

1. **Test the API:** Visit [Swagger UI](https://breast-cancer-survival-regression.onrender.com/docs) to test predictions
2. **Update Mobile App:** Verify API URL in `predictor/lib/main.dart` is set to `https://breast-cancer-survival-regression.onrender.com`
3. **Run Mobile App:** Follow instructions above
4. **Make Predictions:** Use either the Swagger UI or mobile app to predict survival times

---

**Mission:** Transform breast cancer care in Africa with AI and community support.
