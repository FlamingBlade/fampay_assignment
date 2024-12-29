from django.urls import path
from . import views
urlpatterns = [
    path('test',views.test),
    path('start',views.start_fetching_videos),
    path('fetch',views.get_videos),
    path('stop',views.stop_fetching),
    path('search',views.search_videos),
    path('delete',views.delete_videos)
]

