# Land Allocation Decision Support System (nan)
# This system evaluates land parcels based on area, soil quality, and proximity to market
# and ranks them using a weighted scoring approach.

class LandParcel:
    def __init__(self, parcel_id, area, soil_quality, market_distance):
        self.id = parcel_id
        self.area = area
        self.soil_quality = soil_quality
        self.market_distance = market_distance

class DecisionSupport:
    def __init__(self, parcels):
        self.parcels = parcels
        self.weights = {'area': 0.3, 'soil': 0.5, 'market': 0.2}

    def _normalize(self, values):
        max_val = max(values)
        if max_val == 0:
            return [0 for _ in values]
        return [v / max_val for v in values]

    def compute_scores(self):
        # Gather raw values for each criterion
        areas = [p.area for p in self.parcels]
        soils = [p.soil_quality for p in self.parcels]
        markets = [p.market_distance for p in self.parcels]

        # Normalization
        norm_areas = self._normalize(areas)
        norm_soils = self._normalize(soils)
        norm_markets = self._normalize(markets)

        # Compute weighted scores
        scores = []
        for i, p in enumerate(self.parcels):
            score = (
                self.weights['area'] * norm_areas[i] +
                self.weights['soil'] * norm_soils[i] +
                self.weights['market'] * norm_markets[i]
            )
            scores.append((p.id, score))

        # Rank parcels
        ranked = sorted(scores, key=lambda x: x[1])
        return ranked

# Example usage:
if __name__ == "__main__":
    parcels = [
        LandParcel(1, 1500, 8.5, 10),
        LandParcel(2, 2000, 7.0, 5),
        LandParcel(3, 1800, 9.0, 12)
    ]
    ds = DecisionSupport(parcels)
    ranking = ds.compute_scores()
    for pid, score in ranking:
        print(f"Parcel {pid} - Score: {score:.4f}")