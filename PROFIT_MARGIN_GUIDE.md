# Profit Margin Analysis - Quick Start Guide

## Overview
The new Profit Margin Analysis feature allows you to calculate and visualize your profit by comparing your earnings from QS (QuinStreet) with your Google Ads spending.

## How It Works

**Formula:**
- **Profit** = Total Earnings - Total Ad Spend
- **Profit Margin %** = (Profit / Total Earnings) × 100

## Setup Instructions

### Step 1: Prepare Your Google Ads Spend Data

1. Export your Google Ads daily spend data to a CSV file
2. The CSV **must** have these two columns:
   - `Date` (format: YYYY-MM-DD)
   - `Daily Spend` (your daily ad spend amount)

**Example CSV:**
```csv
Date,Daily Spend
2025-12-01,150.00
2025-12-02,145.50
2025-12-03,148.75
2025-12-04,152.30
```

**Note:** Dollar signs ($) and commas (,) in the spend amount are automatically cleaned.

### Step 2: Upload to the Application

1. Open the application (http://localhost:8501)
2. Expand the **"Manage Google Ads Spend Data"** section
3. Click **"Upload Ad Spend CSV"**
4. Select your CSV file
5. The file will be saved to the `ad_spend/` directory

### Step 3: View Profit Margin Analysis

Once uploaded, the **"💰 Profit Margin Analysis"** section will automatically appear with:

#### 1. **Key Metrics Dashboard**
- 💵 Total Earnings
- 💸 Total Ad Spend  
- 💰 Total Profit
- 📊 Profit Margin %

#### 2. **Daily Profit/Loss Chart**
- Green line: Your earnings over time
- Red line: Your ad spend over time
- Bars: Daily profit (green = profit, red = loss)

#### 3. **Profit Margin % Over Time**
- Track how your profit margin changes day-by-day
- Shows break-even line (0%)
- Shows average profit margin

#### 4. **Total Summary Chart**
- Side-by-side comparison of Total Earnings, Total Spend, and Total Profit

#### 5. **Daily Details Table**
- Expandable table with day-by-day breakdown
- Shows Earnings, Ad Spend, Profit, and Margin % for each day

## Using Date Filters

The profit analysis respects your date range selection:
1. Use the **sidebar date picker** to select a custom date range
2. All profit calculations update automatically for the selected period
3. You can analyze profit for specific weeks, months, or custom periods

## Tips

✅ **Best Practices:**
- Keep your Google Ads spend CSV up to date
- Match the date ranges in your earnings and spend data
- Upload a new spend file whenever you have updated data

⚠️ **Important:**
- If a date has earnings but no spend data, spend is assumed to be $0
- Dates with no earnings will not show in the analysis
- Ensure your date formats match (YYYY-MM-DD)

## File Management

### Renaming Files
1. Expand **"Rename Ad Spend File"**
2. Enter new name (must end with .csv)
3. Click **"Rename Spend File"**

### Deleting Files
1. Expand **"Delete Ad Spend File"**
2. Click **"Delete Spend File"**
3. Confirm deletion

### Switching Files
- Use the dropdown to switch between different spend files
- Useful for comparing different months or campaigns

## Example Workflow

1. **Weekly Analysis:**
   - Upload weekly Google Ads spend data
   - Select the matching earnings report
   - Set date range to the specific week
   - View profit margin for that week

2. **Monthly Comparison:**
   - Upload separate spend files for each month
   - Switch between months using the dropdown
   - Compare profit margins across months

3. **Optimization:**
   - Identify days with low profit margins
   - Adjust your ad campaigns accordingly
   - Re-upload spend data and verify improvements

## Sample Data

A template file is provided: `google_ads_spend_template.csv`
- Located in the project root directory
- Contains sample December 2025 data
- Use it as a reference for formatting your own data

## Troubleshooting

**Problem:** Profit analysis section doesn't show
- **Solution:** Make sure you've uploaded a spend CSV file

**Problem:** Numbers don't match
- **Solution:** Check that your date ranges overlap in both earnings and spend data

**Problem:** "Daily Spend column not found" error
- **Solution:** Ensure your CSV has exactly "Daily Spend" as the column name (case-sensitive)

**Problem:** Dates not matching
- **Solution:** Verify dates are in YYYY-MM-DD format in both files

## Questions?

If you need help or have questions about the profit margin feature, refer to the main README.md or contact support.

---

**Happy Analyzing! 📊💰**
