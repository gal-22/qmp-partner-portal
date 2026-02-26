import pandas as pd
import json
import os

def load_caps(filepath):
    with open(filepath, 'r') as f:
        caps = json.load(f)
    return caps

def check_caps_logic():
    filepath = 'caps/partner_caps_jan.json'
    print(f"Loading {filepath}")
    caps = load_caps(filepath)
    
    # Check Betterment raw
    betterment = next((c for c in caps if c['Partner'] == 'Betterment'), None)
    print("Raw Betterment entry:", betterment)
    
    # DataFrame creation
    caps_df_lookup = pd.DataFrame(caps)
    print("\nDataFrame Columns:", caps_df_lookup.columns.tolist())
    
    if 'MonthlyCap' not in caps_df_lookup.columns: 
         print("MonthlyCap COLUMN MISSING. Logic would fill it with DailyCap * 30")
         caps_df_lookup['MonthlyCap'] = caps_df_lookup['DailyCap'] * 30
    else:
         print("MonthlyCap column exists.")
         
    # Check Betterment in DF
    row = caps_df_lookup[caps_df_lookup['Partner'] == 'Betterment']
    print("\nBetterment Row in DF:\n", row[['Partner', 'DailyCap', 'MonthlyCap']])
    
    m_cap = row['MonthlyCap'].values[0]
    print(f"\nExtracted MonthlyCap: {m_cap}")
    
    d_cap = row['DailyCap'].values[0]
    calc_cap = d_cap * 30
    print(f"DailyCap * 30 calculation: {calc_cap}")
    
    if m_cap == calc_cap:
        print("ALERT: MonthlyCap matches DailyCap * 30.")
    else:
        print("MonthlyCap DOES NOT match DailyCap * 30.")

if __name__ == "__main__":
    check_caps_logic()
