from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db['albums']

# Get the top 5 best-selling merchandise items
def find_top_selling_merchandise(db):
    print("\nTop-Selling Merchandise Items:")
    top_selling = db['merchandise'].find().sort("stock_count", -1).limit(5)
    for item in top_selling:
        print(f"Item: {item['name']}, Sold: {item['stock_count']}")

# Find aggregate total streams by album
def total_streams_by_album(db):
    print("\nTotal Streams by Album:")
    pipeline = [
        {"$group": {
            "_id": "$album_id",
            "total_streams": {"$sum": "$streams.count"}
        }},
        {"$sort": {"total_streams": -1}}
    ]
    results = db['songs'].aggregate(pipeline)
    for result in results:
        print(f"Album ID: {result['_id']}, Total Streams: {result['total_streams']}")

# Find low-stock merchandise items
def find_low_stock_merchandise(db, stock_threshold):
    print(f"\nMerch Items with Stock Count Below {stock_threshold}:")
    low_stock_items = db['merchandise'].find({"stock_count": {"$lt": stock_threshold}})
    for item in low_stock_items:
        print(f"Item: {item['name']}, Stock Count: {item['stock_count']}")

# Example function calls
find_top_selling_merchandise(db)
total_streams_by_album(db)
find_low_stock_merchandise(db, 50)


