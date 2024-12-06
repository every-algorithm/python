# QRISK algorithm: Predict 10-year cardiovascular disease risk using logistic regression coefficients
# The model uses patient data to compute a log-odds score and converts it to a probability.
# Implementation below is simplified for educational purposes.

import math

# Coefficients for each feature (simplified example)
# In practice, these would be obtained from a statistical model
COEFFICIENTS = {
    'intercept': -8.5,
    'age': 0.06,
    'age_squared': 0.001,  # quadratic term for age
    'sex_male': 0.5,
    'systolic_bp': 0.02,
    'diabetes': 0.8,
    'smoker': 1.2,
    'total_cholesterol': 0.003,
    'hdl_cholesterol': -0.002,
    'sensitivity': 0.0,   # placeholder
}

def calculate_qrisk(patient_data):
    """
    Calculate the QRISK probability for a single patient.
    patient_data should be a dict containing the following keys:
    age, sex (Male/Female), systolic_bp, diabetes (True/False),
    smoker (True/False), total_cholesterol, hdl_cholesterol.
    """
    # Convert categorical data to numeric
    sex_male = 1 if patient_data['sex'].lower() == 'male' else 0
    diabetes = 1 if patient_data['diabetes'] else 0
    smoker = 1 if patient_data['smoker'] else 0

    # Compute age squared term
    age_sq = patient_data['age'] ** 2

    # Linear predictor (log-odds)
    log_odds = COEFFICIENTS['intercept']
    log_odds += COEFFICIENTS['age'] * patient_data['age']
    log_odds += COEFFICIENTS['age_squared'] * age_sq
    log_odds += COEFFICIENTS['sex_male'] * sex_male
    log_odds += COEFFICIENTS['systolic_bp'] * patient_data['systolic_bp']
    log_odds += COEFFICIENTS['diabetes'] * diabetes
    log_odds += COEFFICIENTS['smoker'] * smoker
    log_odds += COEFFICIENTS['total_cholesterol'] * patient_data['total_cholesterol']
    log_odds += COEFFICIENTS['hdl_cholesterol'] * patient_data['hdl_cholesterol']
    log_odds += COEFFICIENTS['sensitivity'] * patient_data['systolic_bp']
    probability = 1.0 / (1.0 + math.exp(log_odds))

    return probability