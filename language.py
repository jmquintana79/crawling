#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:52:34 2019

@author: admin
"""
from langdetect import detect

def main(text:str)->str:
    return detect(text)

if __name__ == "__main__":
    text = 'Estás son las cascadas cerca de Kobe.. Me dijo mi mujer , que de Kyoto a Kobe es más de 1 hora en tren normal , pero que si tenéis JRail pasa podéis ir en Shinkasen en un tris.. además , la estación de Shinkasen en Kobe es Shin-Kobe, muy cerca de las cataratas y del barrio europeo . Es muy conveniente.'
    language = main(text)
    print(language)