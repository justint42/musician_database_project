from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["musician"]

def simple_query():
    # Retrieve all songs from the album "Echoes of Tomorrow"
    album_name = "Echoes of Tomorrow"
    album = db.AlbumCollection.find_one({"albumName": album_name})
    if album:
        songs = list(db.SongCollection.find({"albumID": album["albumID"]}))
        print("Songs from the album 'Echoes of Tomorrow':")
        for song in songs:
            print(song)
    else:
        print("Album not found")

def complex_query():
    # Find all products that are of type "Apparel" and have sold more than 20 units
    products = list(db.Products.find({
        "type": "Apparel",
        "units_sold": {"$gt": 20}
    }))
    print("Products of type 'Apparel' with more than 20 units sold:")
    for product in products:
        print(product)

def aggregate_query():
    # Calculate the total revenue generated from music products
    pipeline = [
        {"$match": {"type": "Music"}},
        {
            "$group": {
                "_id": None,
                "totalRevenue": {
                    "$sum": {"$multiply": ["$price", "$units_sold"]}
                }
            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(db.Products.aggregate(pipeline))
    if result:
        total_revenue = result[0]["totalRevenue"]
        print(f"Total revenue generated from music products: ${total_revenue:.2f}")
    else:
        print("No music products found.")

# Function calls
simple_query()
complex_query()
aggregate_query()
