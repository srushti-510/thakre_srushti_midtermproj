from io_utils import load_transactions
from bruteforce import mine_frequent_itemsets
from rules import generate_rules

# Menu: label + CSV path
DATASETS = {
    "1": ("Amazon",  "data/amazon.csv"),
    "2": ("Best Buy","data/bestbuy.csv"),
    "3": ("KMart",   "data/kmart.csv"),
    "4": ("Nike",    "data/nike.csv"),
    "5": ("Walmart", "data/walmart.csv"),
}

def _prompt_menu():
    # Show menu and return (label, path)
    print("Market-Basket Miner")
    for k, (label, _) in DATASETS.items():
        print(f"{k}. {label}")
    while True:
        choice = input("Select dataset (1-5): ").strip()
        if choice in DATASETS:
            label, path = DATASETS[choice]
            return label, path
        print("Invalid choice. Please enter a number from 1 to 5.")

def _prompt_percent(label):
    # Ask for percentage in (0, 100]; return as fraction [0,1]
    while True:
        raw = input(f"{label} (%) [1-100]: ").strip()
        try:
            val = float(raw)
            if 0 < val <= 100:
                return val / 100.0
        except ValueError:
            pass
        print("Invalid number. Enter a value between 1 and 100 (exclusive of 0).")

def main():
    # Inputs
    store_label, csv_path = _prompt_menu()
    minsup = _prompt_percent("Minimum Support")
    minconf = _prompt_percent("Minimum Confidence")

    # Load data
    txns = load_transactions(csv_path)
    n_tx = len(txns)

    # Mine itemsets and rules
    freq = mine_frequent_itemsets(txns, minsup)
    rules = generate_rules(freq, minconf)

    print(f"\nStore: {store_label} | file={csv_path} | transactions={n_tx} | "
          f"minsup={minsup:.2%} | minconf={minconf:.2%}")

    # Print frequent itemsets by size (L1, L2, ...)
    by_k = {}
    for it, sup in freq.items():
        by_k.setdefault(len(it), []).append((sorted(it), sup))
    for k in sorted(by_k):
        print(f"\nL{k} (frequent {k}-itemsets):")
        for items, sup in sorted(by_k[k]):
            count = int(round(sup * n_tx))
            print(f"{items} | count={count} | support={sup:.2%}")

    # Print rules
    print("\nFinal Association Rules (A -> B):")
    if not rules:
        print("No rules at these thresholds.")
    for i, (A, B, s, conf) in enumerate(rules, 1):
        count = int(round(s * n_tx))
        print(f"Rule {i}: {sorted(A)} -> {sorted(B)}")
        print(f"  Support: {s:.2%} (count={count})  Confidence: {conf:.2%}")

if __name__ == "__main__":
    main()
