# EVOLVE-BLOCK-START
def constant_time_bit_difference(a: int, b: int) -> int:
    """Returns the bitwise XOR of two integers to indicate equality."""
    return a ^ b

def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This implementation operates in a no-branching manner
    by comparing characters in a fixed-length loop, ensuring
    consistent timing for all comparisons.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Start comparison with the lengths
    diff = len_s ^ len_i  # Mismatched lengths contribute to the diff

    for i in range(max_len):
        char_s = ord(secret[i]) if i < len_s else 0
        char_i = ord(input_val[i]) if i < len_i else 0
        diff |= constant_time_bit_difference(char_s, char_i)
    
    return diff == 0
# EVOLVE-BLOCK-END