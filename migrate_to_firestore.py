import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.Certificate('qmp-partner-portal-2026-firebase-adminsdk-fbsvc-c45407ee13.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# 1. Migrate config
if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config_data = json.load(f)
        db.collection('config').document('app_config').set(config_data)
        print("Config migrated.")

# 2. Migrate caps
if os.path.exists('caps'):
    for filename in os.listdir('caps'):
        if filename.endswith('.json'):
            with open(os.path.join('caps', filename), 'r') as f:
                caps_data = json.load(f)
                db.collection('caps').document(filename).set({'data': caps_data})
                print(f"Cap {filename} migrated.")

# 3. Migrate reports
if os.path.exists('reports'):
    for filename in os.listdir('reports'):
        if filename.endswith('.csv'):
            with open(os.path.join('reports', filename), 'r') as f:
                csv_content = f.read()
                db.collection('reports').document(filename).set({'csv_data': csv_content})
                print(f"Report {filename} migrated.")

# 4. Migrate ad_spend
if os.path.exists('ad_spend'):
    for filename in os.listdir('ad_spend'):
        if filename.endswith('.csv'):
            with open(os.path.join('ad_spend', filename), 'r') as f:
                csv_content = f.read()
                db.collection('ad_spend').document(filename).set({'csv_data': csv_content})
                print(f"Ad Spend {filename} migrated.")

print("Migration complete!")
