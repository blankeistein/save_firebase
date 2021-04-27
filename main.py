import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

cred = credentials.Certificate('maiacomic-fc4c1-firebase-adminsdk-s1jtf-c2db2c3f73.json')

firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://maiacomic-fc4c1-default-rtdb.firebaseio.com'
})

dump_data_collection = {
    "cover": "https://someimage.com/image.jpg",
    "timestamp": int(datetime.now().timestamp()),
    "slug": "slug",
    "title": "sitle"
  }

dump_data_history = {
    "cover": "https://someimage.com/image.jpg",
    "last_read": "something last read",
    "slug": "slug",
    "collection": "terbaru_sekali, favorite",
    "title": "sitle"
  }

# Create Collection
def create_collection(slug, name):
  try:
    ref = db.reference(f"collection/{slug}")
    collection_slug = name.lower().replace(" ", "_")
    data = {collection_slug: name}
    ref.update(data)
  except:
    return False

# Add Comic in Collection and update collection in history
def push_comic_to_collection(slug, collection, data):
  try:
    ref = db.reference(f"data/{slug}/{collection}")
    ref.update({data["slug"]: data})
    
    data = get_comic_history(f"{slug}", data["slug"])
    if collection not in data["collection"]:
      data["collection"] = f"{data['collection']},collection"
    
    ref = db.reference(f"history/{slug}/{data['slug']}")
    ref.update({data["slug"]: data})
  except:
    return False

# GET list comic in collection
# order by : title, timestamp
def get_comic_from_collection(slug, collection, order="timestamp"):
  try:
    ref = db.reference(f"data/{slug}/{collection}")
    temp = ref.order_by_child(f"{order}").get()
    
    data = dict()
    for key, item in temp.items():
      data.update({key: item})

    return data
  except:
    return False

# Record History
def push_comic_to_history(slug, data):
  try:
    ref = db.reference(f"history/{slug}")
    ref.update(data)
  except:
    return False

# Get Data history comic
def get_comic_history(slug, comic):
  try:
    ref = db.reference(f"history/{slug}/{comic}")
    data = ref.get()

    return data
  except:
    return False

if __name__ == "__main__":
  # create_collection("komiku", "Terbaru Sekali")
  # push_comic("komiku", "terbaru_sekali", dump_data)
  # get_comic_from_collection("komiku", "terbaru_sekali", "timestamp")
  pass

