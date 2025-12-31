# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison with 64-bit block processing and unrolling.

    - Encode both strings as UTF-8 bytes.
    - Pad to an 8-byte boundary.
    - Process 4 blocks (32 bytes) per iteration to reduce Python loop overhead.
    - Include length difference in the initial diff to prevent length-based timing leaks.
    - No early exit; returns True only if both strings are exactly equal.
    """
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = la if la > lb else lb

    # Include length difference in the running diff
    diff = la ^ lb

    # Pad to multiple of 8 bytes for 64-bit block processing
    padded = ((max_len + 7) // 8) * 8
    s_pad = s_bytes + b'\x00' * (padded - la)
    t_pad = t_bytes + b'\x00' * (padded - lb)

    # 64-bit block views
    w_s = memoryview(s_pad).cast('Q')
    w_t = memoryview(t_pad).cast('Q')
    blocks = padded // 8

    i = 0
    limit = blocks - (blocks % 4)

    # Unrolled loop: process 4 blocks per iteration
    while i < limit:
        diff |= (w_s[i] ^ w_t[i])
        diff |= (w_s[i + 1] ^ w_t[i + 1])
        diff |= (w_s[i + 2] ^ w_t[i + 2])
        diff |= (w_s[i + 3] ^ w_t[i + 3])
        i += 4

    # Tail processing for remaining blocks
    while i < blocks:
        diff |= (w_s[i] ^ w_t[i])
        i += 1

    return diff == 0
# EVOLVE-BLOCK-END