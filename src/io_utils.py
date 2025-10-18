from pathlib import Path

def load_transactions(csv_path):
    """Read CSV: one basket per line, comma-separated, no header."""
    lines = Path(csv_path).read_text(encoding="utf-8").splitlines()
    txns = []
    for line in lines:
        items = [x.strip() for x in line.split(",") if x.strip()]
        if items:
            txns.append(frozenset(items))
    if not txns:
        raise ValueError(f"No transactions found in {csv_path}")
    return txns
