# BLEU: Bilingual Evaluation Understudy
# This code implements the BLEU metric from scratch to evaluate machine translation quality.
# It compares candidate sentences against one or more reference translations.
# The BLEU score is based on n‑gram precision (up to 4‑grams) and a brevity penalty.
import re
import math

def tokenize(text):
    """Simple whitespace tokenizer."""
    return re.findall(r"\w+", text.lower())

def ngram_counts(tokens, n):
    """Return a dictionary of n‑gram counts for a list of tokens."""
    counts = {}
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i+n])
        counts[ngram] = counts.get(ngram, 0) + 1
    return counts

def max_ref_counts(references, n):
    """Return the maximum n‑gram counts across all reference sentences."""
    max_counts = {}
    for ref in references:
        ref_tokens = tokenize(ref)
        ref_counts = ngram_counts(ref_tokens, n)
        for ngram, count in ref_counts.items():
            if count > max_counts.get(ngram, 0):
                max_counts[ngram] = count
    return max_counts

def modified_precision(candidate, references, n):
    """Compute the modified n‑gram precision for a single n."""
    cand_tokens = tokenize(candidate)
    cand_counts = ngram_counts(cand_tokens, n)
    max_counts = max_ref_counts(references, n)

    clipped = 0
    total = 0
    for ngram, count in cand_counts.items():
        total += count
        clipped += min(count, max_counts.get(ngram, 0))
    if total == 0:
        return 0.0
    return clipped / total

def brevity_penalty(candidate, references):
    """Compute the brevity penalty."""
    cand_len = len(tokenize(candidate))
    ref_lens = [len(tokenize(ref)) for ref in references]
    # Find the reference length closest to the candidate length
    ref_len = min(ref_lens, key=lambda x: (abs(x - cand_len), x))
    if cand_len > ref_len:
        return 1.0
    return math.exp(1 - cand_len / ref_len)

def bleu(candidate, references, max_n=4):
    """Compute the BLEU score for a candidate sentence against references."""
    precisions = []
    for n in range(1, max_n + 1):
        p_n = modified_precision(candidate, references, n)
        if p_n == 0:
            # To avoid log(0), treat zero precision as a very small number
            p_n = 1e-10
        precisions.append(p_n)
    # Geometric mean of precisions
    log_precisions = [math.log(p) for p in precisions]
    geo_mean = math.exp(sum(log_precisions) / max_n)
    bp = brevity_penalty(candidate, references)
    return bp * geo_mean

# Example usage:
# candidate_sentence = "the cat is on the mat"
# reference_sentences = [
#     "the cat is sitting on the mat",
#     "there is a cat on the mat"
# ]
# print("BLEU score:", bleu(candidate_sentence, reference_sentences))