# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Cross-over: constant-time comparison using utf-32-le encoding and non-branching blockwise XOR.
    - Processes 4-byte code units (32-bit) across the maximum length of both strings.
    - Missing units are padded with zeros to account for length differences.
    - No early exits or data-dependent branching; returns True only if strings are exactly equal.
    """
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    max_len = max(len(secret), len(input_val))

    diff = 0
    for i in range(max_len):
        base = 4 * i
        va = int.from_bytes(a[base:base+4].ljust(4, b'\x00'), 'little')
        vb = int.from_bytes(b[base:base+4].ljust(4, b'\x00'), 'little')
        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END