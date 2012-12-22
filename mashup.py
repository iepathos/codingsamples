#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script gets the Popular Music Artists through Yahoo Search API
# Then gets all of the albums for each artist through LastFM API
# Then outputs all of the information in json format.
# Information is a url to a medium-sized image for each album,
# each album's name and each album's playcount.
# The whole script executes in less than 30 seconds.
# This script was written in response to a coding challenge
# issued by Saffron Digital for a python web development position.
#
# Script written by Glen Baker - iepathos@gmail.com

###############################################

""" THREADING FOR PARALLEL URL REQUESTS """
from threading import Thread
from urllib import urlopen
from time import sleep, time

UPDATE_INTERVAL = 0.01

class URLThread(Thread):
    def __init__(self,url):
        super(URLThread, self).__init__()
        self.url = url
        self.response = None

    def run(self):
        self.request = urlopen(self.url)
        self.response = self.request.read()

def multi_get(uris,timeout=2.0):
    def alive_count(lst):
        alive = map(lambda x : 1 if x.isAlive() else 0, lst)
        return reduce(lambda a,b : a + b, alive)
    threads = [ URLThread(uri) for uri in uris ]
    for thread in threads:
        thread.start()
    while alive_count(threads) > 0 and timeout > 0.0:
        timeout = timeout - UPDATE_INTERVAL
        sleep(UPDATE_INTERVAL)
    return [ (x.url, x.response) for x in threads ]

###############################################

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import json

# Yahoo Search for popular music Artists
def GetPopularArtists():
    """ Returns a dictionary of all of the Popular Artists from Yahoo
        topartists = { u'artist': '' } """
    #  yql = select * from music.artist.popular(0) gets all of them
    # URL for Yahoo Search RESTful API
    data = urllib2.urlopen('http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20music.artist.popular(0)&diagnostics=true').read()
    soup = BeautifulSoup(data)
    topartists = {}
    for artist in soup.findAll('artist'):
        topartists[artist['name']] = ''
    if topartists == {}:
        print 'Error 503, Yahoo Search API failed to return the requested information'
    else:
        return topartists

def GetLastFMURLS(artists):
    """ Takes list of artists, returns list of LastFM album api urls """
    # my lastfm testing api key
    api_key = '26ab03cd0a155dea863e4249d2329199'
    albumurls = []
    for artist in artists:
        albumurls.append('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=' + artist.encode('utf-8', 'replace').replace(' ', '%20') + '&api_key=' + api_key)
    print 'Retrieved all album urls at ' + str(time())
    return albumurls

def GetAlbums(artists):    
    urls = GetLastFMURLS(artists)
    """ HERE IS THE SCRIPT'S NETWORK CHOKE POINT """
    print 'We\'re waiting 10 seconds for LastFM\'s response'
    print 'because it is a lot of data and we have time.'
    print 'Time requirement for script is < 30 seconds.'
    requests = multi_get(urls,timeout=10) # Threaded url requests
    print 'Retrieved all artist albums from LastFM'
    artistsalbums = {}
    for url, data in requests:
        for artist in artists:
            if bool(re.search(artist.encode('utf-8', 'replace').replace(' ', '%20'), str(url))):
                print 'Sorting albums for ' + artist
                image_medium_links = []
                album_names = []
                album_playcounts = []
                albumslist = {}
                data = str(data) # quick fix for soup buffer error
                soup = BeautifulSoup(data)
                
                """ HERE IS THE SCRIPT'S DATA PROCESSING CHOKE POINT """
                # I can speed all of this data processing up with multiprocessing, but it's already fast
                
                # Find all album medium sized image links
                for link in soup.findAll(lambda tag: tag.name=='image' and tag.has_key('size') and str(tag['size']) == 'medium'):
                    image_url = str(link)[21:-8] # slice off image tags and attributes
                    image_medium_links.append(image_url)

                # Find all album names    
                for name in soup.findAll('name')[::2]:
                    album_name = str(name)[6:-7]  # slice off name tags
                    album_names.append(album_name)
        
                # Find all album playcounts
                for album in soup.findAll('playcount'):
                    playcount = str(album)[11:-12] # slice off playcount tags
                    album_playcounts.append(playcount)
                    
                # Now insert values from image_medium_links, album_names, and album_playcounts
                # into artist_albums dictionary                   
                for i in range(0, len(album_names)):
                    albumslist[i] = {'image_medium': image_medium_links[i], 'name': album_names[i], 'playcount': album_playcounts[i]}

                artistsalbums[artist.encode('utf-8', 'replace')] = albumslist
            
    print json.dumps(artistsalbums, sort_keys=True, indent=4, separators=(',', ': '))

# json will format roughly to:
#   {
#       "artist"
#       "albums":
#       {
#           "image_medium": 'url'
#           "name": 'album name'
#           "playcount": 'playcount'
#       },
#   }

if __name__ == '__main__':
    start = time()
    print 'Script start time: ' + str(time())
    print 'Getting Popular Artists from Yahoo...'
    topartists = {}
    topartists = GetPopularArtists()
    print 'Retrieved all popular artists at ' + str(time())
    # print topartists
    print 'Retrieving albums for all artists from LastFM at ' + str(time())
    GetAlbums(topartists)
    print 'Script began at ' + str(start)
    print 'Script concluded at ' + str(time())
    print 'Total script time = ' + str(time() - start)
