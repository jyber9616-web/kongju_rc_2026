import datetime

def main():
    ptime = datetime.datetime.now()
    list_a = [0,1,2,3,4,5,6]
    list_b = ["a","b","c","d","e","f", ptime]
    del list_a[0] #객체를 지우는 키워드
    del list_b[2]
    del list_b[5]
    print(list_a)
    print(list_b)
    ''' del(ptime)
    print(ptime) 
    del list_a #heap에 있는 메모리 공간이 삭제
    print(list_a) '''

    print(list_b.pop())
    print(list_b)

    list_b.remove("d")
    print(list_b)


if __name__ == "__main__":
    main()