from loader import load_csv

if __name__ == "__main__":
    data = load_csv("data/banking_transactions.csv")
    print("Show 1 data Example\n")
    print(data[0:1])