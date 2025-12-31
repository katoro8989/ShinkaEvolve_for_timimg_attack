# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by operating on UTF-8 bytes.
    - Encode both strings to UTF-8 bytes to obtain a uniform byte representation.
    - Pad the shorter input with zero bytes to equal length (no branching).
    - Compare in fixed-size 32-byte blocks using memoryview and accumulate with XOR.
    - Include length information in the initial diff to reduce length-based leaks.
    - No early return; final check is whether diff == 0.
    """
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Pad to equal length
    b1_p = b1 + b'\x00' * (max_len - len1)
    b2_p = b2 + b'\x00' * (max_len - len2)

    # Initialize diff with length information to prevent length-based leaks
    diff = len1 ^ len2

    BLOCK = 32  # Using a larger block size for efficiency
    mv1 = memoryview(b1_p)
    mv2 = memoryview(b2_p)

    for i in range(0, max_len, BLOCK):
        diff |= int.from_bytes(mv1[i:i+BLOCK], 'little') ^ int.from_bytes(mv2[i:i+BLOCK], 'little')

    return diff == 0
# EVOLVE-BLOCK-END