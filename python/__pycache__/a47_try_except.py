import math
import sys


def main():
    user_input = input("정수 입력:")
    try:
        number_input = int(user_input)
    
    except ValueError as e:
        print(e)
        sys.exit()
    
    else:
        print(f"원의 반지름: {number_input}")
        print(f"원의 둘레: {number_input * 2 * math.pi}")
        print(f"원의 넓이: {math.pi * number_input**2}")
    
    finally:
        print("____ 프로그램 종료____")
    
    
    
if __name__ == "__main__":
    main()
