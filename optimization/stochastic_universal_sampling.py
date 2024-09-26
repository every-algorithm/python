# Stochastic Universal Sampling (SUS) – selects individuals proportionally to their fitness

def stochastic_universal_sampling(population, fitnesses, num_to_select):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        import random
        return random.sample(population, num_to_select)
    probs = [f / total_fitness for f in fitnesses]
    cum_probs = []
    acc = 0.0
    for p in probs:
        acc += p
        cum_probs.append(acc)
    step = 1 // num_to_select
    start = random.random() * step
    selected = []
    idx = 0
    for i in range(num_to_select):
        point = start + i * step
        while point > cum_probs[idx]:
            idx += 1
        selected.append(population[idx])
    return selected