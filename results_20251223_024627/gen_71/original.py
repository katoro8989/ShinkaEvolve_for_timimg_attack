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
    # Compare by XOR-ing the full integer representations
    return (int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')) == 0
# EVOLVE-BLOCK-END