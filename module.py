from ytsearch import youtubeSearch
from bot import db_connect

def querry(mesage,peer,search,cursor,cnxn): 
  result = youtubeSearch(mesage)
  # db_connect()
  #global db.connect.cursor
  #global cnxn
  
  if result != "video not found":
    for i in result:
      a=i.split(",")
      #print a
      #int1++
      title = "TiTTle : "+a[0]
      link = "Link : "+a[1]
      desc = "Description : "+a[2]
      print title+"\n"+link+"\n"+desc+"\n"
      try:
	cursor.execute("insert into dbo.search_result(search_id, user_id, result, result_desc, link) values ( ?, ?, ?, ?, ?)", search, peer, title, desc, link)
	
      except:
	print "except"
    cnxn.commit() 
     
  else:
    print"else"
    cursor.execute("insert into dbo.search_result(search_id, user_id, result) values ( ?, ?, ?)", search, peer, result)
    cnxn.commit()
  
  cursor.execute(""" UPDATE dbo.bot_search_querry SET flag = 1 where search_id = ?""", [search])
  cnxn.commit()
  return None

"""def db_connect():
    global cursor
    global cnxn
    dsn = 'sqlserverdatasource'
    user = 'sa'
    password = 'credance'
    database = 'howzat'
 
    con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, user, password, database)
    cnxn = pyodbc.connect(con_string)
    cursor = cnxn.cursor()"""