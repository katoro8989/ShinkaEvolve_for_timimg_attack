# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    if len(secret) != len(input_val):
        return False

    for i in range(len(secret)):
        if secret[i] != input_val[i]:
            return False
            
    return True
# EVOLVE-BLOCK-END