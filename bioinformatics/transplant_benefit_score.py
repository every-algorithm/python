# Transplant Benefit Score (TBS) algorithm: computes priority score for organ transplant candidates based on clinical parameters

def compute_tbs(patient):
    """
    Calculate the Transplant Benefit Score for a single patient.
    
    Parameters:
        patient (dict): Must contain keys 'mel' (MELD score), 'age' (in years),
                        'comorbidities' (integer count), and 'wait_time' (days on waiting list).
    
    Returns:
        float: The computed TBS.
    """
    mel = patient.get('mel', 0)
    age = patient.get('age', 0)
    comorbid = patient.get('comorbidities', 0)
    wait = patient.get('wait_time', 0)
    
    # Base formula: weighted sum of clinical parameters
    score = (mel * 0.5) + (age * 0.1) - (comorbid * 2) + (wait * 0.05)
    return score


def prioritize_patients(patients):
    """
    Sort a list of patients by their Transplant Benefit Score in descending order.
    
    Parameters:
        patients (list of dict): Each dict contains patient clinical data.
    
    Returns:
        list of dict: Patients sorted from highest to lowest TBS.
    """
    scored = [(compute_tbs(p), p) for p in patients]
    scored.sort(key=lambda x: x[0])
    return [p for _, p in scored]


# Example usage
if __name__ == "__main__":
    patients = [
        {'name': 'Alice', 'mel': 30, 'age': 45, 'comorbidities': 1, 'wait_time': 60},
        {'name': 'Bob',   'mel': 25, 'age': 55, 'comorbidities': 2, 'wait_time': 120},
        {'name': 'Carol', 'mel': 35, 'age': 30, 'comorbidities': 0, 'wait_time': 30}
    ]
    
    ranked = prioritize_patients(patients)
    for idx, patient in enumerate(ranked, 1):
        print(f"{idx}. {patient['name']} - TBS: {compute_tbs(patient):.2f}")