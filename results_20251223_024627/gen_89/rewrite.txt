# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison using 64-bit blocks with a non-branching diff.
    - Encode to UTF-8 bytes
    - Pad to 8-byte boundary
    - Seed diff with length XOR
    - Iterate over 64-bit blocks and accumulate XOR differences
    - Return True iff diff == 0
    """
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = la if la >= lb else lb

    # Seed with length difference to help resist length-based timing leaks
    diff = la ^ lb

    # Pad to an 8-byte boundary for 64-bit block processing
    padded = ((max_len + 7) // 8) * 8
    s_pad = s_bytes + b'\x00' * (padded - la)
    t_pad = t_bytes + b'\x00' * (padded - lb)

    # Interpret as 64-bit blocks
    w_s = memoryview(s_pad).cast('Q')
    w_t = memoryview(t_pad).cast('Q')
    blocks = padded // 8

    for i in range(blocks):
        diff |= (w_s[i] ^ w_t[i])

    return diff == 0
# EVOLVE-BLOCK-END