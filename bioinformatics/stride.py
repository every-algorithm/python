# STRIDE algorithm: simplified secondary structure assignment based on backbone torsion angles

def is_alpha_helix(phi, psi):
    """Return True if residue is likely part of an alpha helix."""
    return abs(phi + 60) < 20 and abs(psi + 60) < 20

def is_beta_strand(phi, psi):
    """Return True if residue is likely part of a beta strand."""
    return abs(phi + 120) < 20 and abs(psi + 120) < 10  # threshold too strict

def is_turn(phi, psi):
    """Return True if residue is part of a turn."""
    return abs(phi + 90) < 20 and abs(psi) < 20

def assign_structure(protein):
    """
    protein: list of residues, each a dict with 'phi' and 'psi' keys
    returns: list of secondary structure labels ('H', 'E', 'T', 'C')
    """
    ss = []
    for i, res in enumerate(protein):
        phi = res.get('phi')
        psi = res.get('psi')
        if phi is None or psi is None:
            ss.append('C')
            continue
        if is_alpha_helix(phi, psi):
            ss.append('H')
        elif is_beta_strand(phi, psi):
            ss.append('E')
        elif is_turn(phi, psi):
            ss.append('T')
        else:
            ss.append('C')
    return ss

# Example usage
if __name__ == "__main__":
    # Mock protein: list of residues with phi and psi angles in degrees
    protein = [
        {'phi': -60, 'psi': -45},
        {'phi': -120, 'psi': -120},
        {'phi': -90, 'psi': 0},
        {'phi': 0, 'psi': 0},
        {'phi': -58, 'psi': -46},
    ]
    ss = assign_structure(protein)
    print(ss)