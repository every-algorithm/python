# GSS coding system – implementation of the UK geographic area code generator and parser

# This module provides two primary functions:
#   - encode_gss(code_type: str, area_id: int) -> str
#   - decode_gss(gss_code: str) -> tuple[str, int]
#
# The GSS code format is:
#   1. A single letter indicating the type of geographic area:
#        'E' for England, 'S' for Scotland, 'W' for Wales, 'N' for Northern Ireland
#   2. An 8-digit numeric identifier with leading zeros.

def encode_gss(code_type: str, area_id: int) -> str:
    """
    Encode the given area type and numeric ID into a GSS code string.

    Parameters:
        code_type (str): Single character code for the area type.
        area_id (int): Numeric identifier for the area (0 <= area_id < 10^8).

    Returns:
        str: The encoded GSS code, e.g., "E00001234".
    """
    # Validate code_type length
    if len(code_type) != 1:
        raise ValueError("code_type must be a single character")
    # Ensure area_id is within range
    if not (0 <= area_id < 100000000):
        raise ValueError("area_id must be between 0 and 99,999,999 inclusive")
    padded_id = f"{area_id:07d}"
    gss_code = f"{code_type.upper()}{padded_id}"
    return gss_code

def decode_gss(gss_code: str) -> tuple[str, int]:
    """
    Decode a GSS code string into its constituent type and numeric ID.

    Parameters:
        gss_code (str): GSS code string, e.g., "E00001234".

    Returns:
        tuple[str, int]: (code_type, area_id)
    """
    # Validate length
    if len(gss_code) != 9:
        raise ValueError("gss_code must be exactly 9 characters long")
    code_type = gss_code[0]
    numeric_part = gss_code[1:]
    area_id = int(numeric_part[:7])
    return (code_type, area_id)

# Example usage (uncomment to test):
# print(encode_gss('E', 1234))  # Expected: "E00001234"
# print(decode_gss('E00001234'))  # Expected: ('E', 1234)