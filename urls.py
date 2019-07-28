#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:20:30 2019

@author: admin

Source: https://stackoverflow.com/questions/46629681/how-to-find-recursively-all-links-from-a-webpage-with-beautifulsoup
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import posixpath


stop_domains = ['facebook', 'twitter', 'linkedin', 'github.com', 'plus.google', 'telegram.org', 'getpocket', 'mailto']
stop_extensions = [".pptx", ".ppt", ".xls", ".xlsx", ".xml", ".xlt", ".pdf", ".jpg", ".png", ".svg", ".doc", ".docx", ".pps", ".jpg", ".png"]
only_domains = []
only_extensions = []


def exclude_self(url, response_url, mode):
    # mode 1 = Outer url
    if mode == 1:
        if response_url not in url:
            return url
    # mode 2 = Inner url
    elif mode == 2:
        if response_url in url:
            return url

def clean(url):
    # regex to check valid url
    regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    try:
        u = regex.match(url).group()
        # print "%s valid url" % u
        return u
    except:
        # return "not valid url"
        pass

def clean_www(url):
    if 'www.' in url:
        return url.replace('www.', '')
    else:
        return url

def get_base_url(url):
    if url != "":
        u = urlparse(url)
        return "%s://%s" % (u.scheme, u.netloc)
    else:
        return ""
     
def get_norm_url( url, module = posixpath ):
    return module.normpath( url )


## url crawler
class Crawler():
    """
    url crawler.
    
    Attributes defined here:
        
        url_base -- base of input url.    
        urls_inner -- internal urls of the url target.
        urls_outer -- external urls in website of the url target.
    """
    ## constructor
    def __init__(self, max_depth:bool = 0, is_parse_base:bool = False, is_return_base:bool = False ,verbose:bool = False):
        """
        constructor.  
        max_depth -- maximum depth to parse (default 0).
        is_parse_base -- parse the base of input url or not (default False).
        is_return_base -- return the base of output url outer or not (default False).
        verbose -- display extra information or not (default False).
        """
        self._max_depth = max_depth
        self._is_parse_base = is_parse_base
        self._is_return_base = is_return_base
        self._verbose = verbose
        self.url_base = None
        self.urls_inner = list()
        self.urls_outer = list()
            
    ## get urls recursivelly
    def _recursiveUrl(self, url:str, link:str, depth:int):
        try:
            # get href element
            shref = link['href']
            # build final url
            if not 'http' in shref and not 'www' in shref:
                url_shref = urljoin(url, shref) 
            else:
                url_shref = shref
            # cleaning
            url_shref = clean(url_shref)
            # display
            if self._verbose: print('url_shref:',url_shref)
            
            ## append rules
            # if it is already available
            if url_shref in self.urls_inner: return
            if self._is_return_base: 
                if get_base_url(url_shref) in self.urls_outer: return
            else:
                if url_shref in self.urls_outer: return
            # stop domains
            if len([i for i in stop_domains if i in url_shref])>0: return
            # stop extension
            if len([i for i in stop_extensions if i in url_shref])>0: return
            # only domains
            if len(only_domains)>0:
                if len([i for i in only_domains if i in url_shref])==0: return
            # only extension
            if len(only_extensions)>0:
                if len([i for i in only_extensions if i in url_shref])==0: return
                
            ## append
            if self.url_base in url_shref:
                # inner url: append and continuous
                self.urls_inner.append(url_shref)
            else:
                # outer: append and no continous
                if self._is_return_base: self.urls_outer.append(get_base_url(url_shref))
                else: self.urls_outer.append(url_shref) 
                return
        except:
            if self._verbose: print('[warning] there are any error getting the href element:', link)
            return   
        
        if depth == self._max_depth:
            return
        else:
            page = requests.get(url_shref)
            soup = BeautifulSoup(page.text, 'html.parser')
            newlink = soup.find('a')   
            if newlink is None or len(newlink) == 0:
                return
            else:
                self._recursiveUrl(url, newlink, depth + 1)
    
    ## get urls
    def get_urls(self, url:str):
        """
        Get urls recursively.
        url -- url to be parsed.
        """
        self.url_base = get_base_url(url)
        if self._is_parse_base: url = self.url_base
        if self._verbose: print('url', url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            self._recursiveUrl(url, link, 0)
            

def main():
    from datetime import datetime
    # current time
    tic = datetime.now()
    # main
    url = "https://jmquintana79.github.io/tech/2016/09/04/a-enviroment-to-develop-with-a-linux-os-and-awesome-wm.html"
    crw = Crawler(max_depth = 1, is_parse_base = True, is_return_base = True, verbose = False)
    crw.get_urls(url)
    print('--> inner:',len(crw.urls_inner), crw.urls_inner)
    print('--> outer:',len(crw.urls_outer), crw.urls_outer)
    # counting spending time
    toc = datetime.now()
    tictoc = ((toc-tic).seconds)/60. # minutes
    print ("\nProcess start: %s"%tic)
    print ("Process finish: %s"%toc)
    print ("Process time spent %s minutes"%tictoc)
    # return 
    return    
    
if __name__ == '__main__':
    main()