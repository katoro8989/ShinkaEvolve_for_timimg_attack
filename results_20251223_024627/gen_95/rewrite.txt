# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings using fixed-block XOR over UTF-8 bytes.
    - Encodes to UTF-8, pads shorter input with zeros to equal length (no branching).
    - Processes in fixed-size blocks to minimize timing variance.
    - Includes length information in initial diff to reduce leaks.
    - No early returns; final diff indicates equality.
    """
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Initialize diff with length information
    diff = len1 ^ len2

    # Pad to equal length (no branching inside the loop)
    if max_len > len1:
        b1 = b1 + b'\x00' * (max_len - len1)
    if max_len > len2:
        b2 = b2 + b'\x00' * (max_len - len2)

    # Process in fixed-size blocks
    BLOCK = 32
    for i in range(0, max_len, BLOCK):
        chunk1 = b1[i:i+BLOCK]
        chunk2 = b2[i:i+BLOCK]
        diff |= int.from_bytes(chunk1, 'little') ^ int.from_bytes(chunk2, 'little')

    return diff == 0
# EVOLVE-BLOCK-END