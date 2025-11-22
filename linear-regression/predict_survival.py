"""
BREAST CANCER SURVIVAL PREDICTION SCRIPT
Uses the trained best model to predict patient survival times

Dataset: Breast Cancer Survival Dataset
Source: https://www.kaggle.com/datasets/kreeshrajani/breast-cancer-survival-dataset

This script:
1. Loads the saved best model
2. Accepts new patient data
3. Makes survival predictions (in days)
4. Provides risk stratification

Mission: Transform breast cancer care in Africa with AI and community support
"""

import pandas as pd
import numpy as np
import joblib
import json

# ============================================================================
# LOAD MODEL AND PREPROCESSING COMPONENTS
# ============================================================================

print("="*80)
print("BREAST CANCER SURVIVAL PREDICTION SYSTEM")
print("Mission: Transform breast cancer care in Africa with AI")
print("="*80)

print("\n[1] Loading trained model and components...")

try:
    model = joblib.load('best_breast_cancer_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoders = joblib.load('label_encoders.pkl')

    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)

    print("✓ All components loaded successfully!")
    print(f"\n   Model: {metadata['model_name']}")
    print(f"   Test R²: {metadata['test_r2']:.4f}")
    print(f"   Test RMSE: {metadata['test_rmse']:.2f} days")
    print(f"   Features: {len(metadata['features'])}")

except FileNotFoundError as e:
    print(f"\n❌ Error: {e}")
    print("Please run the training script first!")
    exit()

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================


def predict_survival(patient_data):
    """
    Predict survival time for a breast cancer patient

    Parameters:
    -----------
    patient_data : dict
        Dictionary containing patient features:
        - Age: Patient age in years
        - Gender: MALE or FEMALE
        - Protein1, Protein2, Protein3, Protein4: Protein marker levels
        - Tumour_Stage: I, II, or III
        - Histology: Type of cancer
        - ER status: Positive or Negative
        - PR status: Positive or Negative
        - HER2 status: Positive or Negative
        - Surgery_type: Type of surgery performed

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

# ============================================================================
# EXAMPLE PREDICTIONS
# ============================================================================


print("\n" + "="*80)
print("[2] EXAMPLE PREDICTIONS")
print("="*80)

# Example 1: Higher risk profile
print("\n" + "─"*60)
print("PATIENT 1: Higher Risk Profile")
print("─"*60)

patient1 = {
    'Age': 68,
    'Gender': 'FEMALE',
    'Protein1': -0.5,
    'Protein2': 0.8,
    'Protein3': 0.2,
    'Protein4': -0.3,
    'Tumour_Stage': 'III',
    'Histology': 'Infiltrating Ductal Carcinoma',
    'ER status': 'Negative',
    'PR status': 'Negative',
    'HER2 status': 'Positive',
    'Surgery_type': 'Mastectomy'
}

print("\nPatient Data:")
for key, value in patient1.items():
    print(f"   {key}: {value}")

result1 = predict_survival(patient1)

print(f"\n{result1['risk_color']} PREDICTION RESULTS:")
print(f"   Predicted Survival: {result1['predicted_days']:.0f} days")
print(
    f"                       ({result1['predicted_months']:.1f} months / {result1['predicted_years']:.2f} years)")
print(f"   Risk Category: {result1['risk_category']}")
print(f"   Recommendation: {result1['recommendation']}")

# Example 2: Moderate risk profile
print("\n" + "─"*60)
print("PATIENT 2: Moderate Risk Profile")
print("─"*60)

patient2 = {
    'Age': 52,
    'Gender': 'FEMALE',
    'Protein1': 0.5,
    'Protein2': 1.2,
    'Protein3': -0.1,
    'Protein4': 0.05,
    'Tumour_Stage': 'II',
    'Histology': 'Infiltrating Ductal Carcinoma',
    'ER status': 'Positive',
    'PR status': 'Positive',
    'HER2 status': 'Negative',
    'Surgery_type': 'Lumpectomy'
}

print("\nPatient Data:")
for key, value in patient2.items():
    print(f"   {key}: {value}")

result2 = predict_survival(patient2)

print(f"\n{result2['risk_color']} PREDICTION RESULTS:")
print(f"   Predicted Survival: {result2['predicted_days']:.0f} days")
print(
    f"                       ({result2['predicted_months']:.1f} months / {result2['predicted_years']:.2f} years)")
print(f"   Risk Category: {result2['risk_category']}")
print(f"   Recommendation: {result2['recommendation']}")

# Example 3: Lower risk profile
print("\n" + "─"*60)
print("PATIENT 3: Lower Risk Profile")
print("─"*60)

patient3 = {
    'Age': 42,
    'Gender': 'FEMALE',
    'Protein1': 0.95,
    'Protein2': 2.15,
    'Protein3': 0.008,
    'Protein4': -0.05,
    'Tumour_Stage': 'I',
    'Histology': 'Infiltrating Lobular Carcinoma',
    'ER status': 'Positive',
    'PR status': 'Positive',
    'HER2 status': 'Negative',
    'Surgery_type': 'Other'
}

print("\nPatient Data:")
for key, value in patient3.items():
    print(f"   {key}: {value}")

result3 = predict_survival(patient3)

print(f"\n{result3['risk_color']} PREDICTION RESULTS:")
print(f"   Predicted Survival: {result3['predicted_days']:.0f} days")
print(
    f"                       ({result3['predicted_months']:.1f} months / {result3['predicted_years']:.2f} years)")
print(f"   Risk Category: {result3['risk_category']}")
print(f"   Recommendation: {result3['recommendation']}")

# ============================================================================
# INTERACTIVE PREDICTION MODE
# ============================================================================


def interactive_mode():
    """Interactive prediction with user input"""

    print("\n" + "="*80)
    print("[3] INTERACTIVE PREDICTION MODE")
    print("="*80)
    print("\nEnter patient information (press Enter for defaults shown in brackets):\n")

    try:
        patient = {}

        age = input("Age [50]: ").strip()
        patient['Age'] = int(age) if age else 50

        patient['Gender'] = 'FEMALE'  # Default for breast cancer

        p1 = input("Protein1 level [0.5]: ").strip()
        patient['Protein1'] = float(p1) if p1 else 0.5

        p2 = input("Protein2 level [1.0]: ").strip()
        patient['Protein2'] = float(p2) if p2 else 1.0

        p3 = input("Protein3 level [0.0]: ").strip()
        patient['Protein3'] = float(p3) if p3 else 0.0

        p4 = input("Protein4 level [0.0]: ").strip()
        patient['Protein4'] = float(p4) if p4 else 0.0

        stage = input("Tumour Stage (I/II/III) [II]: ").strip()
        patient['Tumour_Stage'] = stage if stage in [
            'I', 'II', 'III'] else 'II'

        print("\nHistology options:")
        print("  1. Infiltrating Ductal Carcinoma")
        print("  2. Infiltrating Lobular Carcinoma")
        print("  3. Mucinous Carcinoma")
        hist = input("Select histology (1/2/3) [1]: ").strip()
        histology_map = {
            '1': 'Infiltrating Ductal Carcinoma',
            '2': 'Infiltrating Lobular Carcinoma',
            '3': 'Mucinous Carcinoma'
        }
        patient['Histology'] = histology_map.get(
            hist, 'Infiltrating Ductal Carcinoma')

        er = input("ER status (Positive/Negative) [Positive]: ").strip()
        patient['ER status'] = er if er in [
            'Positive', 'Negative'] else 'Positive'

        pr = input("PR status (Positive/Negative) [Positive]: ").strip()
        patient['PR status'] = pr if pr in [
            'Positive', 'Negative'] else 'Positive'

        her2 = input("HER2 status (Positive/Negative) [Negative]: ").strip()
        patient['HER2 status'] = her2 if her2 in [
            'Positive', 'Negative'] else 'Negative'

        print("\nSurgery options:")
        print("  1. Lumpectomy")
        print("  2. Mastectomy")
        print("  3. Modified Radical Mastectomy")
        print("  4. Other")
        surg = input("Select surgery type (1/2/3/4) [1]: ").strip()
        surgery_map = {
            '1': 'Lumpectomy',
            '2': 'Mastectomy',
            '3': 'Modified Radical Mastectomy',
            '4': 'Other'
        }
        patient['Surgery_type'] = surgery_map.get(surg, 'Lumpectomy')

        # Make prediction
        result = predict_survival(patient)

        print("\n" + "─"*60)
        print("PREDICTION RESULTS")
        print("─"*60)
        print(
            f"\n{result['risk_color']} Risk Category: {result['risk_category']}")
        print(f"\n   Predicted Survival Time:")
        print(f"      • {result['predicted_days']:.0f} days")
        print(f"      • {result['predicted_months']:.1f} months")
        print(f"      • {result['predicted_years']:.2f} years")
        print(f"\n   Clinical Recommendation:")
        print(f"      {result['recommendation']}")

    except KeyboardInterrupt:
        print("\n\nPrediction cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

# ============================================================================
# BATCH PREDICTION
# ============================================================================


def batch_predict(csv_file):
    """Predict survival for multiple patients from CSV"""

    print("\n" + "="*80)
    print("[4] BATCH PREDICTION MODE")
    print("="*80)

    try:
        df = pd.read_csv(csv_file)
        print(f"\n✓ Loaded {len(df)} patients from '{csv_file}'")

        results = []
        for idx, row in df.iterrows():
            patient = row.to_dict()
            result = predict_survival(patient)
            results.append({
                'Patient_ID': idx + 1,
                'Predicted_Days': result['predicted_days'],
                'Predicted_Months': result['predicted_months'],
                'Risk_Category': result['risk_category'],
                'Recommendation': result['recommendation']
            })

        results_df = pd.DataFrame(results)
        output_file = 'batch_predictions.csv'
        results_df.to_csv(output_file, index=False)

        print(f"\n✓ Predictions saved to '{output_file}'")
        print("\nResults Summary:")
        print(results_df.to_string(index=False))

        print("\nRisk Distribution:")
        risk_counts = results_df['Risk_Category'].value_counts()
        for risk, count in risk_counts.items():
            pct = count / len(results_df) * 100
            print(f"   {risk}: {count} patients ({pct:.1f}%)")

    except FileNotFoundError:
        print(f"\n❌ File '{csv_file}' not found.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

# ============================================================================
# MAIN MENU
# ============================================================================


def main():
    """Main menu for prediction modes"""

    print("\n" + "="*80)
    print("PREDICTION OPTIONS")
    print("="*80)
    print("""
    1. View example predictions (shown above)
    2. Interactive prediction (enter patient data)
    3. Batch prediction (from CSV file)
    4. Exit
    """)

    try:
        choice = input("Select option (1-4): ").strip()

        if choice == '2':
            interactive_mode()
        elif choice == '3':
            csv_file = input("\nEnter CSV file path: ").strip()
            batch_predict(csv_file)
        elif choice == '4':
            print("\nThank you for using the prediction system!")
        else:
            print("\nExample predictions shown above.")

    except KeyboardInterrupt:
        print("\n\nExiting...")

# ============================================================================
# CLINICAL APPLICATION INFO
# ============================================================================


print("\n" + "="*80)
print("CLINICAL APPLICATION FOR AFRICA")
print("="*80)
print("""
This AI prediction system supports breast cancer care by:

🏥 CLINICAL DECISION SUPPORT
   • Risk stratification for treatment prioritization
   • Survival estimation for care planning
   • Resource allocation optimization

👥 COMMUNITY HEALTH IMPACT
   • Identifies patients needing intensive support
   • Enables targeted community health worker visits
   • Supports family counseling and preparation

📊 FEATURES USED FOR PREDICTION
   • Patient demographics (Age)
   • Protein biomarkers (Protein1-4)
   • Cancer characteristics (Stage, Histology)
   • Hormone receptor status (ER, PR, HER2)
   • Treatment information (Surgery type)

⚠️  IMPORTANT LIMITATIONS
   • Predictions are estimates based on population data
   • Individual outcomes may vary significantly
   • Should complement, not replace, clinical judgment
   • Model should be validated on local African populations
""")

print("="*80)
print("Ready for predictions!")
print("="*80)

if __name__ == "__main__":
    main()
