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


DEV_KEY = "AIzaSyDRQ4_A-5YXMFluXDZUofTnMcW27TFG03I"
API_NAME = "youtube"
API_VERSION= "v3"
videos = []

def youtubeSearch(query,filter1='r'):
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
        maxResults=5,
        order=o,
        part="id,snippet",
        q=query
    ).execute()
    #print search_response
    
    for search_result in search_response.get("items", []):
       
        if search_result["id"]["kind"] == "youtube#video":
          url = "http://youtu.be/"+search_result["id"]["videoId"]
          myvid = pafy.new(url)
          duration=str(myvid.duration)
          views=str(myvid.viewcount)
          
          videos.append("%s (%s) %s %s" % (search_result["snippet"]["title"],duration,"Views : "+views,
                                     "http://youtu.be/" +
                                    search_result["id"]["videoId"]))
          
        else:
            return "Video not found."
        
    print "Videos:\n", "\n".join(videos), "\n"
    #return video.encode('ascii', 'ignore')
