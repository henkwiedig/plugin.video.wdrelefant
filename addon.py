import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import urllib, json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')

elefanturl = "http://www.wdrmaus.de/elefantenseite/data/app_video_json.php5"
sections = {'0' : "Anke",
           '1' : "Bobo Siebenschlaefer",
           '2' : "Elefantenkino",
           '3' : "Geschichten",
           '4' : "Lieder",
           '5' : "Raetsel",
           '6' : "Tanja und Adre",
}

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:

    response = urllib.urlopen(elefanturl)
    data = json.loads(response.read())

    print json.dumps(data,indent=1)

    for section in data["clips"]:
        if section == '':
            continue
        url = build_url({'mode': 'section', 'sectionid': section})
        li = xbmcgui.ListItem(sections[section], iconImage='DefaultFolder.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'section':
    section = args['sectionid'][0]

    response = urllib.urlopen(elefanturl)
    data = json.loads(response.read())

    for video in data["clips"][section]:
        url = build_url({'mode': 'video', 'zmdbVideoURL': video["video"]["zmdbVideoURL"], 'title': unicode(video["title"]).encode('utf8')})
        li = xbmcgui.ListItem( video["title"], iconImage='http://www.wdrmaus.de/elefantenseite/' + video["thumbnails"][0]["url"])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'video':
    zmdbVideoURL = args['zmdbVideoURL'][0]
    title = args['title'][0]

    response = urllib.urlopen(zmdbVideoURL)
    data = json.loads(response.read().split('(')[1].split(')')[0])
    m3uurl = data["mediaResource"]["alt"]["videoURL"]
    listItem = xbmcgui.ListItem(title, path=m3uurl)
     
    xbmc.Player().play(item=m3uurl, listitem=listItem)




