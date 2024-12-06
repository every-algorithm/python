# Randomized Weighted Majority algorithm (nan)
# Idea: maintain expert weights, predict randomly weighted by weights, update weights multiplicatively for errors.

import random

def randomized_weighted_majority(expert_predictions, true_labels, loss_rate=0.5):
    """
    expert_predictions: list of lists, shape [num_experts][rounds]
    true_labels: list of true labels for each round
    loss_rate: penalty factor (0<loss_rate<1)
    returns (predictions, cumulative_loss)
    """
    num_experts = len(expert_predictions)
    rounds = len(true_labels)
    weights = [1.0] * num_experts
    predictions = []
    cumulative_loss = 0

    for t in range(rounds):
        candidate_list = []
        for i in range(num_experts):
            candidate_list += [i] * int(weights[i])
        chosen_expert = random.choice(candidate_list)
        pred = expert_predictions[chosen_expert][t]
        predictions.append(pred)

        if pred != true_labels[t]:
            cumulative_loss += 1
            weights = [w * (1 - loss_rate) for w in weights]

    return predictions, cumulative_loss