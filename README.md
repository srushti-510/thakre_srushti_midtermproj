# CS 634 — Midterm Project 

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python src/cli.py

## Project layout
- data/ — CSV datasets 
- notebooks/ — `midtermproject.ipynb` 
- src/ — source code  
  - `cli.py` — brute-force runner 
  - `bruteforce.py`, `rules.py`, `io_utils.py` — mining & rule generation  
  - `apriori_fp.py` — library wrappers for Apriori & FP-Growth 
