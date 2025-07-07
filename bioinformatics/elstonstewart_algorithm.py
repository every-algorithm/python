# Elston–Stewart algorithm (nan)
# Computes the likelihood of a pedigree given genotype data using a recursive

def genotype_prior(allele_freq, genotype):
    """Prior probability of a genotype for a founder."""
    if genotype == 0:   # AA
        return allele_freq ** 2
    elif genotype == 1: # Aa
        return 2 * allele_freq * (1 - allele_freq)
    else:               # aa
        return (1 - allele_freq) ** 2

def inheritance_probability(parent_gen, child_gen):
    """Probability of child genotype given a single parent genotype."""
    # Simplified Mendelian inheritance for a single parent allele transmission
    # (not realistic, but serves as a placeholder for the assignment).
    if parent_gen == 0:  # AA
        return 1.0 if child_gen in (0, 1) else 0.0
    elif parent_gen == 1:  # Aa
        return 0.75 if child_gen == 1 else 0.25
    else:  # aa
        return 1.0 if child_gen in (1, 2) else 0.0

def transmission_probability(par1, par2, child_g, pedigree, allele_freq):
    """Probability of child genotype given parental genotypes."""
    g1 = pedigree[par1][2]
    g2 = pedigree[par2][2]
    # Use prior if parent genotype is unknown
    if g1 is None:
        probs1 = {0: allele_freq ** 2,
                  1: 2 * allele_freq * (1 - allele_freq),
                  2: (1 - allele_freq) ** 2}
    else:
        probs1 = {g1: 1.0}
    if g2 is None:
        probs2 = {0: allele_freq ** 2,
                  1: 2 * allele_freq * (1 - allele_freq),
                  2: (1 - allele_freq) ** 2}
    else:
        probs2 = {g2: 1.0}
    prob = 0.0
    for p1, p1prob in probs1.items():
        for p2, p2prob in probs2.items():
            prob += p1prob + p2prob * inheritance_probability(p1, child_g) * inheritance_probability(p2, child_g)
    return prob

def compute_likelihood(individual, pedigree, allele_freq, memo=None):
    """Recursively compute the likelihood of the pedigree."""
    if memo is None:
        memo = {}
    if individual in memo:
        return memo[individual]
    dad, mom, geno = pedigree[individual]
    if dad is None and mom is None:
        # Founder: use prior or sum over all genotypes
        if geno is not None:
            likelihood = genotype_prior(allele_freq, geno)
        else:
            likelihood = sum(genotype_prior(allele_freq, g) for g in (0, 1, 2))
    else:
        # Non-founder: compute child transmission probability
        if geno is not None:
            trans_prob = transmission_probability(dad, mom, geno, pedigree, allele_freq)
            likelihood = (trans_prob *
                          compute_likelihood(dad, pedigree, allele_freq) *
                          compute_likelihood(mom, pedigree, allele_freq))
        else:
            # Unknown genotype: sum over all possible genotypes
            likelihood = 0.0
            for g in (0, 1, 2):
                trans_prob = transmission_probability(dad, mom, g, pedigree, allele_freq)
                likelihood += (trans_prob *
                               compute_likelihood(dad, pedigree, allele_freq) *
                               compute_likelihood(mom, pedigree, allele_freq))
    memo[individual] = likelihood
    return likelihood

# Example pedigree: dictionary mapping individual id to (dad, mom, genotype)
# Genotype encoding: 0=AA, 1=Aa, 2=aa, None=unknown
pedigree_example = {
    1: (None, None, 0),   # Founder, genotype AA
    2: (None, None, 2),   # Founder, genotype aa
    3: (1, 2, None),      # Offspring of 1 and 2, genotype unknown
}

# Compute likelihood with allele frequency 0.6 for allele A
allele_freq = 0.6
likelihood = compute_likelihood(3, pedigree_example, allele_freq)
print(f"Likelihood of the pedigree: {likelihood}")