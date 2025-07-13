from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DBNAME]
entries_col = db["entries"]

for entry in entries_col.find():
    old_date = entry.get("created_at")
    if old_date and "-" in old_date and ":" in old_date:
        # Convert 'YYYY-MM-DD HH:MM:SS' to 'MM/DD/YYYY'
        try:
            dt = datetime.strptime(old_date[:10], "%Y-%m-%d")
            new_date = dt.strftime("%m/%d/%Y")
            entries_col.update_one(
                {"_id": entry["_id"]},
                {"$set": {"created_at": new_date}}
            )
            print(f"Updated {entry['_id']}: {old_date} -> {new_date}")
        except Exception as e:
            print(f"Error updating {entry['_id']}: {e}")