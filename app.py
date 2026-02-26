import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import io
import os

import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase Initialization ---
@st.cache_resource
def init_firestore():
    try:
        # Clear any existing apps to prevent broken cached states
        if firebase_admin._apps:
            for app_name in list(firebase_admin._apps.keys()):
                firebase_admin.delete_app(firebase_admin.get_app(app_name))
                
        if "firebase" in st.secrets:
            cred_dict = dict(st.secrets["firebase"])
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            
            if 'project_id' in cred_dict:
                os.environ['GOOGLE_CLOUD_PROJECT'] = cred_dict['project_id']
                
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'projectId': cred_dict.get('project_id')
            })
        else:
            # Local fallback
            if os.path.exists('qmp-partner-portal-2026-firebase-adminsdk-fbsvc-c45407ee13.json'):
                cred = credentials.Certificate('qmp-partner-portal-2026-firebase-adminsdk-fbsvc-c45407ee13.json')
                firebase_admin.initialize_app(cred)
            else:
                st.error("⚠️ Streamlit Secrets are missing! Please add the [firebase] block to your App's Advanced Settings > Secrets.")
                st.stop()
        return firestore.client()
    except Exception as e:
        st.error(f"⚠️ Firebase Initialization Error: {e}")
        st.stop()

db = init_firestore()

# --- Data Loading and Processing ---

@st.cache_data
def load_data(report_name):
    # Load CSV from Firestore
    doc = db.collection('reports').document(report_name).get()
    if not doc.exists:
        raise ValueError(f"Report {report_name} not found in Firestore.")
    
    csv_string = doc.get('csv_data')
    df = pd.read_csv(io.StringIO(csv_string))
    
    # Clean 'Supplier Earnings($)' column
    df['Earnings'] = df['Supplier Earnings($)'].replace(r'[\$,]', '', regex=True)
    df['Earnings'] = pd.to_numeric(df['Earnings'], errors='coerce').fillna(0)

    # Clean 'Clicks' column
    df['Clicks'] = df['Clicks'].astype(str).str.replace(',', '', regex=False)
    df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce').fillna(0)

    # Calculate EPC
    df['EPC'] = df.apply(lambda row: row['Earnings'] / row['Clicks'] if row['Clicks'] > 0 else 0, axis=1)
    
    # Parse Date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    
    return df

def load_caps(caps_name):
    doc = db.collection('caps').document(caps_name).get()
    if doc.exists:
        return doc.get('data')
    return []

def map_partner_name(full_name, caps_data):
    full_name_lower = full_name.lower()
    for cap in caps_data:
        partner_name = cap['Partner']
        if not partner_name or not str(partner_name).strip():
            continue
        if partner_name.lower() in full_name_lower:
             return partner_name
    
    # Fallback
    if "betterment" in full_name_lower: return "Betterment"
    if "cash app" in full_name_lower: return "CashApp"
    if "etrade" in full_name_lower or "e*trade" in full_name_lower: return "Etrade"
    if "sofi" in full_name_lower: return "SoFi"
    if "synchrony" in full_name_lower: return "Synchrony"
    if "western alliance" in full_name_lower: return "Western Alliance"
    if "jenius bank" in full_name_lower: return "Jenius Bank"
    if "openbank" in full_name_lower: return "OpenBank"
    if "capital one" in full_name_lower: return "Capital One"
    if "marcus" in full_name_lower: return "Marcus Savings"
    if "gainbridge" in full_name_lower: return "Gainbridge"
    if "axos" in full_name_lower: return "Axos"
    
    return full_name

def save_caps(caps_data, caps_name):
    db.collection('caps').document(caps_name).set({'data': caps_data})
    
def load_config():
    doc = db.collection('config').document('app_config').get()
    if doc.exists:
        return doc.to_dict()
    return {}

def save_config(config_data):
    db.collection('config').document('app_config').set(config_data)

def load_ad_spend(spend_name, ils_to_usd_rate=3.6):
    try:
        doc = db.collection('ad_spend').document(spend_name).get()
        if not doc.exists:
            return pd.DataFrame()
        
        csv_string = doc.get('csv_data')
        df = pd.read_csv(io.StringIO(csv_string))
        
        if 'Cost' in df.columns:
            spend_column = 'Cost'
            is_ils = True
        elif 'Daily Spend' in df.columns:
            spend_column = 'Daily Spend'
            is_ils = False
        else:
            st.error("CSV must have either 'Daily Spend' or 'Cost' column")
            return pd.DataFrame()
        
        df['Spend'] = df[spend_column].astype(str).replace('[\\$₪,]', '', regex=True)
        df['Spend'] = pd.to_numeric(df['Spend'], errors='coerce').fillna(0)
        
        if is_ils:
            df['Spend_ILS'] = df['Spend']
            df['Spend'] = df['Spend'] / ils_to_usd_rate
            st.info(f"💱 Converted ILS to USD using rate: ₪{ils_to_usd_rate} = $1")
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        return df[['Date', 'Spend']]
    except Exception as e:
        st.error(f"Error loading ad spend data: {e}")
        return pd.DataFrame()

# Helper to list documents
def list_firestore_docs(collection_name):
    docs = db.collection(collection_name).stream()
    return [doc.id for doc in docs]

# --- Main App ---

def main():
    st.title("Partner Earnings Analysis")

    # --- Sidebar: Report Selection ---
    st.sidebar.header("Report Selection")
    
    # File Uploader
    uploaded_file = st.sidebar.file_uploader("Upload New Report", type=['csv'])
    if uploaded_file is not None:
        try:
            csv_cont = uploaded_file.getvalue().decode('utf-8')
            db.collection('reports').document(uploaded_file.name).set({'csv_data': csv_cont})
            st.sidebar.success(f"Saved {uploaded_file.name} to Firestore!")
        except Exception as e:
             st.sidebar.error(f"Error saving file: Try ensuring file uses utf-8 encoding. {e}")

    report_files = list_firestore_docs('reports')
    report_files.sort(reverse=True)
    
    if not report_files:
        st.warning("No reports found in Firestore. Please upload a CSV file.")
        return

    config = load_config()
    last_selected = config.get('last_selected_report')
    
    default_index = 0
    if last_selected in report_files:
         default_index = report_files.index(last_selected)

    selected_report = st.sidebar.selectbox("Select Report", report_files, index=default_index)
    
    if selected_report != last_selected:
        config['last_selected_report'] = selected_report
        save_config(config)

    # Renaming Logic
    with st.sidebar.expander("Rename Report"):
        new_name = st.text_input("New Name", value=selected_report)
        if st.button("Rename"):
            if new_name and new_name != selected_report and new_name.endswith('.csv'):
                if new_name in report_files:
                    st.error("File with that name already exists!")
                else:
                    try:
                        # Copy
                        old_doc = db.collection('reports').document(selected_report).get()
                        db.collection('reports').document(new_name).set(old_doc.to_dict())
                        # Delete
                        db.collection('reports').document(selected_report).delete()
                        st.success(f"Renamed to {new_name}")
                        config['last_selected_report'] = new_name
                        save_config(config)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error renaming: {e}")
            elif not new_name.endswith('.csv'):
                st.error("Filename must end with .csv")

    # Deletion Logic
    with st.sidebar.expander("Delete Report"):
        st.write(f"Delete **{selected_report}**?")
        if st.button("Delete Report", type="primary"):
             st.session_state.confirm_delete_report = True
        
        if st.session_state.get('confirm_delete_report'):
             st.warning("Are you sure? This action cannot be undone.")
             if st.button("Confirm Delete Report", type="primary"):
                  try:
                       db.collection('reports').document(selected_report).delete()
                       st.success(f"Deleted {selected_report}")
                       if config.get('last_selected_report') == selected_report:
                            del config['last_selected_report']
                            save_config(config)
                       del st.session_state.confirm_delete_report
                       st.rerun()
                  except Exception as e:
                       st.error(f"Error deleting: {e}")

    # Load data
    try:
        df = load_data(selected_report)
    except Exception as e:
        df = pd.DataFrame()
        st.error(f"Error loading data: {e}")
        return

    # --- Configuration Section ---
    with st.expander("Manage Partner Caps"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
             caps_files = list_firestore_docs('caps')
             caps_files.sort()
             
             if not caps_files:
                 st.error("No caps files found in Firestore.")
                 if st.button("Create Default Caps"):
                      db.collection('caps').document('default_caps.json').set({'data': []})
                      st.rerun()
                 return
                 
             last_selected_caps = config.get('last_selected_caps')
             default_caps_index = 0
             if last_selected_caps in caps_files:
                 default_caps_index = caps_files.index(last_selected_caps)

             selected_caps_file = st.selectbox("Select Caps File", caps_files, index=default_caps_index)
             
             if selected_caps_file != last_selected_caps:
                 config['last_selected_caps'] = selected_caps_file
                 save_config(config)

        with col2:
             uploaded_caps = st.file_uploader("Upload Caps (.json)", type=['json'], key="caps_upload")
             if uploaded_caps:
                  try:
                      caps_data = json.loads(uploaded_caps.getvalue().decode('utf-8'))
                      db.collection('caps').document(uploaded_caps.name).set({'data': caps_data})
                      st.toast(f"Uploaded {uploaded_caps.name}")
                  except Exception as e:
                      st.error(f"Error uploading json: {e}")
        
        # Renaming Logic for Caps
        with st.expander("Rename Caps File"):
             new_caps_name = st.text_input("New Caps Name", value=selected_caps_file)
             if st.button("Rename Caps"):
                 if new_caps_name and new_caps_name != selected_caps_file and new_caps_name.endswith('.json'):
                      if new_caps_name in caps_files:
                          st.error("Caps file with that name already exists!")
                      else:
                          try:
                              old_doc = db.collection('caps').document(selected_caps_file).get()
                              db.collection('caps').document(new_caps_name).set(old_doc.to_dict())
                              db.collection('caps').document(selected_caps_file).delete()
                              st.success(f"Renamed to {new_caps_name}")
                              config['last_selected_caps'] = new_caps_name
                              save_config(config)
                              st.rerun()
                          except Exception as e:
                              st.error(f"Error renaming: {e}")
                 elif not new_caps_name.endswith('.json'):
                      st.error("Filename must end with .json")

        # Deletion Logic for Caps
        with st.expander("Delete Caps File"):
             st.write(f"Delete **{selected_caps_file}**?")
             if st.button("Delete Caps", type="primary"):
                   st.session_state.confirm_delete_caps = True
             
             if st.session_state.get('confirm_delete_caps'):
                   st.warning("Are you sure?")
                   if st.button("Confirm Delete Caps", type="primary"):
                        try:
                             db.collection('caps').document(selected_caps_file).delete()
                             st.success(f"Deleted {selected_caps_file}")
                             if config.get('last_selected_caps') == selected_caps_file:
                                  del config['last_selected_caps']
                                  save_config(config)
                             del st.session_state.confirm_delete_caps
                             st.rerun()
                        except Exception as e:
                             st.error(f"Error deleting: {e}")

        # Load caps from selected file
        try:
            caps = load_caps(selected_caps_file)
        except Exception as e:
            st.error(f"Error loading caps: {e}")
            caps = []

        st.write(f"Editing: **{selected_caps_file}**. Click 'Save Changes' to update.")
        
        caps_df = pd.DataFrame(caps)
        if 'MonthlyCap' not in caps_df.columns:
             if not caps_df.empty:
                caps_df['MonthlyCap'] = caps_df['DailyCap'] * 30
             else:
                caps_df['MonthlyCap'] = pd.Series(dtype='float')
                caps_df['DailyCap'] = pd.Series(dtype='float')
                caps_df['Partner'] = pd.Series(dtype='str') 
        else:
             if not caps_df.empty:
                  caps_df['MonthlyCap'] = caps_df['MonthlyCap'].fillna(caps_df['DailyCap'] * 30)
            
        edited_caps_df = st.data_editor(
            caps_df, 
            num_rows="dynamic",
            column_config={
                "DailyCap": st.column_config.NumberColumn("Daily Cap ($)", help="The daily earning limit", min_value=0, step=10, required=False),
                "MonthlyCap": st.column_config.NumberColumn("Monthly Cap ($)", help="The total monthly budget", min_value=0, step=100, required=False)
            },
            hide_index=True
        )
        
        if st.button("Save Changes"):
            updated_caps = edited_caps_df.to_dict(orient='records')
            cleaned_caps = []
            for item in updated_caps:
                for k in ['DailyCap', 'MonthlyCap']:
                    val = item.get(k)
                    if pd.isna(val):
                        item[k] = None
                cleaned_caps.append(item)
                
            save_caps(cleaned_caps, selected_caps_file)
            st.success(f"Saved to {selected_caps_file}!")
            st.rerun()

    if 'selected_caps_file' in locals():
         caps = load_caps(selected_caps_file)

    # Map mapping
    df['MappedPartner'] = df['Advertiser Name'].apply(lambda x: map_partner_name(str(x), caps))
    
    # --- Google Ads Spend Configuration ---
    with st.expander("Manage Google Ads Spend Data"):
        st.info("📊 Upload your Google Ads daily spend CSV.")
        
        col_spend1, col_spend2 = st.columns([2, 1])
        
        with col_spend1:
            ad_spend_files = list_firestore_docs('ad_spend')
            ad_spend_files.sort()
            
            if ad_spend_files:
                last_selected_spend = config.get('last_selected_ad_spend')
                default_spend_index = 0
                if last_selected_spend in ad_spend_files:
                    default_spend_index = ad_spend_files.index(last_selected_spend)
                
                selected_spend_file = st.selectbox("Select Ad Spend File", ad_spend_files, index=default_spend_index)
                
                if selected_spend_file != last_selected_spend:
                    config['last_selected_ad_spend'] = selected_spend_file
                    save_config(config)
            else:
                st.warning("No ad spend files found.")
                selected_spend_file = None
        
        with col_spend2:
            uploaded_spend = st.file_uploader("Upload Ad Spend CSV", type=['csv'], key="spend_upload")
            if uploaded_spend:
                csv_cont = uploaded_spend.getvalue().decode('utf-8')
                db.collection('ad_spend').document(uploaded_spend.name).set({'csv_data': csv_cont})
                st.toast(f"Uploaded {uploaded_spend.name}")
                st.rerun()
        
        if ad_spend_files:
            with st.expander("Rename Ad Spend File"):
                new_spend_name = st.text_input("New Spend File Name", value=selected_spend_file)
                if st.button("Rename Spend File"):
                    if new_spend_name and new_spend_name != selected_spend_file and new_spend_name.endswith('.csv'):
                        if new_spend_name in ad_spend_files:
                            st.error("File with that name already exists!")
                        else:
                            try:
                                old_doc = db.collection('ad_spend').document(selected_spend_file).get()
                                db.collection('ad_spend').document(new_spend_name).set(old_doc.to_dict())
                                db.collection('ad_spend').document(selected_spend_file).delete()
                                st.success(f"Renamed to {new_spend_name}")
                                config['last_selected_ad_spend'] = new_spend_name
                                save_config(config)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error renaming: {e}")
                    elif not new_spend_name.endswith('.csv'):
                        st.error("Filename must end with .csv")
            
            with st.expander("Delete Ad Spend File"):
                st.write(f"Delete **{selected_spend_file}**?")
                if st.button("Delete Spend File", type="primary"):
                    st.session_state.confirm_delete_spend = True
                
                if st.session_state.get('confirm_delete_spend'):
                    st.warning("Are you sure?")
                    if st.button("Confirm Delete Spend File", type="primary"):
                        try:
                            db.collection('ad_spend').document(selected_spend_file).delete()
                            st.success(f"Deleted {selected_spend_file}")
                            if config.get('last_selected_ad_spend') == selected_spend_file:
                                del config['last_selected_ad_spend']
                                save_config(config)
                            del st.session_state.confirm_delete_spend
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting: {e}")
        
        st.markdown("---")
        st.subheader("💱 Currency Settings")
        
        default_rate = config.get('ils_to_usd_rate', 3.6)
        
        col_rate1, col_rate2 = st.columns([3, 1])
        with col_rate1:
            exchange_rate = st.number_input(
                "ILS to USD Exchange Rate (₪ to $)",
                min_value=0.1, max_value=10.0, value=float(default_rate), step=0.1
            )
        
        with col_rate2:
            if st.button("Save Rate"):
                config['ils_to_usd_rate'] = exchange_rate
                save_config(config)
                st.success("Saved!")
                st.rerun()
        
        st.caption(f"Current rate: ₪{exchange_rate} = $1.00 USD")
    
    ad_spend_df = pd.DataFrame()
    if 'selected_spend_file' in locals() and selected_spend_file:
        exchange_rate = config.get('ils_to_usd_rate', 3.6)
        ad_spend_df = load_ad_spend(selected_spend_file, ils_to_usd_rate=exchange_rate)
        if not ad_spend_df.empty:
            st.success(f"✅ Loaded ad spend data: {len(ad_spend_df)} days")
    
    # --- Sidebar Controls ---
    st.sidebar.header("Settings")
    
    all_partners = sorted(df['MappedPartner'].unique())
    selected_partners = st.sidebar.multiselect("Select Partners", options=all_partners, default=all_partners)
    
    show_limits = st.sidebar.toggle("Show Daily Limits", value=False)
    
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )

    # --- Filtering ---
    filtered_df = df[df['MappedPartner'].isin(selected_partners)]
    
    days_in_range = 30
    if len(date_range) == 2:
        start_date, end_date = date_range
        days_in_range = (end_date - start_date).days + 1
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    if filtered_df.empty:
        st.warning("No data available for the selected partners.")
        return

    # --- Visualization ---
    
    # 1. Daily Earnings Chart
    st.subheader("Daily Earnings")
    fig = px.scatter(
        filtered_df, x='Date', y='Earnings', color='MappedPartner',
        title='Daily Earnings by Partner',
        labels={'MappedPartner': 'Partner', 'Earnings': 'Earnings ($)', 'EPC': 'EPC ($)'},
        hover_data={'Advertiser Name': True, 'Earnings': ':.2f', 'EPC': ':.2f', 'MappedPartner': False, 'Date': True}
    )
    fig.update_traces(marker=dict(size=10, opacity=0.8))

    if show_limits:
        caps_dict = {cap['Partner']: cap['DailyCap'] for cap in caps}
        for partner in selected_partners:
            limit = caps_dict.get(partner)
            if limit is not None and limit > 0:
                 fig.add_hline(y=limit, line_dash="dash", annotation_text=f"{partner} Cap: ${limit}", opacity=0.7)
            if limit == 0:
                 fig.add_hline(y=limit, line_dash="dot", annotation_text=f"{partner} Paused", line_color="red", opacity=0.5)

    st.plotly_chart(fig, use_container_width=True)

    # 1.2 Daily Clicks Chart
    st.subheader("Daily Clicks")
    fig_clicks_daily = px.line(
        filtered_df, x='Date', y='Clicks', color='MappedPartner',
        title='Daily Clicks by Partner', markers=True
    )
    st.plotly_chart(fig_clicks_daily, use_container_width=True)

    # 1.5 EPC Trends Chart
    st.subheader("EPC Trends")
    fig_epc = px.line(
        filtered_df, x='Date', y='EPC', color='MappedPartner',
        title='Daily EPC by Partner', markers=True
    )
    st.plotly_chart(fig_epc, use_container_width=True)
    
    # 1.6 Partner Performance
    st.subheader("Partner Performance")
    partner_perf = filtered_df.groupby('MappedPartner')[['Clicks', 'Earnings']].sum().reset_index()
    partner_perf['Overall EPC'] = partner_perf.apply(
        lambda row: row['Earnings'] / row['Clicks'] if row['Clicks'] > 0 else 0, axis=1
    )
    
    col1, col2 = st.columns(2)
    with col1:
        fig_clicks = px.bar(partner_perf, x='MappedPartner', y='Clicks', title='Total Clicks by Partner', text_auto=True)
        st.plotly_chart(fig_clicks, use_container_width=True)
    with col2:
        fig_partner_epc = px.bar(partner_perf, x='MappedPartner', y='Overall EPC', title='Overall EPC by Partner', text_auto='.2f')
        st.plotly_chart(fig_partner_epc, use_container_width=True)
    
    # --- Profit Margin Analysis ---
    if not ad_spend_df.empty:
        st.subheader("💰 Profit Margin Analysis")
        daily_earnings = filtered_df.groupby('Date')['Earnings'].sum().reset_index()
        profit_df = daily_earnings.merge(ad_spend_df, on='Date', how='left')
        profit_df['Spend'] = profit_df['Spend'].fillna(0)
        profit_df['Profit'] = profit_df['Earnings'] - profit_df['Spend']
        profit_df['Profit Margin %'] = profit_df.apply(
            lambda row: (row['Profit'] / row['Earnings'] * 100) if row['Earnings'] > 0 else 0, axis=1
        )
        
        total_earnings = profit_df['Earnings'].sum()
        total_spend = profit_df['Spend'].sum()
        total_profit = profit_df['Profit'].sum()
        total_profit_margin = (total_profit / total_earnings * 100) if total_earnings > 0 else 0
        
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1: st.metric("💵 Total Earnings", f"${total_earnings:,.2f}")
        with col_p2: st.metric("💸 Total Ad Spend", f"${total_spend:,.2f}")
        with col_p3: st.metric("💰 Total Profit", f"${total_profit:,.2f}", f"{total_profit_margin:.1f}% margin", "normal" if total_profit >= 0 else "inverse")
        with col_p4: st.metric("📊 Profit Margin", f"{total_profit_margin:.1f}%")
        
        st.subheader("Daily Profit/Loss")
        fig_profit = go.Figure()
        fig_profit.add_trace(go.Scatter(x=profit_df['Date'], y=profit_df['Earnings'], mode='lines+markers', name='Earnings', line=dict(color='#2ecc71')))
        fig_profit.add_trace(go.Scatter(x=profit_df['Date'], y=profit_df['Spend'], mode='lines+markers', name='Ad Spend', line=dict(color='#e74c3c')))
        colors = ['#27ae60' if p >= 0 else '#c0392b' for p in profit_df['Profit']]
        fig_profit.add_trace(go.Bar(x=profit_df['Date'], y=profit_df['Profit'], name='Profit', marker_color=colors, opacity=0.6))
        fig_profit.update_layout(title='Daily Earnings, Spend, and Profit', barmode='overlay')
        st.plotly_chart(fig_profit, use_container_width=True)
        
        st.subheader("Profit Margin % Over Time")
        fig_margin = px.line(profit_df, x='Date', y='Profit Margin %', title='Daily Profit Margin Percentage', markers=True)
        fig_margin.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even")
        fig_margin.add_hline(y=total_profit_margin, line_dash="dot", line_color="blue", annotation_text=f"Avg: {total_profit_margin:.1f}%")
        fig_margin.update_traces(line=dict(color='#27ae60'))
        st.plotly_chart(fig_margin, use_container_width=True)
        
        with st.expander("View Profit/Loss Details by Day"):
            display_profit_df = profit_df.copy()
            display_profit_df['Date'] = display_profit_df['Date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_profit_df[['Date', 'Earnings', 'Spend', 'Profit', 'Profit Margin %']], use_container_width=True)
    else:
        st.info("📊 Upload Google Ads spend data to view profit margin analysis.")
    
    # 2. Monthly Budget Analysis
    st.subheader("Budget Analysis (Actual vs Expected)")
    actual_spend = filtered_df.groupby('MappedPartner')['Earnings'].sum().reset_index()
    actual_spend.rename(columns={'Earnings': 'Actual Spend'}, inplace=True)
    
    caps_df_lookup = pd.DataFrame(caps)
    if 'MonthlyCap' not in caps_df_lookup.columns: 
         if not caps_df_lookup.empty:
              caps_df_lookup['MonthlyCap'] = caps_df_lookup['DailyCap'] * 30
    else:
         if not caps_df_lookup.empty:
              caps_df_lookup['MonthlyCap'] = caps_df_lookup['MonthlyCap'].fillna(caps_df_lookup['DailyCap'] * 30)

    budget_data = []
    for partner in selected_partners:
        actual = actual_spend[actual_spend['MappedPartner'] == partner]['Actual Spend'].sum()
        cap_row = caps_df_lookup[caps_df_lookup['Partner'] == partner] if not caps_df_lookup.empty else pd.DataFrame()
        monthly_cap = cap_row['MonthlyCap'].values[0] if not cap_row.empty else None
        
        expected = 0
        if monthly_cap is not None and not pd.isna(monthly_cap):
            expected = (days_in_range / 30.0) * monthly_cap
            
        budget_data.append({
            'Partner': partner, 'Actual Spend': actual, 'Expected Spend': expected, 'Monthly Cap': monthly_cap
        })
        
    budget_df = pd.DataFrame(budget_data)
    if not budget_df.empty:
        budget_melted = budget_df.melt(id_vars='Partner', value_vars=['Actual Spend', 'Expected Spend', 'Monthly Cap'], var_name='Type', value_name='Amount')
        fig_bar = px.bar(budget_melted, x='Partner', y='Amount', color='Type', barmode='group', title=f"Budget Utilization over {days_in_range} days", text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Total Utilization Analysis")
        total_actual = budget_df['Actual Spend'].sum()
        total_expected = budget_df['Expected Spend'].sum()
        total_cap = budget_df['Monthly Cap'].sum()
        util_pct = (total_actual / total_expected * 100) if total_expected > 0 else 0
        
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
             st.metric("Utilization (Actual vs Expected)", f"{util_pct:.1f}%", f"{total_actual - total_expected:,.2f} USD")
        
        summary_df = pd.DataFrame([
            {'Metric': 'Total Actual Spend', 'Amount': total_actual},
            {'Metric': 'Total Expected Spend', 'Amount': total_expected},
            {'Metric': 'Total Monthly Budget', 'Amount': total_cap}
        ])
        fig_summary = px.bar(summary_df, x='Metric', y='Amount', color='Metric', title=f"Total Budget Overview ({len(selected_partners)} Partners Selected)", text_auto='.2s')
        st.plotly_chart(fig_summary, use_container_width=True)
    
    with st.expander("Show Source Data"):
        st.dataframe(filtered_df[['Date', 'Advertiser Name', 'MappedPartner', 'Earnings']])

if __name__ == "__main__":
    main()
