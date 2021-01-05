from apiclient.discovery import build
from apiclient.errors import HttpError
import pandas as pd
import pprint
import matplotlib.pyplot as pd

from pymongo import MongoClient

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q, max_results=10,order="viewCount", token=None, location='40.730610, -73.935242', location_radius='50km'):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=q,type="video",pageToken=token,order = order,part="id,snippet",maxResults=max_results,location=location,locationRadius=location_radius).ex$
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []
    client = MongoClient()
    print("Connected")
    db=client['final-project']
    collection=db['youtube-collection']
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            title.append(search_result['snippet']['title'])

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(part='statistics, snippet',id=search_result['id']['videoId']).execute()
            for data in response['items']:
                print(data['snippet']['title'])
                if data['statistics']['likeCount']:
                    print(data['statistics']['likeCount'])
                channelTitle.append(data['snippet']['channelTitle'])
                favoriteCount.append(data['statistics']['favoriteCount'])
                viewCount.append(data['statistics']['viewCount'])
                if 'likeCount' in data['statistics']:
                    likeCount.append(data['statistics']['likeCount'])
                if 'dislikeCount' in data['statistics']:
                    dislikeCount.append(data['statistics']['dislikeCount'])
                if 'commentCount' in data['statistics']:
                    commentCount.append(data['statistics']['commentCount'])
                if 'likeCount' in data['statistics'] and 'dislikeCount' in data['statistics'] and 'viewCount' in data['statistics'] and 'commentCount' in data['statistics']:
                        collection.insert({'channelTitle':data['snippet']['channelTitle'],
                                  'title': search_result['snippet']['title'],
                                  'viewCount':data['statistics']['viewCount'],
                                  'likeCount':data['statistics']['likeCount'],
                                  'dislikeCount':data['statistics']['dislikeCount'],
                                  'commentCount':data['statistics']['commentCount']})
    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,$
    # print(youtube_dict)
    return youtube_dict
some_dict = youtube_search("Corona")
print(some_dict)
some_dict['viewCount'] = list(map(int, some_dict['viewCount']))
some_dict['likeCount'] = list(map(int, some_dict['likeCount']))
some_dict['dislikeCount'] = list(map(int, some_dict['dislikeCount']))
# print(type(some_dict['likeCount'][0]))
avg_views = sum(some_dict['viewCount'])/len(some_dict['viewCount'])
l_dl_ratio = avg_likes / avg_dislikes
v_l_ratio = avg_likes / avg_views
print("Average views were",avg_views,"Average likes were",avg_likes,"and average dislikes were",avg_dislikes)
print("Response Rate (Likes to views ratio) was",v_l_ratio)
print("Ratio of likes and dislikes is",l_dl_ratio)
