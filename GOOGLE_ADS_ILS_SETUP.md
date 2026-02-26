# Google Ads ILS Currency - Implementation Summary

## ✅ What Was Done

### 1. **Analyzed Your Google Ads CSV Format**
Your file has the following format:
```csv
Date,Cost
"Thu, Jan 1, 2026","₪2,117.50"
"Fri, Jan 2, 2026","₪2,909.80"
```

**Key characteristics:**
- Date format: "Day, Mon DD, YYYY"
- Cost column with ILS symbol (₪)
- Values include commas for thousands separator
- Some values have quotes, some don't

### 2. **Enhanced Currency Support**
Updated the `load_ad_spend()` function to:
- ✅ Automatically detect "Cost" column (Google Ads format) or "Daily Spend" (simple format)
- ✅ Remove ILS symbol (₪) and commas
- ✅ Convert ILS to USD using configurable exchange rate
- ✅ Parse Google Ads date format automatically
- ✅ Handle mixed quoting in CSV files

### 3. **Added Currency Configuration UI**
New features in "Manage Google Ads Spend Data" section:
- 💱 **Currency Settings** subsection
- Exchange rate input (ILS to USD)
- Default rate: 3.1 (₪3.1 = $1.00)
- Persistent storage of your preferred rate
- Visual feedback showing current conversion rate

### 4. **File Integration**
Your file has been copied to: `ad_spend/google_ads_spend_january_2026.csv`

## 🚀 How to Use

### Step 1: Open the App
The app is already running at: **http://localhost:8501**

### Step 2: Load Your Data

1. **Expand "Manage Google Ads Spend Data"**
2. **Select your file** from the dropdown:
   - Choose `google_ads_spend_january_2026.csv`
3. **Verify/Adjust Exchange Rate**:
   - Default: ₪3.6 = $1.00
   - Update if needed based on current exchange rates
   - Click "Save Rate" to persist

### Step 3: View Profit Margins

The app will automatically:
- Convert all ILS amounts to USD
- Match dates with your earnings data
- Calculate daily and total profit margins
- Display all profit analysis graphs

## 📊 What You'll See

### Currency Conversion Notice
When you load the file, you'll see:
```
💱 Converted ILS to USD using rate: ₪3.6 = $1
```

### Your January 2026 Data
**Example conversion:**
- Jan 1: ₪2,117.50 → $588.19 USD
- Jan 2: ₪2,909.80 → $808.28 USD
- Jan 3: ₪2,256.52 → $626.81 USD

### Available Metrics (in USD)
- 💵 Total Earnings (from QS data)
- 💸 Total Ad Spend (converted from ILS)
- 💰 Total Profit
- 📊 Profit Margin %

### Graphs Available
1. **Daily Profit/Loss** - See which days were profitable
2. **Profit Margin % Over Time** - Track margin trends
3. **Total Summary** - Compare earnings vs spend vs profit
4. **Daily Details Table** - Full breakdown by day

## 🔧 Updating Exchange Rate

If you need to update the exchange rate later:

1. Expand "Manage Google Ads Spend Data"
2. Scroll to "💱 Currency Settings"
3. Enter new rate (e.g., 3.7 if exchange rate changed)
4. Click "Save Rate"
5. The app will reload and recalculate everything

## 📅 Date Range Analysis

Use the sidebar date picker to analyze specific periods:
- **Full Month**: Select Jan 1-31, 2026
- **Specific Week**: Select any 7-day range
- **Custom Period**: Pick any start/end dates

All profit calculations update based on selected range!

## 💡 Understanding Your Profit Margins

### Example Calculation:
```
Day: Jan 1, 2026
Earnings: $800.00 (from QS)
Ad Spend: $588.19 (₪2,117.50 converted)
---------------------------------
Profit: $211.81
Margin: 26.5%
```

### What Good Margins Look Like:
- **> 30%** - Excellent profitability
- **20-30%** - Good, sustainable
- **10-20%** - Moderate, room for optimization
- **< 10%** - Low, consider optimization
- **Negative** - Loss, needs immediate attention

## 📈 Next Steps

1. **Review Your Data**
   - Check the profit margin graphs
   - Identify which days had best/worst margins
   - Look for patterns or trends

2. **Optimize Campaigns**
   - Use insights to adjust ad spend
   - Focus on high-margin days/partners
   - Reduce spend on low-margin periods

3. **Track Over Time**
   - Upload new spend data regularly
   - Compare month-to-month
   - Monitor margin improvements

## 🎯 Quick Tips

✅ **Do:**
- Keep exchange rate updated
- Review margins weekly
- Compare different date ranges
- Export data for deeper analysis

⚠️ **Note:**
- The app assumes dates in spend file match dates in earnings data
- Days with $0.00 spend are included (like Jan 18-21 in your file)
- All calculations are in USD after conversion

## 🔍 Your Specific Data

Your file shows:
- **31 days** of data (January 2026)
- **Total ILS Spend**: ~₪63,000 (approximately)
- **Total USD Spend**: ~$17,500 (at 3.6 rate)
- **4 days with $0 spend** (Jan 18-21)

Compare this with your earnings to see your actual profit!

---

**Everything is ready to go! Just open http://localhost:8501 and explore your profit margins! 💰📊**
