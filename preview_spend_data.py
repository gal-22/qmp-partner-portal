"""
Quick analysis of Google Ads spend data - Preview
This script shows what your profit margins will look like in the app
"""

import pandas as pd

# Load the Google Ads spend data
df = pd.read_csv('ad_spend/google_ads_spend_january_2026.csv')

# Clean Cost column
df['Cost_ILS'] = df['Cost'].astype(str).replace('[₪,]', '', regex=True)
df['Cost_ILS'] = pd.to_numeric(df['Cost_ILS'], errors='coerce').fillna(0)

# Convert to USD
ILS_TO_USD = 3.6
df['Cost_USD'] = df['Cost_ILS'] / ILS_TO_USD

# Parse dates
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

print("=" * 80)
print("GOOGLE ADS SPEND ANALYSIS - JANUARY 2026")
print("=" * 80)
print(f"\nCurrency Conversion: ₪{ILS_TO_USD} = $1.00 USD\n")

# Summary statistics
total_ils = df['Cost_ILS'].sum()
total_usd = df['Cost_USD'].sum()
avg_daily_ils = df['Cost_ILS'].mean()
avg_daily_usd = df['Cost_USD'].mean()
days_with_spend = len(df[df['Cost_ILS'] > 0])
days_zero_spend = len(df[df['Cost_ILS'] == 0])

print("SUMMARY STATISTICS:")
print("-" * 80)
print(f"Total Days:              {len(df)}")
print(f"Days with Spend:         {days_with_spend}")
print(f"Days with Zero Spend:    {days_zero_spend}")
print(f"\nTotal Spend (ILS):       ₪{total_ils:,.2f}")
print(f"Total Spend (USD):       ${total_usd:,.2f}")
print(f"\nAverage Daily (ILS):     ₪{avg_daily_ils:,.2f}")
print(f"Average Daily (USD):     ${avg_daily_usd:,.2f}")
print(f"\nHighest Day (ILS):       ₪{df['Cost_ILS'].max():,.2f}")
print(f"Highest Day (USD):       ${df['Cost_USD'].max():,.2f}")
print(f"Lowest Day (non-zero):   ₪{df[df['Cost_ILS'] > 0]['Cost_ILS'].min():,.2f}")
print()

print("\nDAILY BREAKDOWN:")
print("-" * 80)
print(f"{'Date':<20} {'ILS Spend':>15} {'USD Spend':>15}")
print("-" * 80)

for idx, row in df.iterrows():
    date_str = row['Date'].strftime('%a, %b %d, %Y')
    ils_str = f"₪{row['Cost_ILS']:,.2f}" if row['Cost_ILS'] > 0 else "₪0.00"
    usd_str = f"${row['Cost_USD']:,.2f}" if row['Cost_USD'] > 0 else "$0.00"
    print(f"{date_str:<20} {ils_str:>15} {usd_str:>15}")

print("-" * 80)
print(f"{'TOTAL':<20} {'₪' + f'{total_ils:,.2f}':>15} {'$' + f'{total_usd:,.2f}':>15}")
print("=" * 80)

print("\n📊 This data is now available in the app for profit margin analysis!")
print("🌐 Open: http://localhost:8501")
print("📁 File: ad_spend/google_ads_spend_january_2026.csv")
print("\n✅ Ready to calculate profit margins when matched with earnings data!")
