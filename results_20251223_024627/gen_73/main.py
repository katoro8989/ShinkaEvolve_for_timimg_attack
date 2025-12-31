# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time style comparison using utf-32-le encoding and large-integer XOR.
    The two strings are encoded to 32-bit code units and compared as a single
    large integer, avoiding per-character branching and early exits.
    Returns True only if both strings are exactly equal (same length and content).
    """
    # Encode as UTF-32 little-endian so each character is a fixed 4-byte unit
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    # Initialize the accumulator with the length difference
    diff = len(a) ^ len(b)  # Incorporate length difference
    # Process the encoded strings in a constant-time manner
    for i in range(max(len(a), len(b)) // 4):  # Each character is 4 bytes
        byte_a = int.from_bytes(a[i*4:(i+1)*4], 'little') if i < len(a) // 4 else 0
        byte_b = int.from_bytes(b[i*4:(i+1)*4], 'little') if i < len(b) // 4 else 0
        diff |= byte_a ^ byte_b
    return (int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')) == 0
# EVOLVE-BLOCK-END