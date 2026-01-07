import json
import os
import pymongo
from dotenv import load_dotenv

# 1. Kết nối MongoDB
load_dotenv()
MONGO_URL = os.getenv('MONGO_URL') # Lấy link từ file .env
if not MONGO_URL:
    print("❌ Lỗi: Chưa có MONGO_URL trong file .env")
    exit()

client = pymongo.MongoClient(MONGO_URL)
db = client["DiscordBotDB"]
ranks_col = db["user_ranks"]

# 2. Đọc file JSON cũ trên máy
try:
    with open("user_ranks.json", "r", encoding="utf-8") as f:
        old_data = json.load(f)
except FileNotFoundError:
    print("❌ Không tìm thấy file user_ranks.json")
    exit()

# 3. Đẩy lên MongoDB
count = 0
for user_id, stats in old_data.items():
    # Cấu trúc mới trên Mongo: _id là user_id, data là stats
    ranks_col.update_one(
        {"_id": str(user_id)}, 
        {"$set": {"data": stats}}, 
        upsert=True
    )
    count += 1

print(f"✅ Đã chuyển thành công {count} người dùng lên MongoDB!")