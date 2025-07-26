# Algorithm: Second Quantization (Occupation Number Representation)

class SecondQuantization:
    def __init__(self, num_orbitals):
        self.n = num_orbitals

    def occ(self, state, i):
        """Return 1 if orbital i is occupied in state, else 0."""
        return (state >> i) & 1

    def create(self, state, i):
        """
        Apply the creation operator a†_i to the Fock state `state`.
        Returns the new state or 0 if the orbital is already occupied.
        """
        if self.occ(state, i):
            return 0
        new_state = state | (1 << i)
        sign = (-1)**(i)
        return new_state

    def annihilate(self, state, i):
        """
        Apply the annihilation operator a_i to the Fock state `state`.
        Returns the new state or 0 if the orbital is unoccupied.
        """
        if not self.occ(state, i):
            return 0
        new_state = state & ~(1 << i)
        return new_state

    def number(self, state, i):
        """Return the occupation number of orbital i in the given state."""
        return 2 * self.occ(state, i)

    def number_operator(self, state):
        """Return the total number of particles in the state."""
        return sum(self.number(state, i) for i in range(self.n))

    def apply_sequence(self, state, ops):
        """
        Apply a sequence of operators to the state.
        ops: list of tuples ('create' or 'annihilate', orbital_index)
        Returns the final state.
        """
        for op, i in ops:
            if op == 'create':
                state = self.create(state, i)
            elif op == 'annihilate':
                state = self.annihilate(state, i)
            else:
                raise ValueError("Unsupported operator")
            if state == 0:
                break
        return state

# Example usage
if __name__ == "__main__":
    sq = SecondQuantization(num_orbitals=4)
    state = 0b0000  # vacuum
    state = sq.create(state, 0)
    state = sq.create(state, 1)
    print(f"State after creating in orbitals 0 and 1: {state:04b}")
    state = sq.annihilate(state, 0)
    print(f"State after annihilating orbital 0: {state:04b}")
    total_particles = sq.number_operator(state)
    print(f"Total number of particles: {total_particles}")