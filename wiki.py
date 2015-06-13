from BeautifulSoup import BeautifulSoup
import urllib2

def wiki(term,peer,search,cursor,cnxn): # wiki <search term>
    'Returns a wiki link and the first paragraph of the page'

    main_page = 'http://en.wikipedia.org/wiki/Main_Page'
    print "Going to fetch wiki of %s" % term
    wlink = term # notice the trailing space
    if 1 == len(wlink): # no search term given, the Main_Page is "displayed"
        response = main_page
    else:
        #search_term = wlink[1].lstrip().replace(' ', '_')
        search_term = wlink.replace(' ', '_')
        #print search_term

        if len(search_term) < 1:
            response = main_page
        else:
            response = 'http://en.wikipedia.org/wiki/' + search_term

    response1 = response + ',' + get_para(response)
    print response
    
    if ("Cannot acces link!" in response1):
      return response
    
    else:
      
      cursor.execute("insert into dbo.search_result(search_id, user_id, result, result_desc, link) values ( ?, ?, ?, ?, ?)", search, peer, term, get_para(response), response)
      cnxn.commit() 
      
      cursor.execute(""" UPDATE dbo.bot_search_querry SET flag = 1 where search_id = ?""", [search])
      cnxn.commit()
      print "else inside"
      return None

def get_para(wlink):
    'Gets the first paragraph from a wiki link'

    msg = ''
    try:
        page_request = urllib2.Request(wlink)
        page_request.add_header('User-agent', 'Mozilla/5.0')
        page = urllib2.urlopen(page_request)
    except IOError:
        msg = 'Cannot acces link!'
    else:

        soup = BeautifulSoup(page)
        msg = ''.join(soup.find('div', { 'id' : 'bodyContent'}).p.findAll(text=True))

        while 460 < len(msg): # the paragraph cannot be longer than 510
            # characters including the protocol command
            pos = msg.rfind('.')
            msg = msg[:pos]

    return msg
