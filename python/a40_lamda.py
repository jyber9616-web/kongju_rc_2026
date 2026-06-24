def power(item):
    return item * item

def uner_3(item):
    return item < 3 #3보다 작으면 true

def main():
    li = [ 1, 2, 3, 4, 5]
    output_map = map(lambda x : x*x, li) #power를 대신함.(제곱)
    #print(list(output_map))
    output_under_3 = filter(output_under_3, li)
    print(list(output_under_3))
    output_under_3 = filter(lambda x: x < 3, li)
    print(list(output_under_3))
    
if __name__ == "__main__":
    main()