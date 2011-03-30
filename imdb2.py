#!/usr/bin/env python

#
# ImdbRating
# Laszlo Szathmary, 2011 (jabba.laci@gmail.com)
#
# Project's home page: 
# https://pythonadventures.wordpress.com/2011/03/25/get-the-imdb-rating-of-a-movie/
#
# Version: 0.1 
# Date:    2011-03-25 (yyyy-mm-dd)
#
# Inspired by the script of Rag Sagar:
# https://ragsagar.wordpress.com/2010/11/20/python-script-to-find-imdb-rating/
#
# This free software is copyleft licensed under the same terms as Python, or,
# at your option, under version 2 of the GPL license.
#

import os
import sys
import re
import urllib
import urlparse

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

class ImdbRating:
    # title of the movie
    title = None
    # IMDB URL of the movie
    url = None
    # IMDB rating of the movie
    rating = None
    # Did we find a result?
    found = False
    
    # constant
    BASE_URL = 'http://www.imdb.com'
    
    def __init__(self, title):
        self.title = title
        self._process()
        
    def _process(self):
        movie = '+'.join(self.title.split())
        br = Browser()
        url = "%s/find?s=tt&q=%s" % (self.BASE_URL, movie)
        br.open(url)

        if re.search(r'/title/tt.*', br.geturl()):
            self.url = "%s://%s%s" % urlparse.urlparse(br.geturl())[:3]
            soup = BeautifulSoup( MyOpener().open(url).read() )
        else:
            link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
            res = br.follow_link(link)
            self.url = urlparse.urljoin(self.BASE_URL, link.url)
            soup = BeautifulSoup(res.read())

        try:
            self.title = soup.find('h1').contents[0].strip()
            self.rating = soup.find('span',attrs='rating-rating').contents[0]
            self.found = True
        except:
            pass

# class ImdbRating

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s 'Movie title'" % (sys.argv[0])
    else:
        imdb = ImdbRating(sys.argv[1])
        if imdb.found:
            print imdb.url
            print imdb.title
            print imdb.rating

