import json
import pandas as pd
import numpy as np

notebook_path = 'car_price/Old Car Price Predicution.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

extracted_df = None
for i, cell in enumerate(nb.get('cells', [])):
    outputs = cell.get('outputs', [])
    for out in outputs:
        # Check for dataframe in HTML or text
        data_html = out.get('data', {}).get('text/html', [])
        if data_html:
            html_str = "".join(data_html)
            if '<table' in html_str and ('Location' in html_str or 'Price' in html_str):
                try:
                    dfs = pd.read_html(html_str)
                    if dfs and len(dfs[0]) > 50:
                        print(f"Found table in cell {i} with shape {dfs[0].shape}")
                        if extracted_df is None or len(dfs[0]) > len(extracted_df):
                            extracted_df = dfs[0]
                except Exception as e:
                    pass

print("Extracted DF shape:", extracted_df.shape if extracted_df is not None else "None")
