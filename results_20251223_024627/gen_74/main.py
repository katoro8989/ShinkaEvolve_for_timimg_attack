# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time style comparison using UTF-32 LE encoding with blockwise XOR.
    - Encodes strings into fixed 32-bit code units.
    - Iterates over the maximum number of units, padding with zeros as needed.
    - Accumulates differences in a single diff variable without branches.
    - Returns True only if strings are exactly equal (same length and content).
    """
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    max_len = max(len(a), len(b))

    diff = 0
    for i in range(0, max_len, 4):
        va = int.from_bytes(a[i:i+4].ljust(4, b'\x00'), 'little')
        vb = int.from_bytes(b[i:i+4].ljust(4, b'\x00'), 'little')
        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END