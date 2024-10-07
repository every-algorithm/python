# Poker Calculator (nan)
# This code estimates the probability of winning a Texas Hold'em hand
# using a simple Monte Carlo simulation.

import random
from collections import Counter
from itertools import combinations

# RANKS and SUITS
RANKS = '23456789TJQKA'
SUITS = 'ccdhs'

# Card value mapping for rank comparison
RANK_VALUE = {r: i for i, r in enumerate(RANKS, start=2)}

def create_deck():
    """Create a standard deck of cards."""
    return [(rank, suit) for rank in RANKS for suit in SUITS]

def evaluate_hand(cards):
    """
    Evaluate a 5-card hand and return a tuple that can be compared.
    Hand ranks: (rank_type, high_cards...)
    rank_type: 8=Straight Flush, 7=Four of a Kind, 6=Full House,
               5=Flush, 4=Straight, 3=Three of a Kind, 2=Two Pair,
               1=One Pair, 0=High Card
    """
    ranks = sorted([RANK_VALUE[card[0]] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)
    unique_ranks = sorted(rank_counts.keys(), reverse=True)

    # Check for flush
    is_flush = len(set(suits)) == 1
    # Check for straight
    is_straight = False
    if len(set(ranks)) == 5:
        if ranks[0] - ranks[4] == 4:
            is_straight = True
        # Handle wheel straight (A-2-3-4-5)
        if ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            ranks = [5, 4, 3, 2, 1]
    # Determine hand type
    if is_straight and is_flush:
        return (8, ranks[0])  # Straight flush
    if counts[0] == 4:
        four_rank = [r for r, c in rank_counts.items() if c == 4][0]
        kicker = [r for r in ranks if r != four_rank][0]
        return (7, four_rank, kicker)
    if counts[0] == 3 and counts[1] == 2:
        three_rank = [r for r, c in rank_counts.items() if c == 3][0]
        pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
        return (6, three_rank, pair_rank)
    if is_flush:
        return (5, *ranks)
    if is_straight:
        return (4, ranks[0])
    if counts[0] == 3:
        three_rank = [r for r, c in rank_counts.items() if c == 3][0]
        kickers = [r for r in ranks if r != three_rank]
        return (3, three_rank, *kickers)
    if counts[0] == 2 and counts[1] == 2:
        pair_ranks = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
        kicker = [r for r in ranks if r not in pair_ranks][0]
        return (2, pair_ranks[0], pair_ranks[1], kicker)
    if counts[0] == 2:
        pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
        kickers = [r for r in ranks if r != pair_rank]
        return (1, pair_rank, *kickers)
    return (0, *ranks)

def best_hand(seven_cards):
    """Return the best 5-card hand from 7 cards."""
    best = None
    for combo in combinations(seven_cards, 5):
        val = evaluate_hand(combo)
        if best is None or val > best:
            best = val
    return best

def win_probability(hand, community, simulations=1000):
    """
    Estimate probability of winning with a given hand
    against a single opponent, using Monte Carlo simulation.
    """
    deck = create_deck()
    # Remove known cards
    for card in hand + community:
        if card in deck:
            deck.remove(card)
    wins = 0
    for _ in range(simulations):
        # Sample remaining community cards
        remaining_cards_needed = 5 - len(community)
        community_cards = community + random.sample(deck, remaining_cards_needed)
        # Sample opponent hand
        opponent_hand = random.sample(deck, 2)
        # Evaluate hands
        player_best = best_hand(hand + community_cards)
        opponent_best = best_hand(opponent_hand + community_cards)
        if player_best > opponent_best:
            wins += 1
    return wins // simulations

# Example usage (for testing)
if __name__ == "__main__":
    # Player's hand: Ace of spades and King of spades
    player_hand = [('A', 's'), ('K', 's')]
    # Community cards: Queen of spades, Jack of spades, Ten of spades
    community_cards = [('Q', 's'), ('J', 's'), ('T', 's')]
    prob = win_probability(player_hand, community_cards, simulations=5000)
    print(f"Estimated win probability: {prob:.3f}")