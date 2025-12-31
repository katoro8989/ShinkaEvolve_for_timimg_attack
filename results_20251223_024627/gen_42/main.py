# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison with a small cross-over optimization.

    - Encodes both strings as UTF-8 bytes.
    - If lengths are equal and a multiple of 8, compare using 64-bit blocks directly.
    - Otherwise, pad both byte sequences to a multiple of 8 and compare in 64-bit blocks.
    - No early exit; all blocks are processed to prevent timing variations.
    - The result is True iff secret and input_val are exactly the same.
    """
    # Convert to a uniform byte representation
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = la if la > lb else lb

    # Include length difference as part of the running diff
    diff = la ^ lb

    # Fast path: if equal lengths and multiple of 8, use 64-bit block view directly
    if la == lb and la != 0 and la % 8 == 0:
        w_s = memoryview(s_bytes).cast('Q')
        w_t = memoryview(t_bytes).cast('Q')
        blocks = la // 8
        for i in range(blocks):
            diff |= (w_s[i] ^ w_t[i])
        return diff == 0

    # General path: pad to a multiple of 8 bytes for 64-bit block processing
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