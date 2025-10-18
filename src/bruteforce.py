from collections import Counter

def _support(itemset, txns):
    """Support = fraction of transactions containing itemset."""
    n = len(txns)
    if n == 0:
        return 0.0
    return sum(1 for t in txns if itemset.issubset(t)) / n

def mine_frequent_itemsets(txns, minsup):
    """
    Level-wise brute force:
      - Find L1 (single items with support >= minsup)
      - Join Lk -> candidates for L(k+1)
      - Keep those meeting minsup; repeat until none
    Returns {itemset: support}.
    """
    # L1
    C1 = Counter(x for t in txns for x in t)
    supmap = {frozenset([i]): C1[i] / len(txns) for i in C1}
    L = {k for k, s in supmap.items() if s >= minsup}
    all_freq = {k: supmap[k] for k in L}

    # Lk -> L(k+1)
    while L:
        prev = sorted(L)
        k = len(next(iter(L)))  # current size
        candidates = set()
        # Join pairs that differ by 1 item
        for i in range(len(prev)):
            for j in range(i + 1, len(prev)):
                u = prev[i] | prev[j]
                if len(u) == k + 1:
                    candidates.add(u)
        # Count supports and keep frequent
        next_L = set()
        for c in candidates:
            s = _support(c, txns)
            if s >= minsup:
                next_L.add(c)
                all_freq[c] = s
        L = next_L

    return all_freq
