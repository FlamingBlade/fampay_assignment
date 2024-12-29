from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from django.conf import settings
from .models import YouTubeVideo
# import YouTubeVideo
# Create your views here.
def test(request):
    return HttpResponse("Test successful")

def get_videos(request):
    videos=YouTubeVideo.objects.all()
    videos_result=[]
    for video in videos:
       video_data = {
            "title": video.title,
            "channel_title": video.channel_title,
            "description": video.description,
            "published_at": video.published_at,
            "thumbnail_url": video.thumbnail_default_url, 
        }
       videos_result.append(video_data)
    return JsonResponse({"videos": videos_result})

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
        videos_data = response.json().get("items", [])
        # print(videos[0])
        # videoList=[]
        for video in videos_data:
            snippet = video.get('snippet', {})
            thumbnails = snippet.get('thumbnails', {})
            YouTubeVideo.objects.create(
                kind=video.get('kind', ''),
                etag=video.get('etag', ''),
                video_id=video['id'].get('videoId', ''),
                published_at=snippet.get('publishedAt', ''),
                channel_id=snippet.get('channelId', ''),
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                thumbnail_default_url=thumbnails.get('default', {}).get('url', ''),
                thumbnail_default_width=thumbnails.get('default', {}).get('width', 0),
                thumbnail_default_height=thumbnails.get('default', {}).get('height', 0),
                thumbnail_medium_url=thumbnails.get('medium', {}).get('url', ''),
                thumbnail_medium_width=thumbnails.get('medium', {}).get('width', 0),
                thumbnail_medium_height=thumbnails.get('medium', {}).get('height', 0),
                thumbnail_high_url=thumbnails.get('high', {}).get('url', ''),
                thumbnail_high_width=thumbnails.get('high', {}).get('width', 0),
                thumbnail_high_height=thumbnails.get('high', {}).get('height', 0),
                channel_title=snippet.get('channelTitle', ''),
                live_broadcast_content=snippet.get('liveBroadcastContent', ''),
                publish_time=snippet.get('publishTime', ''),
            )
        # for video in videos:
        #     # videoList.append(Yout)
        #     snippet = video["snippet"]
        #     print(f"- Title: {snippet['title']}")
        #     print(f"  Description: {snippet['description']}")
        #     print(f"  Published At: {snippet['publishedAt']}")
        #     print(f"  Thumbnail URL: {snippet['thumbnails']['default']['url']}\n")
    else:
        print(f"Error fetching videos: {response.status_code}, {response.text}")
    return HttpResponse("Fetched videos")