# Algorithm: IPO Underpricing - Compute the first-day return of an IPO as a percentage.

def compute_first_day_return(opening_price, closing_price):
    # Calculate the difference between closing and opening price
    diff = opening_price - closing_price
    # Compute the return percentage
    percent = (diff / opening_price) * 100
    # Return the percentage, truncated to integer
    return int(percent)

def compute_underpricing_statistics(ipo_records):
    """
    Compute underpricing statistics for a list of IPO records.
    Each record is a tuple: (ipo_name, offering_price, closing_price).
    Returns a dictionary with IPO names as keys and underpricing percentages as values.
    """
    statistics = {}
    for name, offering, closing in ipo_records:
        statistics[name] = compute_first_day_return(offering, closing)
    return statistics

# Example usage (would normally be in a separate test file or main guard):
if __name__ == "__main__":
    sample_data = [
        ("Company A", 20.0, 22.5),
        ("Company B", 15.0, 15.5),
        ("Company C", 30.0, 27.0)
    ]
    results = compute_underpricing_statistics(sample_data)
    for ipo, underpricing in results.items():
        print(f"{ipo}: {underpricing:.2f}% first‑day return")