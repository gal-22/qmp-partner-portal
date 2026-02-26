# QMP Analysis - Partner Earnings Dashboard

A Streamlit-based web application for analyzing partner earnings data, tracking budget utilization, and monitoring campaign performance.

## Features

- 📊 **Partner Earnings Analysis**: View and analyze earnings data by partner
- 💰 **Budget Tracking**: Monitor daily and monthly caps with utilization percentages
- 📈 **Performance Metrics**: Track clicks, EPC (Earnings Per Click), and conversion rates
- 📅 **Date Range Analysis**: Filter and analyze data for specific time periods
- 🎯 **Partner Performance**: Compare partners and identify top performers
- 💵 **Profit Margin Analysis**: Calculate and visualize profit margins by comparing earnings with Google Ads spend

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Clone or Download the Project

Download the project folder to your local machine.

### 2. Install Python Dependencies

Open a terminal/command prompt, navigate to the project directory, and run:

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations

### 3. Project Structure

Make sure you have the following structure:
```
qmp-analysis/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── partner_caps.json           # Partner budget caps configuration
├── config.json                 # Application configuration
├── caps/                       # Monthly caps data
│   └── partner_caps_jan.json
├── ad_spend/                   # Google Ads spend data (CSV files)
│   └── [your spend CSV files here]
└── reports/                    # CSV reports directory
    └── [your earnings CSV files here]
```

### 4. Add Your Data

#### Earnings Reports
Place your earnings CSV reports in the `reports/` folder. The CSV files should contain columns like:
- Date
- Advertiser Name
- Supplier Earnings($)
- Clicks
- EPC (Earnings Per Click)
- Impressions
- etc.

#### Google Ads Spend Data (Optional - for Profit Margin Analysis)
Place your Google Ads daily spend CSV files in the `ad_spend/` folder. The CSV files **must** contain:
- `Date` - Date in YYYY-MM-DD format
- `Daily Spend` - Daily ad spend amount (can include $ symbol and commas, they will be cleaned)

Example CSV format:
```csv
Date,Daily Spend
2025-12-01,150.00
2025-12-02,145.50
2025-12-03,148.75
```

A template file (`google_ads_spend_template.csv`) is provided in the project root directory.

## Running the Application

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd /path/to/qmp-analysis
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. The application will open automatically in your default browser at `http://localhost:8501`

If it doesn't open automatically, copy the Local URL shown in the terminal and paste it into your browser.

## Usage

### Basic Workflow

1. **Upload Reports**: The app automatically loads CSV files from the `reports/` folder
2. **Select Report**: Use the dropdown to select which earnings report to analyze
3. **Upload Google Ads Spend** (Optional): 
   - Expand "Manage Google Ads Spend Data" section
   - Upload your daily spend CSV file
   - The app will calculate profit margins automatically
4. **View Analytics**: Explore different sections:
   - Partner performance metrics
   - Daily earnings and clicks
   - EPC trends
   - **Profit margin analysis** (when spend data is loaded)
   - Budget utilization
5. **Interactive Charts**: Click and hover on charts for detailed information
6. **Filter by Date Range**: Use the sidebar date picker to analyze specific periods

### Profit Margin Analysis

When you upload Google Ads spend data, the application will display:
- **Total Profit Metrics**: Total earnings, ad spend, profit, and profit margin percentage
- **Daily Profit/Loss Chart**: Visualize earnings, spend, and profit over time
- **Profit Margin % Trend**: Track how your profit margin changes day-by-day
- **Financial Summary**: Compare total earnings vs. spend vs. profit for the selected period
- **Detailed Daily Breakdown**: View profit/loss data in a table format

## Configuration

### Partner Caps (`partner_caps.json` and `caps/partner_caps_jan.json`)
Configure daily and monthly budget caps for each partner. The application will track actual spend vs. caps.

### Config (`config.json`)
General application settings and preferences.

## Troubleshooting

### Common Issues

**Issue**: `streamlit: command not found`
- **Solution**: Make sure Python and pip are installed, then run `pip install streamlit` again

**Issue**: Module not found errors
- **Solution**: Install missing packages: `pip install pandas plotly streamlit`

**Issue**: No data showing in the app
- **Solution**: Make sure CSV files are in the `reports/` folder and formatted correctly

**Issue**: Port 8501 already in use
- **Solution**: Either stop the other Streamlit instance or run on a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

## Stopping the Application

To stop the application:
- Press `Ctrl+C` in the terminal where the app is running

## Data Privacy

⚠️ **Important**: This application processes financial and partner data locally on your machine. No data is sent to external servers. Keep your data files secure and only share with authorized personnel.

## Support

For questions or issues, contact the development team.

---

**Last Updated**: January 2026
