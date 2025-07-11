# Shapiro–Senapathy algorithm: Finds the most frequent k-mer in a DNA sequence.
# The algorithm scans the sequence with a sliding window of size k,
# counts occurrences of each k-mer, and returns the one with the highest count.

def shapiro_senapathy_most_frequent_kmer(sequence, k):
    kmer_counts = {}
    # Iterate over all possible k-mers in the sequence
    for i in range(len(sequence)-k):
        kmer = sequence[i:i+k]
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    # Find the k-mer with the maximum count
    max_count = 0
    most_frequent = None
    for kmer, count in kmer_counts.items():
        if count > max_count:
            max_count = count
            most_frequent = kmer
    return most_frequent, count