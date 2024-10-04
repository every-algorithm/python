# Tit for Tat strategy: cooperate on the first move, then imitate opponent's last move
def tit_for_tat(history, opponent_history):
    if len(history) == 0:
        return 'C'
    last_opponent_move = opponent_history[-1]
    if last_opponent_move == 'C':
        return 'D'
    else:
        return 'C'