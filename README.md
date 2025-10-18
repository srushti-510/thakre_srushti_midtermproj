# CS 634 — Midterm Project 

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python src/cli.py

## Project layout
- **data/** — CSV datasets (small, deterministic)
- **notebooks/** — `midtermproject_demo.ipynb` (shows Apriori & FP-Growth runs)
- **src/** — source code  
  - `cli.py` — brute-force runner (Part 2)  
  - `bruteforce.py`, `rules.py`, `io_utils.py` — mining & rule generation  
  - `apriori_fp.py` — library wrappers for Apriori & FP-Growth (Part 3)

## Submission reminders (per instructions)
- Do **not** include: `.venv/`, `.git/`, `.DS_Store`, installed packages/binaries, or large datasets.  
- Zip should contain: **report** (.docx/.pdf), **.py** files, **.ipynb**, and **CSV** files only.
