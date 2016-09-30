# -*- coding: utf-8 -*-
import libMediathek
import xbmc
import xbmcplugin
import xbmcgui
import json
import re
import _utils#todo: move to lib

base = 'https://www.funk.net'

def main():
	libMediathek.addEntry({'name':'Formate', 'mode':'listFormats', 'type': 'dir'})
	libMediathek.addEntry({'name':'Serien',  'mode':'listShows',   'type': 'dir'})
	
def listFormats():
	response = _utils.getUrl('https://www.funk.net/formate')
	main = response.split('<section id="formate" class="whiteDark">')[-1]
	
	#shows = re.compile('<div style=".+?" class="large-3 medium-6 small-12 columns show-more-item">(.+?)</a>', re.DOTALL).findall(main)
	shows = re.compile('class="large-3 medium-6 small-12 columns show-more-item">(.+?)</a>', re.DOTALL).findall(main)
	
	l = []
	for show in shows:
		d = {}
		d['url'] = base + re.compile('<a href="(.+?)"', re.DOTALL).findall(show)[0]
		d['name'] = re.compile('<h2 class="video_thumbnail_text">(.+?)<', re.DOTALL).findall(show)[0]
		d['thumb'] = re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(show)[0]
		d['type'] = 'dir'
		d['mode'] = 'listVideos'
		l.append(d)
		
	libMediathek.addEntries(l)
	
def listShows():
	response = _utils.getUrl('https://www.funk.net/serien')
	
	shows = re.compile('<div class="slide-inner">(.+?)</a>', re.DOTALL).findall(response)
	l = []
	for show in shows:
		d = {}
		d['url'] = base + re.compile('<a href="(.+?)"', re.DOTALL).findall(show)[0]
		d['name'] = re.compile('<h2 class="ellipsis_line">(.+?)<', re.DOTALL).findall(show)[0]
		d['thumb'] = re.compile('<img.+?src="(.+?)"', re.DOTALL).findall(show)[0]
		d['type'] = 'dir'
		d['mode'] = 'listVideos'
		l.append(d)
	libMediathek.addEntries(l)
	
def listVideos():
	response = _utils.getUrl(params['url'])
	videos = response.split('<div style="display: block;" class="large-3 medium-6 small-12 columns show-more-item">')[1:]
	l = []
	for video in videos:
		#xbmc.log(video)
		d = {}
		u = 'https://cdnapisec.kaltura.com/html5/html5lib/v2.47/mwEmbedFrame.php?&wid=_1985051&uiconf_id=35472181&entry_id='
		d['url'] = u + re.compile("renderPlayer\('.+?', '(.+?)'\)", re.DOTALL).findall(video)[0]
		d['name'] = re.compile('<h2.+?>(.+?)<', re.DOTALL).findall(video)[0]
		d['thumb'] = re.compile('<img.+?data-src="(.+?)"', re.DOTALL).findall(video)[0]
		d['type'] = 'video'
		d['mode'] = 'play'
		l.append(d)
	libMediathek.addEntries(l)
		
	
def list():
	response = _utils.getUrl(params['url'])
	j = json.loads(response)
	l = []
	for video in j['videos']:
		d = {}
		d['name'] = video['title']
		d['epoch'] = video['datesec']
		d['thumb'] = video['image_ipad'][:-10] + str(int(video['image_ipad'][-10:-4]) - 1) + video['image_ipad'][-4:]
		d['url'] = 'http://www.phoenix.de/php/mediaplayer/data/beitrags_details.php?ak=web&id=' + str(video['id'])
		d['mode'] = 'play'
		d['type'] = 'video'
		l.append(d)
		
	libMediathek.addEntries(l)
	
def play():
	response = _utils.getUrl(params['url'])
	details = re.compile('window.kalturaIframePackageData = (.+?);', re.DOTALL).findall(response)[0]
	xbmc.log(details)
	j = json.loads(details)
	flavorIds = ''
	for flavorAsset in j['entryResult']['contextData']['flavorAssets']:
		flavorIds += flavorAsset['id'] + ','
	entryId = j['playerConfig']['entryId']
	videoUrl = 'https://cdnapisec.kaltura.com/p/1985051/sp/198505100/playManifest/entryId/1_1902tyg6/format/url/protocol/https'
	#videoUrl = 'https://cdnapisec.kaltura.com/p/1985051/sp/198505100/playManifest/entryId/1_1902tyg6/flavorIds/1_zk1myx9f,1_bwuxxmjr,1_vecakz4m,1_lnth4dx7/format/applehttp/protocol/https/a.m3u8?referrer=aHR0cHM6Ly93d3cuZnVuay5uZXQ='
	videoUrl = 'https://cdnapisec.kaltura.com/p/1985051/sp/198505100/playManifest/entryId/'+entryId+'/flavorIds/'+flavorIds[:-1]+'/format/applehttp/protocol/https/a.m3u8'
	videoUrl += '?referrer=aHR0cHM6Ly93d3cuZnVuay5uZXQ='
	#videoUrl += '&playSessionId=5a6c13d1-0ec8-1cb4-ea4e-4b89ab5791e3'
	#videoUrl += '&clientTag=html5:v2.47'
	#videoUrl += '&uiConfId=35472181'
	#videoUrl += '&responseFormat=jsonp'
	#videoUrl += '&callback=jQuery1111023988482763819396_1475251230056'
	#videoUrl += '&_=1475251230057'
	xbmc.log(videoUrl)
	response = _utils.getUrl(params['url'])
	xbmc.log(response)
	listitem = xbmcgui.ListItem(path=videoUrl)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


modes = {
'main': main,
'listFormats': listFormats,
'listShows': listShows,
'listVideos': listVideos,
'play': play
}	
def list():	
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	
	if not params.has_key('mode'):
		main()
	else:
		modes.get(params['mode'],main)()
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
list()