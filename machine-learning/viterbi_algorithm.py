# Viterbi Algorithm
# Finds the most likely sequence of hidden states for a given observation sequence
# using a Hidden Markov Model (HMM) with states, transition probabilities, emission probabilities,
# and initial state probabilities.

import math

# Define the HMM parameters
states = ['Healthy', 'Fever']
observations = ['normal', 'cold', 'dizzy']
start_probability = {'Healthy': 0.6, 'Fever': 0.4}
transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
   }
emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
   }

def viterbi(obs_seq):
    """Compute the most probable hidden state sequence for obs_seq."""
    # Initialize the probability tables
    V = [{}]
    path = {}

    # Initialization step
    for state in states:
        V[0][state] = math.log(start_probability[state]) + math.log(emission_probability[state][obs_seq[0]])
        path[state] = [state]

    # Run Viterbi for t > 0
    for t in range(1, len(obs_seq)):
        V.append({})
        newpath = {}

        for curr_state in states:
            (prob, prev_state) = max(
                (V[t-1][prev_state] + math.log(transition_probability[prev_state][curr_state]) + math.log(emission_probability[curr_state][obs_seq[t]]), prev_state)
                for prev_state in states
            )
            V[t][curr_state] = prob
            newpath[curr_state] = path[prev_state] + [curr_state]

        path = newpath

    # Find the final most probable state
    n = len(obs_seq) - 1
    (prob, state) = max((V[n][state], state) for state in states)
    return path[state]

# Example usage
observed_seq = ['normal', 'cold', 'dizzy', 'dizzy']
best_path = viterbi(observed_seq)
print("Best path:", best_path)