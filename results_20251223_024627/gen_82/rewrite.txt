# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison by processing UTF-32-le code units in 4-byte blocks.
    Pads the shorter string to equal length and XORs corresponding 32-bit blocks.
    No early exits; returns True only if all blocks are identical and lengths match.
    """
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')

    len_a_units = len(a) // 4
    len_b_units = len(b) // 4

    max_units = max(len_a_units, len_b_units)

    # Pad to equal number of 4-byte units
    if len_a_units < max_units:
        a += b'\x00' * (4 * (max_units - len_a_units))
    if len_b_units < max_units:
        b += b'\x00' * (4 * (max_units - len_b_units))

    diff = (len_a_units ^ len_b_units)

    for i in range(max_units):
        base = i * 4
        va = int.from_bytes(a[base:base+4], 'little')
        vb = int.from_bytes(b[base:base+4], 'little')
        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END