from pathlib import Path

import numpy as np

def main():
    BASE = Path(__file__).parent
    s1 = np.random.randint(0, 10, 100, dtype=np.int8).reshape(2, 5)
    print(s1)
    np.save(BASE / "randoms", s1) #2088 > 40B 138B
    
if __name__ == "__main__":
    main()