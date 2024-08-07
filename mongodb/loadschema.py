import json
from pymongo import MongoClient
from bson import json_util

def load_data(filepath, collection_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']
    collection = db[collection_name]

    collection.delete_many({})

    with open(filepath, 'r') as file:
        data = json.load(file, object_hook=json_util.object_hook)

        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)

if __name__ == '__main__':
    load_data('AlbumCollection.json', 'albums')


# Load data into collections
load_data('AlbumCollection.json', 'albums')
load_data('ArtistTeam.json', 'team_members')
load_data('Merchandise.json', 'merchandise')
load_data('SocialMedia.json', 'social_media_platforms')
load_data('SongCollection.json', 'songs')
load_data('StreamingPlatforms.json', 'streaming_platforms')
load_data('Venues.json', 'venues')

print("Data has been successfully imported into MongoDB!")
