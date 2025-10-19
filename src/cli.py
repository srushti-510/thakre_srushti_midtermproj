from __future__ import annotations
from pathlib import Path
import sys
import re

from io_utils import load_transactions
from bruteforce import mine_frequent_itemsets
from rules import generate_rules


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PERCENT_RX = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*%?\s*$")


def _find_datasets() -> list[Path]:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data folder not found: {DATA_DIR}")
    csvs = sorted(p for p in DATA_DIR.glob("*.csv") if p.is_file())
    if not csvs:
        raise FileNotFoundError(f"No CSV files found under {DATA_DIR}")
    return csvs


def _prompt_menu(csvs: list[Path]) -> Path:
    print("Market-Basket Miner")
    for i, p in enumerate(csvs, 1):
        print(f"{i}. {p.name}")
    while True:
        s = input(f"Select dataset (1-{len(csvs)}): ").strip()
        if s.isdigit():
            k = int(s)
            if 1 <= k <= len(csvs):
                return csvs[k - 1]
        print("Invalid choice. Please enter a valid number from the list.")


def _prompt_prob(label: str) -> float:
    """
    Accepts '0.2', '20', '20%' etc., returns a float in (0, 1].
    """
    while True:
        raw = input(f"{label} (e.g., 0.2 or 20%): ").strip()
        m = PERCENT_RX.match(raw)
        if not m:
            print("Please enter a number like 0.2 or 20%.")
            continue
        val = float(m.group(1))
        if val > 1.0:  # interpret as percent
            val /= 100.0
        if 0.0 < val <= 1.0:
            return val
        print("Value must be within (0, 1].")


def _sanity_check_transactions(txns):
    if not txns:
        raise ValueError("Loaded zero transactions.")
    if not all(isinstance(t, (set, frozenset)) for t in txns):
        raise TypeError("Transactions must be sets of items.")
    if not all(all(isinstance(x, str) for x in t) for t in txns):
        raise TypeError("Each item must be a string.")
    if len(set().union(*txns)) < 2:
        raise ValueError("Dataset must contain at least 2 distinct items.")


def main() -> int:
    try:
        csvs = _find_datasets()
    except Exception as e:
        print(f"❌ {e}")
        return 2

    csv_path = _prompt_menu(csvs)
    store_label = csv_path.stem  # label derived from filename

    minsup = _prompt_prob("Minimum Support")
    minconf = _prompt_prob("Minimum Confidence")

    # Load & validate transactions
    try:
        txns = load_transactions(csv_path)
        _sanity_check_transactions(txns)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except Exception as e:
        print(f"❌ Failed to load/validate '{csv_path.name}': {e}")
        return 3

    n_tx = len(txns)
    print(
        f"\nStore: {store_label} | file={csv_path} | transactions={n_tx} | "
        f"minsup={minsup:.2%} | minconf={minconf:.2%}"
    )

    # Mine frequent itemsets (brute-force) and rules with defensive guards
    try:
        freq = mine_frequent_itemsets(txns, minsup)
    except Exception as e:
        print(f"❌ Brute-force mining failed: {e}")
        return 4

    try:
        rules = generate_rules(freq, minconf)
    except Exception as e:
        print(f"❌ Rule generation failed: {e}")
        return 5

    # Print frequent itemsets by size
    by_k: dict[int, list[tuple[list[str], float]]] = {}
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
    else:
        for i, (A, B, s, conf) in enumerate(rules, 1):
            count = int(round(s * n_tx))
            print(f"Rule {i}: {sorted(A)} -> {sorted(B)}")
            print(f"  Support: {s:.2%} (count={count})  Confidence: {conf:.2%}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
