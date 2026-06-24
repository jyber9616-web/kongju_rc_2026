def main():
    tu = tuple()
    print(tu, type(tu))
    tu = (1, 2) #원소 추가 제거 변경이 안된다.
    print(tu, type(tu))
    print(tu[0])
    for ele in tu:
        print(ele) #list하고 같은 기능을 가진 컨테이너
    #system 내부적으로 안정적으로 데이터를 전달하기 위해서
    tu_1 = 1, 2
    print(tu_1, type(tu_1))
    a = 10
    b = 20
    # swap C 스타일
    tmp = a
    a = b
    b = tmp
    print(a, b)
    # swap python 스타일
    a, b = b, a
    print(a, b)

    
        
        
if __name__ == "__main__":
    main()