def test():
    print("함수 호출")
    yield "re"

def main():
    ge = test() #함수의 실행이 매번 다른 결과를 요구할때 사용
    print(ge)   #일련의 과정이 결정되어서 연속적으로 일을 수행할때
    '''print(ge.__next__())
    print(next(ge))
    print(next(ge))'''
    
if __name__ == "__main__":
    main()