#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:20:30 2019

@author: admin

Source: https://stackoverflow.com/questions/46629681/how-to-find-recursively-all-links-from-a-webpage-with-beautifulsoup
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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


## get urls recursivelly
def recursiveUrl(url, link, depth, max_depth, verbose):
    if depth == max_depth:
        return url
    else:
        try:
            shref = link['href']
            if not 'http' in shref or not 'www' in shref:
                url_shref = url + shref
            else:
                url_shref = shref
            if verbose: print('url_shref:',url_shref)
            page = requests.get(url_shref)
            soup = BeautifulSoup(page.text, 'html.parser')
            newlink = soup.find('a')
        except:
            return url
   
        if newlink is None or len(newlink) == 0:
            return link
        else:
            return link, recursiveUrl(url, newlink, depth + 1, max_depth, verbose)

## get links
def getLinks(url, max_depth = 1, parse_base = False ,verbose = False):
    assert max_depth > 0, 'the max depth cannot be 0.'
    if parse_base: url = get_base_url(url)
    if verbose: print('url', url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        links.append(recursiveUrl(url, link, 0, max_depth, verbose))
    return links


def main():
    url = "https://jmquintana79.github.io/tech/2016/09/04/a-enviroment-to-develop-with-a-linux-os-and-awesome-wm.html"
    links = getLinks(url, parse_base = True, verbose = True)
    print(links)
    
    
if __name__ == '__main__':
    main()