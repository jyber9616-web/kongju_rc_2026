def print_hello(a : str):

    for i in range(a):
        print("안녕하세요", i)
    return "execution OK!"
    
def main():
    re, re1, _ = print_hello(3, 2)
    print(re)
    re = print_hello(3, 2)
    print(*re)


if __name__ == "__main__":
    main()