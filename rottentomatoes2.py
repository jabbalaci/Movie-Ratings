#!/usr/bin/env python

"""Get the rating of a movie on RottenTomatoes.com."""

# RottenTomatoesRating
# Laszlo Szathmary, 2011 (jabba.laci@gmail.com)
#
# Project's home page: 
# https://pythonadventures.wordpress.com/2011/03/26/get-the-rottentomatoes-rating-of-a-movie/
#
# Version: 0.2 
# Date:    2011-03-29 (yyyy-mm-dd)
#
# This free software is copyleft licensed under the same terms as Python, or,
# at your option, under version 2 of the GPL license.

import sys
import re
import urllib
import urlparse

from BeautifulSoup import BeautifulSoup


class MyOpener(urllib.FancyURLopener):
    """Tricking web servers."""
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
    
class RottenTomatoesRating:
    """Get the rating of a movie."""
    # title of the movie
    title = None
    # RT URL of the movie
    url = None
    # RT tomatometer rating of the movie
    tomatometer = None
    # RT audience rating of the movie
    audience = None
    # Did we find a result?
    found = False
    
    # for fetching webpages
    myopener = MyOpener()
    # Should we search and take the first hit?
    search = True
    
    # constant
    BASE_URL = 'http://www.rottentomatoes.com'
    SEARCH_URL = '%s/search/full_search.php?search=' % BASE_URL
    
    def __init__(self, title, search=True):
        self.title = title
        self.search = search
        self._process()
        
    def _search_movie(self):
        """Use RT's own search and return the first hit."""
        movie_url = ""
        
        url = self.SEARCH_URL + self.title
        page = self.myopener.open(url)
        result = re.search(r'(/m/.*)', page.geturl())
        if result:
            # if we are redirected
            movie_url = result.group(1)
        else:
            # if we get a search list
            soup = BeautifulSoup(page.read())
            ul = soup.find('ul', {'id' : 'movie_results_ul'})
            if ul:
                div = ul.find('div', {'class' : 'media_block_content'})
                if div:
                    movie_url = div.find('a', href=True)['href']
                
        return urlparse.urljoin( self.BASE_URL, movie_url )
        
    def _process(self):
        """Start the work."""
        
        # if search option is off, i.e. try to locate the movie directly 
        if not self.search:
            movie = '_'.join(self.title.split())
            
            url = "%s/m/%s" % (self.BASE_URL, movie)
            soup = BeautifulSoup(self.myopener.open(url).read())
            if soup.find('title').contents[0] == "Page Not Found":
                url = self._search_movie()                
        else:
            # if search option is on => use RT's own search
            url = self._search_movie()

        try:
            self.url = url
            soup = BeautifulSoup( self.myopener.open(url).read() )
            self.title = soup.find('meta', {'property' : 'og:title'})['content']
            if self.title:
                self.found = True
            
            self.tomatometer = soup.find('span', {'id' : 'all-critics-meter'}).contents[0]
            self.audience = soup.find('span', {'class' : 'meter popcorn numeric '}).contents[0]
            
            if self.tomatometer.isdigit():
                self.tomatometer += "%"
            if self.audience.isdigit():
                self.audience += "%"
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: %s 'Movie title'" % (sys.argv[0])
    else:
        rt = RottenTomatoesRating(sys.argv[1])
        if rt.found:
            print rt.url
            print rt.title
            print rt.tomatometer
            print rt.audience
