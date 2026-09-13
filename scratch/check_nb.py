import json
import pandas as pd
import numpy as np

notebook_path = 'car_price/Old Car Price Predicution.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("Cells count:", len(nb.get('cells', [])))
for i, cell in enumerate(nb.get('cells', [])):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if 'read_csv' in source or 'fit' in source or 'DataFrame' in source:
            print(f"--- Cell {i} ---")
            print(source[:300])
