import requests
from requests import post
import base64
import json
import time


# function to generate a certain number of related artists based on initial artist name and number provided
def getAPI(artist_name):
  params = {
    'q': artist_name,
    'type': 'artist',
    'limit': '1'
  }
  # first api request from Spotify search API 
  response1 = requests.get('https://api.spotify.com/v1/search?q=' + artist_name + '&type=artist&market=us&limit=50&offset=0', params=params, headers=headers).json()
  # get artist ID from search API
  artist_id = response1["artists"]["items"][0]["id"]
  # second api request from Spotify Related Artist API (using ID from initial api)
  response2 = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/related-artists', headers=headers).json()
  
  return response2["artists"]
    
 # get artist names from api
def getNames(artist_name, number):
  rec_artists_names = []
  if(number <= 10):
    for i in range (0, int(number)):
      rec_artists_names.append(getAPI(artist_name)[i]["name"])
    return rec_artists_names
  else:
    return []

# get artist genres from api
def getGenres(artist_name, number):
  rec_artists_genres = []
  for i in range (0, int(number)):
    rec_artists_genres.append(getAPI(artist_name)[i]["genres"])
  return rec_artists_genres

# get artist images from api
def getImages(artist_name, number):
  rec_artists_images = []
  for i in range (0, int(number)):
    rec_artists_images.append(getAPI(artist_name)[i]["images"][0]["url"])
  return rec_artists_images

# get artist links from api
def getLinks(artist_name, number):
  rec_artists_links = []
  for i in range (0, int(number)):
    rec_artists_links.append(getAPI(artist_name)[i]["external_urls"]["spotify"])
  return rec_artists_links

      


# client id, client secret, and grant type for spotify api access token
client_id ='602549ec66af4e47aeabc02f756f53ff'
client_secret ='e3f7c536999840349f84244978753173'

data = {
    'grant_type': 'client_credentials',
    'client_id': '602549ec66af4e47aeabc02f756f53ff',
    'client_secret': 'e3f7c536999840349f84244978753173',
}

# code to generate refresh token to access spotify api
token_expiration_time = 0
access_token = ""


def get_token():
  global token_expiration_time, access_token
  current_time = int(time.time())

  # Check if a valid token is available and hasn't expired yet
  if 'access_token' in globals() and token_expiration_time > current_time:
    return access_token

  # If the token is not available or has expired, request a new one
  auth_string = client_id + ':' + client_secret
  auth_bytes = auth_string.encode('utf-8')
  auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

  url = "https://accounts.spotify.com/api/token"
  headers = {
      'Authorization': 'Basic ' + auth_base64,
      'Content-Type': 'application/x-www-form-urlencoded'
  }
  data = {'grant_type': 'client_credentials'}

  result = post(url, headers=headers, data=data)
  json_result = json.loads(result.content)
  access_token = json_result['access_token']

  # Calculate the expiration time of the new token (default is 3600 seconds)
  token_expiration_time = current_time + json_result.get('expires_in', 3600)

  return access_token

# code to get refresh token and add it into headers (for spotify api)
token = get_token()
bearer = "Bearer " + token
headers = {'Authorization': bearer}



  
