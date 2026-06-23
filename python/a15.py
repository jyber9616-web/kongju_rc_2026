def main():
    print( 10 == 100) #false
    print( 10 != 100) #true
    print( 10 < 100) #true
    print( 100 <= 100) #true
    print(type(True))

    print(not True) #false
    print(not False) #true
    print(True and True) #true
    print(False or False) #False

    a = int(input("100보다 큰 숫자를 입력:"))

    if a > 100:
        print("a는 100보다 크다")
    print("프로그램 종료")


if __name__ == "__main__":
    main()
    