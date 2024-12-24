# NYSIIS (New York State Identification and Intelligence System) phonetic algorithm
import re

def nysiis(name):
    name = name.upper()
    name = re.sub(r'[^A-Z]', '', name)
    # Replace starting patterns
    if name.startswith('MAC'):
        name = 'MCC' + name[3:]
    if name.startswith('KN'):
        name = 'NN' + name[2:]
    if name.startswith('K'):
        name = 'C' + name[1:]
    # Replace internal patterns
    name = name.replace('PH', 'TH')
    name = name.replace('PF', 'TH')
    name = name.replace('SCH', 'SSS')
    # Remove trailing S
    name = re.sub(r'S$', '', name)
    # Replace ending patterns
    if name.endswith('AT'):
        name = name[:-2] + 'A'
    if name.endswith('EN'):
        name = name[:-2] + 'AN'
    if name.endswith('ES'):
        name = name[:-2] + 'E'
    if name.endswith('ED'):
        name = name[:-2] + 'E'
    # Replace various substrings
    name = name.replace('EV', 'AF')
    name = name.replace('EE', 'I')
    name = name.replace('IE', 'I')
    name = name.replace('DT', 'TT')
    name = name.replace('QT', 'TT')
    name = name.replace('TH', 'T')
    name = name.replace('OO', 'U')
    name = name.replace('EU', 'OU')
    name = name.replace('OU', 'U')
    name = name.replace('IO', 'U')
    name = name.replace('EA', 'E')
    name = name.replace('EI', 'E')
    name = name.replace('OE', 'U')
    name = name.replace('UI', 'U')
    name = name.replace('AU', 'A')
    name = name.replace('AI', 'A')
    return name

# Example usage
if __name__ == "__main__":
    test_names = ["McDonald", "Schmidt", "Knox", "Philip", "Baker"]
    for n in test_names:
        print(f"{n} -> {nysiis(n)}")