from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests,threading,time
from django.core.paginator import Paginator
from django.conf import settings
from .models import YouTubeVideo
# import YouTubeVideo
# Create your views here.
SEARCH_QUERY = "Python programming"
fetching_status_flag={}
fetching_events = {}
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
def test(request):
    return HttpResponse("Test successful")
def periodic_fetching(search_query,stop_event):
    YOUTUBE_API_KEYS=getattr(settings,'YOUTUBE_API_KEYS')
    while not stop_event.is_set():
        for key in YOUTUBE_API_KEYS:
            params = {
                    "part": "snippet",
                    "q": search_query,
                    "type": "video",
                    "order": "date",
                    "maxResults": 12,
                    "key": key,
                }            
            response = requests.get(YOUTUBE_API_URL, params=params)
            if response.status_code==403 and 'exhaused' in response.text.lower():
                continue           
            elif response.status_code == 200:
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
                        query=search_query,
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
        time.sleep(10)
def start_fetching_videos(request):
    search_query=request.GET.get('q',SEARCH_QUERY).replace('+',' ')
    if search_query not in fetching_status_flag or fetching_status_flag[search_query] is False:
        stop_event=threading.Event()
        fetching_status_flag[search_query]=True
        fetching_events[search_query]=stop_event
        thread = threading.Thread(target=periodic_fetching,args=(search_query,stop_event))
        thread.daemon = True
        thread.start()
        return HttpResponse("Started fetching videos for "+ search_query)
    else:
        return HttpResponse("Already fetching videos")
def stop_fetching(request):
    search_query=request.GET.get('q',SEARCH_QUERY).replace('+',' ')
    if search_query in fetching_events:
        stop_event=fetching_events[search_query]
        stop_event.set()
        fetching_status_flag[search_query]=False
        print("Stopped fetching videos for"+ search_query)
        return HttpResponse("Stopped fetching videos for "+ search_query)
    else:
        print("Task doesnt exist"+ search_query)
        return HttpResponse("Task doesnt exist"+ search_query)
def get_videos(request):
    page_size = int(request.GET.get('page_size', 3))
    videos = YouTubeVideo.objects.all().order_by('-publish_time')
    paginator = Paginator(videos, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
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
    return JsonResponse({
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_videos": paginator.count,
        "videos": videos_result,
        
    })


    
def search_videos(request):
    query = request.GET.get('q', '').replace('+',' ').strip()
    if query:
        videos = YouTubeVideo.objects.filter(
            title__icontains=query
        ) | YouTubeVideo.objects.filter(
            description__icontains=query
        )
    else:
        videos = YouTubeVideo.objects.none()
    videos_result = []
    for video in videos:
        video_data = {
            "title": video.title,
            "description": video.description,
            "published_at": video.published_at,
            "thumbnail_url": video.thumbnail_default_url, 
        }
        videos_result.append(video_data)

    # Return the filtered videos as a JSON response
    return JsonResponse({
        "videos": videos_result
    })
def delete_videos(request):
    YouTubeVideo.objects.all().delete()
    return HttpResponse("Deleted videos")