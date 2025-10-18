# Library-based mining (Apriori & FP-Growth) using mlxtend
# Note: install once (document in README, not in code): pip install pandas mlxtend

from pathlib import Path
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

def _to_onehot(transactions):
    items = sorted({i for t in transactions for i in t})
    data = [[(i in t) for i in items] for t in transactions]   # True/False
    return pd.DataFrame(data, columns=items, dtype=bool)


def mine_with_apriori(transactions, minsup, minconf):
    """Return list[(A,B,support,confidence)] via Apriori."""
    df = _to_onehot(transactions)
    freq = apriori(df, min_support=minsup, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=minconf)
    out = []
    for _, r in rules.iterrows():
        A = frozenset(r["antecedents"])
        B = frozenset(r["consequents"])
        out.append((A, B, float(r["support"]), float(r["confidence"])))
    out.sort(key=lambda z: z[3], reverse=True)
    return out

def mine_with_fpgrowth(transactions, minsup, minconf):
    """Return list[(A,B,support,confidence)] via FP-Growth."""
    df = _to_onehot(transactions)
    freq = fpgrowth(df, min_support=minsup, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=minconf)
    out = []
    for _, r in rules.iterrows():
        A = frozenset(r["antecedents"])
        B = frozenset(r["consequents"])
        out.append((A, B, float(r["support"]), float(r["confidence"])))
    out.sort(key=lambda z: z[3], reverse=True)
    return out

def print_rules(rules, n=10):
    """Pretty-print top n rules in our A -> B format."""
    for i, (A, B, s, c) in enumerate(rules[:n], 1):
        print(f"Rule {i}: {sorted(A)} -> {sorted(B)}")
        print(f"  Support: {s:.2%}  Confidence: {c:.2%}")
