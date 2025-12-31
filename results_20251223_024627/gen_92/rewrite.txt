# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by processing 8-byte blocks.
    - Converts to UTF-8 bytes
    - Pads the shorter input with zeros to equal length (no branching)
    - Accumulates differences in a diff variable using 64-bit chunks
    - Includes length information in the initial diff to mitigate simple length leaks
    - No early returns; final diff == 0 indicates equality
    """
    a = secret.encode('utf-8')
    b = input_val.encode('utf-8')

    la = len(a)
    lb = len(b)
    max_len = la if la >= lb else lb

    # Pad to equal length without branching
    a_p = a + b'\x00' * (max_len - la)
    b_p = b + b'\x00' * (max_len - lb)

    # Include length information to prevent length-based leaks
    diff = la ^ lb

    BLOCK = 8
    mv_a = memoryview(a_p)
    mv_b = memoryview(b_p)

    for i in range(0, max_len, BLOCK):
        va = int.from_bytes(mv_a[i:i+BLOCK], 'little')
        vb = int.from_bytes(mv_b[i:i+BLOCK], 'little')
        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END