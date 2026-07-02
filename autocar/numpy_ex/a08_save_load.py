from pathlib import Path

import numpy as np

def main():
    BASE = Path(__file__).parent
    s1 = np.load(BASE / "randoms.npy")
    print(s1)
    
if __name__ == "__main__":
    main()