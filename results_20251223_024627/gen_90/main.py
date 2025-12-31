# EVOLVE-BLOCK-START
def _utf32le_units(s: str):
    """
    Convert a Python string to a tuple of 32-bit code units (utf-32-le).
    Each character becomes one 32-bit integer. The length matches the original
    string length in characters.
    """
    # Each character is encoded as 4 bytes in utf-32-le
    data = s.encode('utf-32-le')
    # Number of 4-byte units equals the number of characters
    n = len(s)
    units = []
    for i in range(n):
        # 4 bytes per unit
        start = i * 4
        units.append(int.from_bytes(data[start:start+4], 'little'))
    return tuple(units)

def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    - Uses utf-32-le encoding and 32-bit blockwise XOR.
    - Processes the maximum length of the two inputs in fixed iterations.
    - Pads shorter input with zeros to avoid data-dependent branches.
    - No early returns; final diff == 0 implies equality.
    """
    a_units = _utf32le_units(secret)
    b_units = _utf32le_units(input_val)

    max_len = max(len(a_units), len(b_units))

    diff = 0
    for i in range(max_len):
        va = a_units[i] if i < len(a_units) else 0
        vb = b_units[i] if i < len(b_units) else 0
        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END