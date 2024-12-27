from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.conf import settings
# Create your views here.
def test(request):
    return HttpResponse("Test successful")


SEARCH_QUERY = "Python programming"
YOUTUBE_API_KEY='AIzaSyA7G6upmtoIMRF1cnmcfHv6c0Ou8-YwiA4'
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def fetch_videos(request):
    params = {
            "part": "snippet",
            "q": SEARCH_QUERY,
            "type": "video",
            "order": "date",
            "maxResults": 5,
            "key": YOUTUBE_API_KEY,
        }
    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])
        print("\nLatest Videos:")
        for video in videos:
            snippet = video["snippet"]
            print(f"- Title: {snippet['title']}")
            print(f"  Description: {snippet['description']}")
            print(f"  Published At: {snippet['publishedAt']}")
            print(f"  Thumbnail URL: {snippet['thumbnails']['default']['url']}\n")
    else:
        print(f"Error fetching videos: {response.status_code}, {response.text}")
    return HttpResponse("Fetched videos")