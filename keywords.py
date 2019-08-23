#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:55:45 2019

@author: admin
"""
import textacy
import textacy.ke


def main(text, dmodels, snormalize = 'lemma', sngrams = (1,2,3,4,5,6), sinclude_pos=('NOUN', 'PROPN', 'ADJ') , swindow_size = 1500, stopn = 1., sidf = None, verbose = False):
    # identify language
    language = textacy.lang_utils.identify_lang(text)
    if verbose: print('[info] language = "%s"'%language)
    # load language model
    nlp = textacy.load_spacy_lang(dmodels[language], disable=("parser",))
    # create documents
    doc = textacy.make_spacy_doc(text, lang=nlp)
    # model launch
    keywords =textacy.ke.sgrank(doc, 
                               normalize=snormalize, #normalize = None, #normalize = 'lower', 
                               ngrams=sngrams, 
                               include_pos=sinclude_pos, 
                               window_size=swindow_size,
                               topn=stopn, 
                               idf=sidf)  
    # return
    return keywords


if __name__ == "__main__":
    dmodels = {'es':'es_core_news_md', 'en':'en_core_web_md'}
    text = 'Estás son las cascadas cerca de Kobe.. Me dijo mi mujer , que de Kyoto a Kobe es más de 1 hora en tren normal , pero que si tenéis JRail pasa podéis ir en Shinkasen en un tris.. además , la estación de Shinkasen en Kobe es Shin-Kobe, muy cerca de las cataratas y del barrio europeo . Es muy conveniente.'
    keywords = main(text, dmodels, swindow_size = 100, verbose = True)
    print([ik[0] for ik in keywords])