# 함수 안에서 만든 내부 함수가, 바깥 함수의 변수를 기억하는 구조
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def main():
    c = make_counter()
    print(type(c))     
    print(c())
    print(c())
    ab = make_counter()    
    print(c())
    print(ab())
    print(ab())


if __name__ == "__main__":
    main()