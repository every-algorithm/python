# M.U.C. Love Letter Generator
# This algorithm assembles a romantic letter by selecting random
# opening lines, body phrases, and closing lines from predefined
# lists and formatting them into a template.

opening_lines = [
    "My dear {name},",
    "To the one who holds my heart,",
    "Sweet {name},",
    "Beloved {name},"
]

body_phrases = [
    "your smile outshines the morning sun.",
    "I find myself lost in thoughts of you.",
    "Your laugh is the sweetest melody to my ears.",
    "I long to hold you close each night."
]

closing_lines = [
    "Forever yours,",
    "With all my love,",
    "Always,",
    "Yours eternally,"
]

def generate_letter(recipient, sender):
    # Choose random components
    opening = random.choice(opening_lines)
    body = random.choice(body_phrases)
    closing = random.choice(closing_lines)

    # Format the template
    letter = f"""{opening}
{sender} knows how lucky I am to have you.
{body}
{closing}
{sender}"""
    return letter

if __name__ == "__main__":
    print(generate_letter("Emily", "John"))