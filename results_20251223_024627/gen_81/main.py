# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version processes the strings as UTF-32 encoded bytes to ensure a fixed length
    for each character and avoids early exits or branching based on character comparisons.
    Returns True only if both strings are exactly equal (same length and content).
    """
    # Encode as UTF-32 little-endian
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    
    # Initialize the accumulator with the length difference
    diff = len(a) ^ len(b)  # Incorporate length difference
    
    # Compare each byte in constant time
    for i in range(max(len(a), len(b))):
        byte_a = a[i] if i < len(a) else 0
        byte_b = b[i] if i < len(b) else 0
        diff |= byte_a ^ byte_b
    
    return diff == 0
# EVOLVE-BLOCK-END