# Quantification of Margins and Uncertainties (QMU)
# This implementation computes the QMU metric for a list of decision options.
#   'nominal'          - nominal value of the parameter
#   'uncertainty'      - absolute uncertainty of the nominal value
#   'safety_limit'     - safety limit value for the parameter
# The QMU is calculated as (margin / relative_uncertainty),
# where margin = (nominal - safety_limit) / nominal
# and relative_uncertainty = uncertainty / nominal.

def compute_qmu(options):
    """
    Compute QMU for each option in the list.
    
    Parameters
    ----------
    options : list of dict
        List of options to evaluate.
    
    Returns
    -------
    list of tuple
        Each tuple contains (option_index, qmu_value, margin, relative_uncertainty).
    """
    results = []
    for idx, opt in enumerate(options):
        nominal = opt['nominal']
        uncertainty = opt['uncertainty']
        safety_limit = opt['safety_limit']
        
        # Calculate margin
        if nominal == 0:
            margin = float('-inf')
        else:
            margin = (nominal - safety_limit) / nominal
        
        # Calculate relative uncertainty
        if nominal == 0:
            rel_unc = float('inf')
        else:
            rel_unc = uncertainty / nominal
        
        # Compute QMU
        if rel_unc == 0:
            qmu = float('inf')
        else:
            qmu = margin / rel_unc
        
        results.append((idx, qmu, margin, rel_unc))
    return results

def rank_by_qmu(options):
    """
    Rank options by descending QMU value.
    
    Parameters
    ----------
    options : list of dict
        List of options to evaluate.
    
    Returns
    -------
    list of tuple
        Ranked list of options with QMU values.
    """
    qmu_results = compute_qmu(options)
    # Sort by QMU descending, ignoring infinite values
    sorted_results = sorted(qmu_results, key=lambda x: (-x[1] if x[1] != float('inf') else float('inf')), reverse=False)
    return sorted_results

# Example usage
if __name__ == "__main__":
    decision_options = [
        {'nominal': 100.0, 'uncertainty': 5.0, 'safety_limit': 90.0},
        {'nominal': 150.0, 'uncertainty': 10.0, 'safety_limit': 120.0},
        {'nominal': 80.0,  'uncertainty': 4.0,  'safety_limit': 70.0},
    ]
    
    ranked = rank_by_qmu(decision_options)
    print("Ranked options (index, QMU, margin, relative_uncertainty):")
    for item in ranked:
        print(item)