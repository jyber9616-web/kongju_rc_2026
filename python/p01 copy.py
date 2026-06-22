def main():
    product_name = input("상품명을 입력하세요: ")

    try:
        price = float(input("상품 가격을 입력하세요: "))
        discount_rate = float(input("할인율(%)을 입력하세요: "))

        discount_amount = price * discount_rate / 100
        final_price = price - discount_amount

        print("\n===== 상품 할인 정보 =====")
        print(f"상품명: {product_name}")
        print(f"원래 가격: {price:,.0f}원")
        print(f"할인율: {discount_rate}%")
        print(f"할인 금액: {discount_amount:,.0f}원")
        print(f"최종 가격: {final_price:,.0f}원")

    except ValueError:
        print("가격과 할인율은 숫자로 입력해야 합니다.")


if __name__ == "__main__":
    main()

'''
1교시: ot
2교시: wsl설치, vscode 설치 및 설문
3교시: git 연동, github 계정 만들기, github repository 만들기
4교시: python 기초 강의
5교시: print 함수 해석
6교시: 변수와 자료형
7교시: 연산자와 표현식, input 함수 해석
8교시: 문자열 f-string, format
'''