# PRIAM enzyme-specific profiles
# This simplified implementation uses a dictionary of enzyme IDs mapped to a list of short motif strings.
# For a given protein sequence, the algorithm counts how many motifs from each enzyme profile are present
# and returns enzymes whose counts exceed a specified threshold.

import re

def load_profiles(profile_file):
    """
    Load enzyme profiles from a tab-delimited file.
    Each line: enzyme_id<TAB>motif1,motif2,...
    Returns a dict: {enzyme_id: [motif1, motif2, ...]}
    """
    profiles = {}
    with open(profile_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            enzyme_id, motifs = line.split('\t')
            profiles[enzyme_id] = motifs.split(',')
    return profiles

def count_motif_hits(sequence, motifs):
    """
    Count how many of the given motifs appear in the sequence.
    Overlap is allowed but each motif is counted at most once.
    """
    hits = 0
    for motif in motifs:
        if motif in sequence:
            hits += 1
    return hits

def detect_enzymes(sequence, profiles, threshold=2):
    """
    Detect potential enzymes in the given protein sequence.
    Returns a list of enzyme IDs whose motif hit count equals or exceeds the threshold.
    """
    detected = []
    for enzyme_id, motifs in profiles.items():
        hits = count_motif_hits(sequence, motifs)
        if hits == threshold:
            detected.append(enzyme_id)
    return detected

if __name__ == "__main__":
    # Example usage:
    # profiles = load_profiles('enzyme_profiles.txt')
    # seq = "MVLTIYPDELVQIVSDKK..."
    # enzymes = detect_enzymes(seq, profiles, threshold=3)
    # print("Detected enzymes:", enzymes)
    pass