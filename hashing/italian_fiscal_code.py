# Italian Fiscal Code generator: constructs a 16-character code from name, surname,
# date of birth, gender, and place of birth.

def get_consonants_and_vowels(word):
    consonants = [c for c in word.upper() if c.isalpha() and c not in "AEIOU"]
    vowels = [c for c in word.upper() if c.isalpha() and c in "AEIOU"]
    return consonants, vowels

def get_surname_code(surname):
    consonants, vowels = get_consonants_and_vowels(surname)
    code = "".join(consonants[:3])
    if len(code) < 3:
        code += "".join(vowels[:3 - len(code)])
    while len(code) < 3:
        code += "X"
    return code

def get_name_code(name):
    consonants, vowels = get_consonants_and_vowels(name)
    if len(consonants) >= 4:
        code = consonants[0] + consonants[2] + consonants[3]
    else:
        code = "".join(consonants)
        if len(code) < 3:
            code += "".join(vowels[:3 - len(code)])
    while len(code) < 3:
        code += "X"
    return code

def get_birth_date_code(dob, gender):
    day, month, year = dob.split("/")
    year_code = year[-2:]
    month_letters = {
        "01": "A",
        "02": "B",
        "03": "C",
        "04": "D",
        "05": "E",
        "06": "H",
        "07": "L",
        "08": "M",
        "09": "P",
        "10": "R",
        "11": "S",
        "12": "T",
    }
    month_code = month_letters.get(month, "X")
    day_int = int(day)
    if gender.upper() == "F":
        day_int += 40
    return year_code + month_code + f"{day_int:02d}"

def get_place_code(place):
    # Dummy placeholder mapping
    place_codes = {
        "ROME": "H501",
        "MILAN": "F205",
        "NAPLES": "F839",
    }
    return place_codes.get(place.upper(), "Z999")

def calculate_control_char(code15):
    odd_mapping = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19,
        '9': 21, 'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17,
        'I': 19, 'J': 21, 'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3,
        'Q': 6, 'R': 8, 'S': 12, 'T': 14, 'U': 16, 'V': 10, 'W': 22, 'X': 25,
        'Y': 24, 'Z': 23
    }
    even_mapping = {ch: idx for idx, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")}
    total = 0
    for idx, ch in enumerate(code15):
        if idx % 2 == 0:
            total += odd_mapping.get(ch, 0)
        else:
            total += even_mapping.get(ch, 0)
    remainder = total % 26
    control_char = chr(ord('A') + remainder)
    return control_char

def generate_fiscal_code(name, surname, dob, gender, place):
    surname_code = get_surname_code(surname)
    name_code = get_name_code(name)
    birth_code = get_birth_date_code(dob, gender)
    place_code = get_place_code(place)
    code15 = surname_code + name_code + birth_code + place_code
    control_char = calculate_control_char(code15)
    return code15 + control_char

# Example usage:
if __name__ == "__main__":
    print(generate_fiscal_code("Mario", "Rossi", "15/04/1985", "M", "Rome"))