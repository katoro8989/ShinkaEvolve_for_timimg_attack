# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Function to determine if two strings match.
    Currently contains a typical 'timing vulnerability'.
    Returns False immediately if even one character differs,
    resulting in different execution times when the error is at the beginning versus the end.
    """
    if len(secret) != len(input_val):
        return False

    for i in range(len(secret)):
        # Vulnerability point: exits immediately upon finding a mismatch
        if secret[i] != input_val[i]:
            return False
            
    return True
# EVOLVE-BLOCK-END