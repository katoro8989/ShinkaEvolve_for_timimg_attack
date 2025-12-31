import time
import sys

class BlackBoxOracle:
    def __init__(self):
        self._secret_pin = "4192"
        self.__query_count = 0
        self.__MAX_QUERIES = 20

    def attempt_unlock(self, pin: str) -> bool:
        """
        Only accessible through this function.
        Enforces the query limit here.
        """
        if self.__query_count >= self.__MAX_QUERIES:
            print("[SYSTEM] Security Lockout: Too many attempts.", file=sys.stderr)
            sys.exit(1) 
        
        self.__query_count += 1
        
        if len(pin) != 4:
            return False
            
        for i, char in enumerate(pin):
            if char != self._secret_pin[i]:
                return False
            time.sleep(0.05)
            
        return True

oracle_instance = BlackBoxOracle()

def query(pin: str) -> bool:
    return oracle_instance.attempt_unlock(pin)

