# Please note that this requires "Google APIs Clinet Library for Python".
#
# Available from easy_install:
#       $ easy_install --upgrade google-api-python-client
#
# Or available using pip:
#       $ pip install --upgrade google-api-python-client
#
# Depending on your system you may require root privileges
# to install the required library.

import os
import pafy
from apiclient.discovery import build

import timeit


DEV_KEY = "" #developerKey
API_NAME = "youtube"
API_VERSION= "v3"
videos = []

def youtubeSearch(query,filter1='r'):
    start_time = timeit.default_timer()
    if filter1 is 'd':
        o='date'
    if filter1 is 'r':
        o='rating'
    if filter1 is 't':
        o='title'
    if filter1 is 'vd':
        o='videoCount'
    if filter1 is 'vc':
        o='viewCount'
    if filter1 is 'r':
        o='relevance'
        
    youtube = build(API_NAME,
                    API_VERSION,
                    developerKey=DEV_KEY)
    search_response = youtube.search().list(
        maxResults=10,
        order=o,
        part="id,snippet",
        q=query
    ).execute()
    #print search_response
    
    for search_result in search_response.get("items", []):
       
        if search_result["id"]["kind"] == "youtube#video":
          url = "http://youtu.be/"+search_result["id"]["videoId"]
          #myvid = pafy.new(url)
          #duration=str(myvid.duration)
          #views=str(myvid.viewcount)
          
          videos.append("%s,%s,%s" % (search_result["snippet"]["title"],url,search_result["snippet"]["description"]))
          
        else:
            return "video not found"
        
    return videos
    print timeit.default_timer() - start_time, "seconds"
    #return video.encode('ascii', 'ignore')
