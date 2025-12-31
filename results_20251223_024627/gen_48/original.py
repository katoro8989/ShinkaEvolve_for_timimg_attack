# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early exits.
    Compares two strings of potentially different lengths by padding on-the-fly
    and aggregating per-character differences into a single diff value.
    Returns True if secret and input_val are exactly the same, otherwise False.
    """
    # Convert to a uniform byte representation
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = la if la > lb else lb

    # Include length difference as part of the running diff
    diff = la ^ lb

    # Pad to a multiple of 8 bytes for 64-bit block processing
    padded = ((max_len + 7) // 8) * 8
    s_pad = s_bytes + b'\x00' * (padded - la)
    t_pad = t_bytes + b'\x00' * (padded - lb)

    mv_s = memoryview(s_pad)
    mv_t = memoryview(t_pad)

    # Interpret as 64-bit unsigned integers
    w_s = mv_s.cast('Q')
    w_t = mv_t.cast('Q')
    blocks = padded // 8

    for idx in range(blocks):
        diff |= (w_s[idx] ^ w_t[idx])

    return diff == 0
# EVOLVE-BLOCK-END