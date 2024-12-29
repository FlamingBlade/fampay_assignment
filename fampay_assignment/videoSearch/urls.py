from django.urls import path
from . import views
urlpatterns = [
    path('test',views.test),
    path('yt',views.fetch_videos),
    path('gt',views.get_videos)

]

