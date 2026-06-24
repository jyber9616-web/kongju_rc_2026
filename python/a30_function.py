def print_hello(a : str):

    for i in range(a):
        print("안녕하세요", i)
    return "execution OK!"
    
def main():
    re = print_hello(3, "hi")
    print(re)
    


if __name__ == "__main__":
    main()