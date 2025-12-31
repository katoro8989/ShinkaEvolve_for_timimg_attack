# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings using UTF-32 little-endian encoding.
    This function processes both strings in fixed-size blocks to ensure consistent
    timing regardless of mismatches and avoids early returns.
    Returns True only if both strings are exactly equal (same length and content).
    """
    # Encode strings as UTF-32 little-endian
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    
    # Determine the maximum length for comparison
    max_len = max(len(a), len(b))
    
    # Initialize the diff accumulator with length difference
    diff = len(a) ^ len(b)

    # Compare in blocks of 4 bytes
    for i in range(0, max_len, 4):
        # Extract 4-byte blocks, padding with zeros if necessary
        block_a = a[i:i+4] if i < len(a) else b'\x00' * 4
        block_b = b[i:i+4] if i < len(b) else b'\x00' * 4
        
        # Accumulate the differences using XOR
        diff |= int.from_bytes(block_a, 'little') ^ int.from_bytes(block_b, 'little')

    return diff == 0
# EVOLVE-BLOCK-END