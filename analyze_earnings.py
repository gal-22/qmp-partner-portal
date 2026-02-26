import pandas as pd
import numpy as np

def load_and_analyze(filepath):
    print(f"Loading {filepath}")
    df = pd.read_csv(filepath)
    
    # Logic from app.py
    if 'Supplier Earnings($)' in df.columns:
        df['Earnings'] = df['Supplier Earnings($)'].replace('[\$,]', '', regex=True)
        df['Earnings'] = pd.to_numeric(df['Earnings'], errors='coerce').fillna(0)
    else:
        print("Column 'Supplier Earnings($)' not found.")
        return

    # Check for specific sum
    target_sum = 260.47
    tolerance = 0.01
    
    # 1. Group by Advertiser Name
    grouped = df.groupby('Advertiser Name')['Earnings'].sum()
    
    print("\n--- Partners with sum close to 260.47 ---")
    found = False
    for name, earnings in grouped.items():
        if abs(earnings - target_sum) < tolerance:
            print(f"MATCH: '{name}' - Earnings: {earnings}")
            found = True
            
    if not found:
        print("No exact match found for 260.47 by Advertiser Name")
        
    # 2. Check for empty/NaN names
    print("\n--- Rows with problematic Partner Names ---")
    # Check nulls
    null_mask = df['Advertiser Name'].isna()
    if null_mask.any():
        null_sum = df[null_mask]['Earnings'].sum()
        print(f"NULL Advertiser Names Sum: {null_sum}")
        print(df[null_mask])
        
    # Check empty strings
    empty_mask = df['Advertiser Name'].astype(str).str.strip() == ''
    if empty_mask.any():
        empty_sum = df[empty_mask]['Earnings'].sum()
        print(f"EMPTY Advertiser Names Sum: {empty_sum}")
        print(df[empty_mask])
        
    # Check sums of all to see if any combination matches? No, user implied a single partner.

    # 3. Check combinations logic? 
    # Maybe the user sees "MappedPartner" as empty?
    # Let's verify mapping logic
    
    print("\n--- Inspecting Mapped Partner logic simulation ---")
    # Simulation of map_partner_name from app.py
    # We don't have caps loaded here so we'll just check the Raw names.
    
    # Sort by earnings desc
    print(grouped.sort_values(ascending=False).head(10))

if __name__ == "__main__":
    load_and_analyze('reports/Earnings-summary-data (4).csv')
