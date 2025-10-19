# CS 634 — Midterm Project 

## Setup (one time)

```bash
# Create & activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Project layout
- data/ — CSV datasets 
- notebooks/ — `midtermproject.ipynb` 
- src/ — source code  
  - `cli.py` — brute-force runner 
  - `bruteforce.py`, `rules.py`, `io_utils.py` — mining & rule generation  
  - `apriori_fp.py` — library wrappers for Apriori & FP-Growth 
