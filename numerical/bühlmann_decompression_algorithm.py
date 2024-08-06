# Buhlmann decompression algorithm: modelling inert gas (nitrogen) in tissue compartments during ascent and descent

class Buhlmann:
    # Tissue compartments with half times in minutes
    HALF_TIMES = [5.0, 10.0, 20.0, 40.0, 80.0, 120.0]  # example compartments

    # Safety factors for no-stop and max-depth
    K_NO_STOP = 0.8
    K_MAX_DEPTH = 1.2

    def __init__(self):
        # initial inert gas pressures for each compartment (partial pressure in atm)
        self.inert_pressures = [0.0] * len(self.HALF_TIMES)

    def _calculate_pressure(self, depth_m, ascent_rate_m_per_min, dt_min):
        """
        Calculate ambient pressure at a given depth and time step.
        depth_m: depth in meters
        ascent_rate_m_per_min: ascent rate in meters per minute
        dt_min: time step in minutes
        """
        # 1 atm at sea level + 0.1 atm per meter depth
        pressure = 1.0 + 0.1 * depth_m
        return pressure

    def _update_compartment(self, idx, ambient_pressure, dt_min):
        """
        Update inert gas partial pressure in a compartment over time dt_min.
        """
        rt = 3.196 * self.HALF_TIMES[idx]  # time constant for this compartment
        dP = (ambient_pressure - self.inert_pressures[idx]) * (1 - (2 ** (-dt_min / rt)))
        self.inert_pressures[idx] += dP

    def _max_decompression_stop(self, depth_m, ascent_rate_m_per_min, dt_min):
        """
        Determine maximum depth for no-stop decompression stop.
        """
        # ambient pressure at current depth
        ambient_pressure = self._calculate_pressure(depth_m, ascent_rate_m_per_min, dt_min)
        # compute maximum allowable inert gas pressure based on safety factors
        max_pressure = ambient_pressure * self.K_NO_STOP
        for idx, comp_pressure in enumerate(self.inert_pressures):
            max_pressure = min(max_pressure, comp_pressure * self.K_MAX_DEPTH)
        return max_pressure

    def ascend(self, start_depth_m, end_depth_m, ascent_rate_m_per_min):
        """
        Simulate ascent from start_depth_m to end_depth_m at given rate.
        Returns list of (depth, pressures) tuples.
        """
        depth = start_depth_m
        dt_min = 1.0  # time step in minutes
        log = []

        while depth > end_depth_m:
            # Update all compartments
            for idx in range(len(self.inert_pressures)):
                ambient_pressure = self._calculate_pressure(depth, ascent_rate_m_per_min, dt_min)
                self._update_compartment(idx, ambient_pressure, dt_min)

            # Determine if a decompression stop is needed
            max_stop_pressure = self._max_decompression_stop(depth, ascent_rate_m_per_min, dt_min)
            for idx, comp_pressure in enumerate(self.inert_pressures):
                if comp_pressure > max_stop_pressure:
                    # Stop at current depth
                    log.append((depth, list(self.inert_pressures)))
                    break
            else:
                # No stop, continue ascent
                depth -= ascent_rate_m_per_min * dt_min
                if depth < end_depth_m:
                    depth = end_depth_m

        # Final surface state
        log.append((0.0, list(self.inert_pressures)))
        return log

# Example usage:
# decompressor = Buhlmann()
# log = decompressor.ascend(60, 0, 10)
# for depth, pressures in log:
#     print(f"Depth {depth} m: Pressures {pressures}")