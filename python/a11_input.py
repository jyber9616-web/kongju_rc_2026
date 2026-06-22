def main():
    input_var = input("숫자를 입력하세요: ")
    print(input_var, type(input_var))
    '''try:
        print(int(input_var) + 100)
    except ValueError:
        print("다시.")'''
    if input_var.isdigit():
        print(int(input_var) + 100)
    else:
        print("다시.")

    
if __name__ == "__main__":
    main()
    