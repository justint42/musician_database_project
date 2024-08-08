# import the relevant modules

import json
from pymongo import MongoClient
from bson import json_util

def load_data(filepath, collection_name):
    try:
        # Establish a connection to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['musician']
        collection = db[collection_name]

        # For project purposes and to ensure data load accuracy, clear db before loading data
        collection.delete_many({})

        # Open and load data from the JSON files (within mongodb folder)
        with open(filepath, 'r') as file:
            data = json.load(file, object_hook=json_util.object_hook)

            # Insert data into the collection
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)

        print(f"{filepath} data has been loaded into the '{collection_name}' collection.")

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is not valid.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    try:
        # Establish mongoDb connection
        client = MongoClient('mongodb://localhost:27017/')

        # Drop the entire musician database to start fresh
        client.drop_database('musician')
        print("Database 'musician' has been dropped.")

        # Load data into collections
        load_data('AlbumCollection.json', 'AlbumCollection')
        load_data('Creatives.json', 'Creatives')
        load_data('Products.json', 'Products')
        load_data('SocialMedia.json', 'SocialMedia')
        load_data('SongCollection.json', 'SongCollection')
        load_data('StreamingPlatforms.json', 'StreamingPlatforms')

        print("Data has been successfully imported into MongoDB!")

    except Exception as e:
        print(f"An error occurred during setup: {e}")
