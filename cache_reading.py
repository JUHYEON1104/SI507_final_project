import json

f = open('Chicago_American_YelpResult.json',"r")
data = json.loads(f.read())
f.close()

class Stores:
    def __init__(self, data=None, json = None):
        if json == None:
            self.name = data['name']
            self.ReviewCount =data ['review_count']
            self.Categories = data['categories']
            self.Rating = data['rating']
            self.Lat = data['coordinates']['latitude']
            self.Long = data['coordinates']['longitude']
            self.Address = data['location']['address1']
            self.City = data['location']['city']
            self.Location = data['location']
            self.Phone = data['phone']
            self.url = data['url']
            # if data['price']
            # self.price = data['price']
            # self.recommend = None
        else:
            self.name = json['name']
            self.ReviewCount =json ['ReviewCount']
            self.Categories = json['Categories']
            self.Rating = json['Rating']
            self.Lat = json['Lat']
            self.Long = json['Long']
            self.Address = json['Address']
            self.City = json['City']
            self.Location = json['Location']
            self.Phone = json['Phone']
            self.url = json['url']

# Load Cache

SaerchedStores= [Stores(None,data[i]) for i in range(len(data))]

class google_stores():
    def __init__(self,data,json = None):
        if json is None:
                self.name = data['name']
                self.Rating = data['rating']
            # self.price_level = data['price_level']
                self.ReviewCount = data['user_ratings_total']
        else:
                self.name = json['name']
                self.Rating = json['Rating']
            # self.price_level = data['price_level']
                self.ReviewCount = json['ReviewCount']

f = open('Chicago_American_googleResult.json',"r")
data = json.loads(f.read())
f.close()
google_results = []
google_results = [google_stores(None,data[i]) for i in range(len(data))]

class Tree:
    def __init__(self,root):
        self.root = root
        self.google = None
        self.yelp = None
        self.recommend = False

# Build Tree Structure
StoreTree = [Tree(SaerchedStores[i].name)for i in range(len(data))]
for i in range(len(data)):
    StoreTree[i].google = google_results[i]
    StoreTree[i].yelp = SaerchedStores[i]

print('google data')
print(StoreTree[0].google.__dict__)
print('yelp data')
print(StoreTree[0].yelp.__dict__)

