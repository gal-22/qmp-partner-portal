import pandas as pd

try:
    df = pd.read_csv('reports/Earnings-summary-data (4).csv')
    print("Columns:", df.columns.tolist())
    print("First few rows of Advertiser Name:\n", df['Advertiser Name'].head(10))
except Exception as e:
    print(e)
