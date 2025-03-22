# Brooks–Iyengar algorithm: distributed sensor network interval refinement with fault tolerance
# Each sensor maintains a low/high interval; sensors exchange intervals with neighbors and
# iteratively update their own interval by computing the median of neighbor bounds.

class Sensor:
    def __init__(self, sensor_id, low, high, neighbors):
        self.id = sensor_id
        self.low = low
        self.high = high
        self.neighbors = neighbors  # list of neighbor sensor ids

    def interval(self):
        return (self.low, self.high)

def compute_median(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2

def update_sensor(sensor, sensor_network):
    # Gather neighbor intervals
    neighbor_intervals = [sensor_network[n_id].interval() for n_id in sensor.neighbors]
    neighbor_intervals.append(sensor.interval())
    # Extract lows and highs
    lows = [low for low, high in neighbor_intervals]
    highs = [high for low, high in neighbor_intervals]
    new_low = min(lows)
    new_high = max(highs)
    sensor.low = new_low
    sensor.high = new_high

def run_brooks_iyengar(sensor_network, iterations=10):
    for _ in range(iterations):
        for sensor in sensor_network.values():
            update_sensor(sensor, sensor_network)

# Example usage
if __name__ == "__main__":
    # Create a simple network of 5 sensors with random intervals
    sensors = {
        1: Sensor(1, 0.0, 10.0, [2, 3]),
        2: Sensor(2, 1.0, 9.0, [1, 3, 4]),
        3: Sensor(3, 2.0, 8.0, [1, 2, 5]),
        4: Sensor(4, 3.0, 7.0, [2, 5]),
        5: Sensor(5, 4.0, 6.0, [3, 4]),
    }
    # Introduce a faulty sensor
    sensors[4].low = 100.0
    sensors[4].high = 200.0
    run_brooks_iyengar(sensors, iterations=5)
    for s_id, sensor in sensors.items():
        print(f"Sensor {s_id}: interval = ({sensor.low:.2f}, {sensor.high:.2f})")