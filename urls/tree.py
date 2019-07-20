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


class Crawler():
    def __init__(self, max_depth = 0, parse_base = False ,verbose = False):
        self.max_depth = max_depth
        self.parse_base = parse_base
        self.verbose = verbose
        self.urls = list()
        self.urls_inner = list()
        self.urls_outer = list()
            
    ## get urls recursivelly
    def recursiveUrl(self, url, link, depth):
        try:
            shref = link['href']
            if not 'http' in shref and not 'www' in shref:
                url_shref = urljoin(url, shref) 
            else:
                url_shref = shref
            if self.verbose: print('url_shref:',url_shref)
            if not url_shref in self.urls: self.urls.append(url_shref)
        except:
            print('hay error', url, shref)
            return   
        
        if depth == self.max_depth:
            return
        else:
            page = requests.get(url_shref)
            soup = BeautifulSoup(page.text, 'html.parser')
            newlink = soup.find('a')   
            if newlink is None or len(newlink) == 0:
                return
            else:
                self.recursiveUrl(url, newlink, depth + 1)
    
    ## get links
    def getLinks(self, url):
        url_base = get_base_url(url)
        if self.parse_base: url = url_base
        if self.verbose: print('url', url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            self.recursiveUrl(url, link, 0)

        self.urls_outer = sorted(list(set([get_base_url(exclude_self(l, url_base, 1)) for l in set(self.urls) if not exclude_self(l, url_base, 1) is None])))
        self.urls_inner = sorted(list(set([exclude_self(l, url_base, 2) for l in set(self.urls) if not exclude_self(l, url_base, 2) is None])))


def main():
    url = "https://jmquintana79.github.io/tech/2016/09/04/a-enviroment-to-develop-with-a-linux-os-and-awesome-wm.html"
    crw = Crawler(max_depth = 1, parse_base = True, verbose = False)
    crw.getLinks(url)
    print('--> all:',len(crw.urls), crw.urls)
    print('--> inner:',len(crw.urls_inner), crw.urls_inner)
    print('--> outer:',len(crw.urls_outer), crw.urls_outer)
    
    
if __name__ == '__main__':
    main()