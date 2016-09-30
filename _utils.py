import urllib
import urllib2
import socket
import xbmc
def getUrl(url):
	xbmc.log(url)

	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	return link
	