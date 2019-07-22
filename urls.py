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



class Crawler():
    def __init__(self, max_depth = 0, parse_base = False ,verbose = False):
        self.max_depth = max_depth
        self.parse_base = parse_base
        self.verbose = verbose
        self.urls = list()
        self.urls_inner = list()
        self.urls_outer = list()
        self.url_base = None
            
    ## get urls recursivelly
    def recursiveUrl(self, url, link, depth):
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
            if self.verbose: print('url_shref:',url_shref)
            ## append rules
            # if it is already available
            if url_shref in self.urls: return
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
            # append and continuous
            self.urls.append(url_shref)
        except:
            if self.verbose: print('[warning] there are any error getting the href element:', link)
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
    
    ## get urls
    def get_urls(self, url):
        self.url_base = get_base_url(url)
        if self.parse_base: url = self.url_base
        if self.verbose: print('url', url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            self.recursiveUrl(url, link, 0)
            
    ## get outer urls
    def get_urls_outer(self):
        assert len(self.urls) > 0, "urls have to be collected previously."
        self.urls_outer = sorted(list(set([get_base_url(exclude_self(l, self.url_base, 1)) for l in set(self.urls) if not exclude_self(l, self.url_base, 1) is None])))

    ## get outer urls
    def get_urls_inner(self):
        assert len(self.urls) > 0, "urls have to be collected previously."
        self.urls_inner =  sorted(list(set([exclude_self(l, self.url_base, 2) for l in set(self.urls) if not exclude_self(l, self.url_base, 2) is None])))


def main():
    url = "https://jmquintana79.github.io/tech/2016/09/04/a-enviroment-to-develop-with-a-linux-os-and-awesome-wm.html"
    crw = Crawler(max_depth = 0, parse_base = False, verbose = False)
    crw.get_urls(url)
    print('--> all:',len(crw.urls), crw.urls)
    crw.get_urls_inner()
    crw.get_urls_outer()
    print('--> inner:',len(crw.urls_inner), crw.urls_inner)
    print('--> outer:',len(crw.urls_outer), crw.urls_outer)
    
    
if __name__ == '__main__':
    main()