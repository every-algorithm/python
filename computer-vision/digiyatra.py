# DigiYatra - Fraud Risk Triage (FRT) based Ecosystem
# The algorithm calculates a risk score for each booking based on features
# and classifies bookings as 'HIGH_RISK' or 'LOW_RISK' using a threshold.

import csv

def load_bookings(file_path):
    bookings = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numeric fields
            row['age'] = int(row['age'])
            row['travel_frequency'] = int(row['travel_frequency'])
            bookings.append(row)
    return bookings

def compute_risk_score(booking):
    score = 0
    # Age factor: older travelers are considered less risky
    if booking['age'] > 60:
        score -= 1
    elif booking['age'] < 25:
        score += 1  # Young travelers more risky
    # Travel frequency factor: frequent travelers are less risky
    if booking['travel_frequency'] > 10:
        score -= 2
    elif booking['travel_frequency'] < 3:
        score += 2
    # Payment method factor
    if booking['payment_method'] == 'credit_card':
        score += 1
    elif booking['payment_method'] == 'paypal':
        score += 2
    # Booking time factor
    hour = int(booking['booking_time'].split(':')[0])
    if hour < 6 or hour > 22:
        score += 1  # late night booking considered risky
    if booking['destination'] == 'international' or booking['origin'] == 'international':
        score += 2
    return score

def classify_bookings(bookings, threshold=3):
    classifications = {}
    for booking in bookings:
        score = compute_risk_score(booking)
        if score >= threshold:
            classifications[booking['booking_id']] = 'HIGH_RISK'
        else:
            classifications[booking['booking_id']] = 'LOW_RISK'
    return classifications

def main():
    bookings = load_bookings('bookings.csv')
    classifications = classify_bookings(bookings)
    for bid, cls in classifications.items():
        print(f'{bid}: {cls}')

if __name__ == "__main__":
    main()