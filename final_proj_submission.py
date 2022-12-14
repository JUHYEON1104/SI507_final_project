import requests
import json
import googlemaps
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.patches import Rectangle
import webbrowser
import os

def search_stores():
    YelpApiKey='Cqekjd4kRbOCsMosH6xZR3iZfecl0IG8fHLqOi5ysav8BQPcw5YhQHAlCfqevARVYW0IfCdkZwVVlF4SipJyIUgspvgQWUxC0Mv0IOXpXoT-_YrFKqoaE991EceWY3Yx'
    headers = {'Authorization': 'Bearer %s' % YelpApiKey}
    while True:
        location = input('what city you want to search?')
        foodtype = input('what kind of food you want to eat?')

        if os.path.exists(location+'_'+foodtype+'_'+'YelpResult.json'):
            cache_flag = True
            # print('found cache data')
            f = open(location+'_'+foodtype+'_'+'YelpResult.json',"r")
            sample_data = json.loads(f.read())
            f.close()
            return sample_data, location, foodtype

        url='https://api.yelp.com/v3/businesses/search'
        params = {f'term':foodtype,'location':location,'limit': 50}
        # Making a get request to the API
        req=requests.get(url, params=params, headers=headers)
        print('The status code is {}'.format(req.status_code))
        if req.status_code == 200:
                print('list is loaded')
                break
        # proceed only if the status code is 200
        else:
            print('Please search again')
    return json.loads(req.text)['businesses'], location, foodtype


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

data, Location, Foodtype = search_stores()
# Load Cache
if os.path.exists(Location+'_'+Foodtype+'_'+'YelpResult.json'):
    print('Found Cache Data')
    SaerchedStores= [Stores(None,data[i]) for i in range(len(data))]
else:
    SaerchedStores = [Stores(data[i],None) for i in range(len(data))]

def google_search(name,city):
    googleApiKey = 'Please replace here with your API key'
    gmaps = googlemaps.Client(key=googleApiKey)
    place_details = gmaps.places(name+' in '+city+' + restaurant')
    # print(f'google saerch with',name+' in '+city+' + restaurant') #print part for debugging
    # place_details['results']
    return place_details['results']

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

google_results = []
if os.path.exists(Location+'_'+Foodtype+'_'+'googleResult.json'):
        print('found cache')
        cache_flag = True
        # print('found cache data')
        f = open(Location+'_'+Foodtype+'_'+'googleResult.json',"r")
        data = json.loads(f.read())
        f.close()
        google_results = []
        google_results = [google_stores(None,data[i]) for i in range(len(data))]
else:
        for i in range(len(data)):
                google_results.append(google_stores(google_search(SaerchedStores[i].name,SaerchedStores[i].City)[0]))

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

# Caching
googlejsonstr = json.dumps([StoreTree[i].google.__dict__ for i in range(len(StoreTree))])
yelpjsonstr = json.dumps([StoreTree[i].yelp.__dict__ for i in range(len(StoreTree))])
with open(Location+'_'+Foodtype+'_'+'googleResult.json', 'w') as f:
    f.write(googlejsonstr)
with open(Location+'_'+Foodtype+'_'+'YelpResult.json', 'w') as f:
    f.write(yelpjsonstr)

storeNames = [StoreTree[i].root for i in range(len(StoreTree))]
googleRatings = [float(StoreTree[i].google.Rating) for i in range(len(StoreTree))]
googleReviewCounts = [StoreTree[i].google.ReviewCount for i in range(len(StoreTree))]
yelpRatings = [float(StoreTree[i].yelp.Rating) for i in range(len(StoreTree))]
yelpReviewCounts = [StoreTree[i].yelp.ReviewCount for i in range(len(StoreTree))]
yelpurl = [StoreTree[i].yelp.url for i in range(len(StoreTree))]

def Grading(each,ratingmin = 0, RCmin = 0):
    if each.Rating >= ratingmin and each.ReviewCount >= RCmin:
        return True
    else:
        return False
def filtering(each,yelpRmin,yelpRCmin,googleRmin,googleRCmin,absdiff):
    return Grading(each.yelp,yelpRmin,yelpRCmin) and Grading(each.google,googleRmin,googleRCmin) and abs(each.yelp.Rating-each.google.Rating) < absdiff

yelpRmin = 4
yelpRCmin = 500
googleRmin = 4.5
googleRCmin = 1000
absdiff = 0.2
recommend_list = []
for i in range(len(StoreTree)):
    StoreTree[i].recommend = filtering(StoreTree[i],yelpRmin,yelpRCmin,googleRmin,googleRCmin,absdiff)
    if StoreTree[i].recommend:
        recommend_list.append(StoreTree[i])
    # print(StoreTree[i].recommend)




rect1 = Rectangle((googleRmin-0.05,yelpRmin-0.05),(5-googleRmin+0.1),(5-yelpRmin+0.1),fill = False,color = 'red')
rect2 = Rectangle((googleRCmin,yelpRCmin),(max(googleReviewCounts)-googleRCmin),(max(yelpReviewCounts)-yelpRCmin),fill = False,color = 'red')
plt.figure(figsize = (10,5))


plt.subplot(1,2,1)
plt.scatter(googleRatings,yelpRatings)
plt.xlabel('Google Ratings')
plt.ylabel('Yelp Ratings')
plt.title('Rating distribution')
plt.gca().add_patch(rect1)
plt.xlim((2.9,5.1))
plt.ylim((2.9,5.1))
plt.subplot(1,2,2)
plt.scatter(googleReviewCounts,yelpReviewCounts)
plt.gca().add_patch(rect2)
plt.title('Number of review distribution')
plt.xlabel('Google number of reviews')
plt.ylabel('Yelp number of reviews')
plt.xscale("log")
plt.yscale("log")

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.8,
                    wspace=0.4,
                    hspace=0.2)
# plt.suptitle(recommend_list[0].yelp.Categories[0]['title']+' Restaurants in '+recommend_list[0].yelp.City+'\n Rating and Review Counts Distribution',fontsize = 13)
plt.suptitle(Foodtype+' Restaurants in '+Location+'\n Rating and Review Counts Distribution',fontsize = 13)
mplcursors.cursor(hover=True)

plt.figure(figsize = (16,8))

for i in range(len(recommend_list)):
    plt.subplot(2,len(recommend_list),i+1)
    plt.bar([0], height =[recommend_list[i].yelp.Rating],color = 'orangered')
    plt.bar([1], height =[recommend_list[i].google.Rating],color = 'royalblue')
    plt.xticks([0,1], ['Yelp', 'Google'])
    plt.title(str(i+1)+'\n'+recommend_list[i].yelp.name + '\n (Rating)')
    plt.ylim([4,5])

    plt.subplot(2,len(recommend_list),len(recommend_list)+i+1)
    plt.bar([0], height =[recommend_list[i].yelp.ReviewCount],color = 'limegreen')
    plt.bar([1], height =[recommend_list[i].google.ReviewCount],color = 'gold')
    plt.xticks([0,1], ['Yelp', 'Google'])
    plt.title('(Number of Reviews)')
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.88,
                    wspace=0.4,
                    hspace=0.2)
plt.suptitle('Recommended '+Foodtype+' Restaurants in '+Location,fontsize = 13)
mplcursors.cursor(hover=True)
plt.show()
select = input('which one you want to check?')

while True:
    select2 = input('yelp or google?')
    if select2 == 'yelp':
        webbrowser.open(recommend_list[int(select)-1].yelp.url)
        break
    elif select2 == 'google':
        googleurl = 'https://www.google.com/search?q='+Location+'+'+recommend_list[int(select)-1].google.name+'&newwindow=1&rls=com.microsoft%3Aen-US%3A%7Breferrer%3Asource%3F%7D&rlz=1I7ADRA_ko&sxsrf=ALiCzsbSx296QNdQ0i_kZd_YkNEbI7Ty_A%3A1671045624095&ei=-CGaY4muBfri2roP9ZCCgAU&ved=0ahUKEwiJis-G6vn7AhV6sVYBHXWIAFAQ4dUDCA8&uact=5&oq=chicago+The+dearborn&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCAAQgAQQDTIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjoGCAAQBxAeOggIABAIEAcQHkoECEEYAEoECEYYAFAAWK4FYPQGaABwAXgAgAFziAHEBZIBAzMuNJgBAKABAcABAQ&sclient=gws-wiz-serp'
        webbrowser.open(googleurl)
        break
    else:
        print('select google or yelp')