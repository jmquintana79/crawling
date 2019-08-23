#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:41:41 2019

@author: admin
"""

# parser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

## text parser from a url formatted by sentences.
class Parser():
    '''
    Text parser from a url formatted by sentences.
    url -- url to be parsed.
    isheader -- include headers (default False)
    return -- whole parsed text formatted by sentences.
    '''
    def __init__(self, url:str, isheaders:bool = False):
        self.url = url
        self.isheaders = isheaders
        
    @staticmethod
    def format_parsed(parsed:'bs4.element.ResultSet'):
        return[re.sub('\s+',' ',i.text) if re.sub(' ','',re.sub('\s+',' ',i.text))[-1] == '.' else '%s.'%re.sub('\s+',' ',i.text) for i in parsed if not not re.sub(' ','',re.sub('\s+',' ',i.text))]
    
    def get_text(self):
        # web request
        try:
            req = Request(self.url , headers={'User-Agent': 'Mozilla/5.0'})
            website = urlopen(req).read()
        except Exception as error:
            print('[error] there are some problem parsing "%s".'%self.url)
            print(error)
            return ''
        soup = BeautifulSoup(website, "html.parser")
        # parse components
        parsed_paragraphs = soup.find_all('p')
        if self.isheaders:
            parsed_headers = soup.find_all(re.compile('^h[1-6]$'))
            parsed = self.format_parsed(parsed_headers) + self.format_parsed(parsed_paragraphs)
        else:
            parsed = self.format_parsed(parsed_paragraphs)
        # return joinned list as a string
        return ' '.join(parsed)
    
    
if __name__ == '__main__':
    url = 'https://resuelvetudeuda.com/segundas-oportunidades/'
    parser = Parser(url, True)
    text = parser.get_text().translate(str.maketrans(' ', ' ', '!"“”#$%&\'()*+/:;<=>?@[\\]^_`{|}~'))
    print(text)