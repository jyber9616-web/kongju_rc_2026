class mylist:
    def __init__(self):
        self.myVariable = "j"
        self.myVariable2 = "y"
        self.mylist = list()
    
    def append(self, ele):
        self.mylist.append(ele)

def main():
    list_a = [1,2,3]
    list_b = [4,5,6]
    print(list_a + list_b)
    print(list_a)
    list_a.extend(list_b)
    print(list_a)

    list_b.append(7)
    list_b.append(8)
    print(list_b)
    list_b.insert(1, 4.5) #type: ignored
    print(list_b)
    mylist_A = mylist()
    mylist_A.append("jyc")
    print(mylist_A.myVariable, mylist_A.myVariable2,
          mylist_A.mylist)

if __name__ == "__main__":
    main()
