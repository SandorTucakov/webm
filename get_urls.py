import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
from urllib2 import URLError
import time


from lxml import etree
import urllib2
from unidecode import unidecode

def get_urls(start=1, n=100, filename='links_1'):
    lista = []
    for i in range(1, int(np.round(n / 12, 0))):
        lista.append("http://www.webmotors.com.br/comprar/carros/usados/veiculos-todos-estados/?tipoveiculo=carros&anunciante=concession%C3%A1ria%7Cloja%7Cmontadora%7Cpessoa%20f%C3%ADsica&tipoanuncio=usados&estado1=veiculos-todos-estados&qt=12&o=1&p=" + str(i))

    links = []
    count = 0
    for li in lista:
        #response = urllib2.urlopen(li)
        req = Request(li)
        try:
            response = urlopen(req)
        except URLError as e:
            time.sleep(5)  # delays for 5 seconds
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            # everything is fine
            htmlparser = etree.HTMLParser()
            tree = etree.parse(response, htmlparser)
            ll = tree.xpath('//div[@class="visao list c-after boxResultado"]/a/@href')
            links = links + ll

            count += 1
            if count % 100 == 0:
                print count
                linkser = pd.Series(links)

                with open(filename + '.csv', 'a') as f:
                    linkser.to_csv(f, header=False, index=False)
                links = []

    #linkser = pd.Series(links)
    #linkser.to_csv(filename + '.csv', index=False)

    return 'done'
