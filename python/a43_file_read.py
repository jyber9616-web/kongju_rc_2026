from pathlib import Path

def main():
    url = Path(__file__).parent.parent / "data" / "text.txt"
    bin_rul = Path(__file__).parent.parent / "data" / "text.txt"
    with open(url, "r", encoding= 'utf-8') as f:
        data = f.read()
        print(data)
        f.seek(0)
        while data := f.readling():
            print(data)
        f.seek(0)
        data =  f.readlines()
        print(data)
            
if __name__ == "__main__":
    main()
    