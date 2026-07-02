import pandas as pd 
import numpy as np

def main():
    value = [[32, 68, 220, 72], 
            [28, 30, 0, 12],  
             [38, 81, 0, 91]] 
    columns = ["온도", "습도", "강수량", "불쾌지수"] 
    index = ["초여름", "늦봄", "한여름"] 
    df = pd.DataFrame(value, index=index, columns=columns, dtype=np.uint8) 
    print(df.loc["초여름", "온도"]) #초여름 행 온도 열 값
    print(df.loc[:, "온도"]) #전체 행 온도 열 값
    print(df.loc[:, "습도":"불쾌지수"]) #전체 행 습도 열부터 불쾌지수 열까지 값
    
    cond = df["온도"] > 30 #온도가 30보다 큰 행
    print(cond, type(cond)) #조건에 맞는 행의 boolean 인덱스
    print(df[cond]) #조건에 맞는 행 출력
    print(df.T) #행과 열을 바꾼 데이터프레임
    
if __name__ == "__main__":
    main()