# SI507 Final Project

Main code: final_proj.py

### Step1: get API keys for Yelp Fusio and Google Maps Place  
* #### Yelp Fusion API Key:
  * Go to "https://www.yelp.com/developers/documentation/v3/authentication" and generate app and get API key.
  * Key is already included in the main code
  * Assign to YelpApiKey in the final_proj.py
* #### Google Maps Place: Please see the final report to find the api key and use it
  * Go to "https://developers.google.com/maps/documentation/places/web-service/get-api-key" to get API key, it may take up to 48 hours
  * or Please find my key in the final project report
  * Assign it to googleApiKey in the final_proj.py
 _____________
 
### Step2: Package list
  * requests
  * googlemaps
  * pandas
  * numpy
  * matplotlib
  * mplcursors
  * webbrowser
---------------
### Step3: Run final_proj.py
  * The program will ask you a city (eg. Chicago) you want to find restaurants and foodtype you want to eat(eg. American)
  * Then it will find restaurants on Yelp and search and match with google to give you recommendation
  * Recommend criteria:
    * Over 500 reviews and 4.0 rating on Yelp
    * Over 1000 reviews and 4.5 rating on Google
    * Rating diffrence between Yelp and Google < 0.2
  * The program will show the distributino and suggestions
  * You will select the restaurant to check whether on Yelp or Google
  * The code will automacically open the restaurant page
 
 
