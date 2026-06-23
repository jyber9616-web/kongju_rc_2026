import datetime

from a01_hello import main as hello_main #a01파일의 메인을 hello_main으로 불러옴


def main():
    hello_main()
    now = datetime.datetime.now()

    if 9 < now.hour < 12:
        print(f"현재 시각은 {now.hour}로 오전입니다.")
    elif now.hour < 9:
        print(f"현재 시각은 {now.hour}로 새벽입니다.")
    else:
        print(f"현재시각은 {now.hour}로 오후입니다.")

    print(now.month, type(now.month))

    if 1 <= now.month <= 3:
        print(f"현재 계절은 {now.month}로 겨울이다.")
    elif 4 <= now.month <= 5:
        print(f"현재 계절은 {now.month}로 봄이다.")
    elif 6 <= now.month <= 8:
        print(f"현재 계절은 {now.month}로 여름이다.")
    elif 9 <= now.month <11:
        print(f"현재 계절은 {now.month}로 가을이다.")
    else:
        print(f"현재 계절은 {now.month}로 겨울이다.")
    #봄, 여름, 가을, 겨울을 출력하라
    #12,1,2,3:겨울/ 4,5:봄 / 6,7,8:여름 / 9,10,11:가을

    if now.month in [12, 1, 2, 3]:
        print("겨울")
    elif now.month in [4,5]:
        print("봄")
    elif now.month in [6,7, 8]:
        print("여름")
    else:
        print("가을")
if __name__ == "__main__":
    main()
