from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyDRQ4_A-5YXMFluXDZUofTnMcW27TFG03I'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
def places(key,user_id,search_id,cursor,cnxn,rad=10000):
  cursor.execute("""select TOP 1 lat,lon from dbo.location where user_id = ?""",[user_id])
  row = cursor.fetchone()
  if row:
    #print row

    lat = row.lat
    lon = row.lon
    loc=lat+","+lon
    print loc
  
  #print loc,key,rad
  try:
    print "try"
    query_result = google_places.nearby_search(location=loc, keyword=key,radius=rad)
  except :
    print "except"
  print "hello"
  if query_result.has_attributions:
      print query_result.html_attributions


  for place in query_result.places:
    # Returned places from a query are place summaries.
      a= place.name
      print a
      lat = str(place.geo_location['lat'])
    
      lon = str(place.geo_location['lng'])
      
      
      
      b= "Link : https://www.google.com/maps@"+lat+","+lon
      print b
    #print place.place_id

    # The following method has to make a further API call.
      try :
	place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    #print place.details # A dict matching the JSON response from Google.
	c = "phone : "+place.local_phone_number
    #print place.international_phone_number
	d = "Website : "+place.website
	e = c+"\n"+d
	
      except:
	e = "Website and Phone number not found"
    #print place.url
      print ("olay"+"\n")
      cursor.execute("insert into dbo.search_result(search_id, user_id, result, result_desc, link) values ( ?, ?, ?, ?, ?)", search_id, user_id, a, e, b)
   
  cnxn.commit()
    # Getting place photos
  print "finish"
  cursor.execute(""" UPDATE dbo.bot_search_querry SET flag = 1 where search_id = ?""", [search_id])
  cnxn.commit()
    #for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        #photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        #photo.mimetype
        # Image URL
        #photo.url
        # Original filename (optional)
        #photo.filename
        # Raw image data
        #photo.data
 
