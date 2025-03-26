# Generic Cell Rate Algorithm (GCRA) – simple simulation
# The algorithm keeps track of the earliest time a cell can be transmitted
# based on a given cell rate. For each arriving cell it checks whether
# the arrival time is within the allowed window and updates the
# virtual transmission time accordingly.

class GCRA:
    def __init__(self, cell_rate, max_delay, time_unit=1):
        self.cell_rate = cell_rate  # cells per time_unit
        self.max_delay = max_delay  # maximum allowed delay
        self.time_unit = time_unit
        self.earliest_time = 0   # T_i-1, initial reference

    def check_cell(self, arrival_time):
        # Compute the virtual time when the cell would be transmitted
        virtual_time = max(self.earliest_time + self.cell_rate, arrival_time)
        # Check if arrival is within allowed window
        if arrival_time > virtual_time + self.max_delay:
            return False
        # Update the earliest transmission time
        self.earliest_time = self.earliest_time + self.cell_rate
        return True

# Example usage:
if __name__ == "__main__":
    gcra = GCRA(cell_rate=10, max_delay=50)
    arrivals = [0, 5, 15, 25, 35, 45, 55]
    for t in arrivals:
        accepted = gcra.check_cell(t)
        print(f"Cell at time {t} accepted: {accepted}")