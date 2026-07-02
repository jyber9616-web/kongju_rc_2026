import numpy as np
import pandas as pd

def main():
    arr = np.array([10, 20, 30], dtype=np.int8)
    sr = pd.Series(arr)
    print(sr, type(sr))
    
    value = [32, 68, 220, 72]
    index = ["온도", "습도", "강수량", "불쾌지수"]
    sr2 = pd.Series(value, index=index)
    print(sr2)
    print(sr2["온도"], sr2[0])
    
if __name__ == "__main__":
    main()