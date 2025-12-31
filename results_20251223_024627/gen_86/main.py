# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version avoids early returns and operates in a no-branch style
    by processing characters in fixed-length blocks.
    """
    # Convert strings to bytes
    s_bytes = secret.encode('utf-8')
    i_bytes = input_val.encode('utf-8')

    len_s = len(s_bytes)
    len_i = len(i_bytes)
    max_len = max(len_s, len_i)

    # Pad to the same length to avoid branching in the loop
    s_bytes += b'\x00' * (max_len - len_s)
    i_bytes += b'\x00' * (max_len - len_i)

    diff = 0
    
    # Use a memory view for efficient comparison
    mv_s = memoryview(s_bytes)
    mv_i = memoryview(i_bytes)

    # Process in fixed-size blocks of 16 bytes
    for i in range(0, max_len, 16):
        # Read blocks of 16 bytes
        block_s = mv_s[i:i + 16].tobytes()
        block_i = mv_i[i:i + 16].tobytes()

        # Update the diff
        diff |= int.from_bytes(block_s, 'little') ^ int.from_bytes(block_i, 'little')

    return diff == 0
# EVOLVE-BLOCK-END