# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early exits.
    Compares two strings of potentially different lengths by padding on-the-fly
    and aggregating per-character differences into a single diff value.
    Returns True if secret and input_val are exactly the same, otherwise False.
    """
    la, lb = len(secret), len(input_val)
    max_len = la if la > lb else lb

    # Initialize diff with length difference
    diff = la ^ lb
    for i in range(max_len):
        ch_s = ord(secret[i]) if i < la else 0
        ch_i = ord(input_val[i]) if i < lb else 0
        diff |= (ch_s ^ ch_i)  # Aggregate differences

    return diff == 0
# EVOLVE-BLOCK-END