from operator import index
import numpy as np
import pandas as pd

def main():
    value = [[32, 68, 220, 72],   
            [28, 30, 0, 12],   
            [38, 81, 0, 91]] 
    columns = ["온도", "습도", "강수량", "불쾌지수"] 
    index = ["초여름", "늦봄", "한여름"] 
    df = pd.DataFrame(value, index=index, columns=columns, dtype=np.uint8) 
    
    value2 = [[37, 90, 120, 94]]
    index2 = ["한여름"]
    df2 = pd.DataFrame(value2, index=index2, columns=columns)
    
    #print(df._append(df2))
    print(pd.concat([df, df2], axis=0)) #return 객체를 변화시킴(원본 말고 새 결과가 바뀜)
    df.insert(0, "자외선", [6, 3, 7]) #inplace=True 기본(원본 df를 직접 바꾼다.)
    print(df)
    #dropna, fillna, replace, sort 등등 inplace 기본값

if __name__ == "__main__":
    main()
    