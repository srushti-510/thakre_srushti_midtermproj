from itertools import combinations

def generate_rules(freq_sup, minconf):
    """
    Build rules A -> B from frequent itemsets.
    Keep rules with confidence >= minconf.
    Return list of (A, B, support_X, confidence) sorted by confidence.
    """
    rules = []
    for X, supX in freq_sup.items():
        if len(X) < 2:
            continue
        items = list(X)
        # All non-empty proper subsets A of X
        for r in range(1, len(items)):
            for A in combinations(items, r):
                A = frozenset(A)
                B = X - A
                supA = freq_sup.get(A)
                if not supA:
                    continue
                conf = supX / supA
                if conf >= minconf:
                    rules.append((A, B, supX, conf))
    rules.sort(key=lambda z: z[3], reverse=True)
    return rules
