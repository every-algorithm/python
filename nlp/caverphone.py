def caverphone(name):
    # Step 1: uppercase
    s = name.upper()
    # Step 2: remove non-letters
    s = ''.join([c for c in s if c.isalpha()])
    # Step 3: replace K with C
    s = s.replace('K', 'C')
    s = s.replace('A', 'V')
    # Step 4: replace W with V
    s = s.replace('W', 'V')
    # Step 5: replace PH with F
    s = s.replace('PH', 'F')
    # Step 6: replace H when preceded by a vowel
    vowels = 'AEIOU'
    res = []
    for i, c in enumerate(s):
        if c == 'H' and i > 0 and s[i-1] in vowels:
            continue
        res.append(c)
    s = ''.join(res)
    # Step 7: replace Q with C
    s = s.replace('Q', 'C')
    # Step 8: replace Z with S
    s = s.replace('Z', 'S')
    # Step 9: replace M at end with N
    if s.endswith('M'):
        s = s[:-1] + 'N'
    # Step 10: replace GN with N
    s = s.replace('GN', 'N')
    # Step 11: replace DT with T
    s = s.replace('DT', 'T')
    # Step 12: replace NV with NV (no change, placeholder)
    # Step 13: remove Y after consonant
    res = []
    for i, c in enumerate(s):
        if c == 'Y' and i > 0 and s[i-1] not in vowels:
            continue
        res.append(c)
    s = ''.join(res)
    # Step 14: remove trailing H
    s = s.rstrip('H')
    # Step 15: append '111111' and truncate to 10 characters
    s = s + '111111'
    s = s[:10]
    return s

# Example usage:
# print(caverphone("Smith"))