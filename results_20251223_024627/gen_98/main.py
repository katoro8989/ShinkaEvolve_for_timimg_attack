# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Cross-over: combines non-branching diff accumulator with utf-32-le block processing.
    - Encodes to utf-32-le and processes 4-byte chunks.
    - Pads shorter input with zeros to avoid data-dependent branches.
    - Returns True only if strings are exactly equal (same length and content).
    """
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')
    max_units = max(len(secret), len(input_val))  # number of 4-byte units
    diff = len(secret) ^ len(input_val)  # incorporate length difference

    for i in range(max_units):
        base = i * 4
        # 4-byte chunk from a
        ca = a[base:base+4]
        if len(ca) < 4:
            ca = ca + b'\x00' * (4 - len(ca))
        va = int.from_bytes(ca, 'little')

        # 4-byte chunk from b
        cb = b[base:base+4]
        if len(cb) < 4:
            cb = cb + b'\x00' * (4 - len(cb))
        vb = int.from_bytes(cb, 'little')

        diff |= (va ^ vb)

    return diff == 0
# EVOLVE-BLOCK-END