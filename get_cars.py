import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib
from urllib2 import Request, urlopen
from urllib2 import URLError
import time

from lxml import etree
import urllib2
from unidecode import unidecode
from time import gmtime, strftime

def requestator(url):
    print url
    #req = Request(url)
    try:
        req = Request(url)
        response = urlopen(req)
    except URLError as e:
        status = 'error'
        tree = 'error'
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        status = 'ok'
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)

    return status, tree


def get_cars(links, filename='./webm/results'):
    campos = dict(
        estado='//head/meta[@name="wm.dt_estado"]/@content',
        cidade='//head/meta[@name="wm.dt_cidade"]/@content',
        marca='//head/meta[@name="wm.dt_marca"]/@content',
        dt_mod='//head/meta[@name="wm.dt_mod"]/@content',
        combustivel='//head/meta[@name="wm.dt_combustivel"]/@content',
        cambio='//head/meta[@name="wm.dt_cambio"]/@content',
        codigo='//head/meta[@name="wm.dt_codanunc"]/@content',
        cor='//head/meta[@name="wm.dt_cor"]/@content',
        preco='//head/meta[@name="wm.dt_prc"]/@content',
        carroceria='//head/meta[@name="wm.dt_carroceria"]/@content',
        anomod='//head/meta[@name="wm.dt_anomod"]/@content',
        tipo='//head/meta[@name="wm.dt_tipoa"]/@content',
        tpag='//head/meta[@name="wm.tpag"]/@content',
        tipoc='//head/meta[@name="wm.dt_tipoc"]/@content',
        idk='//span[@class="dis-b pad-q_gutter-b"]/text()',
        ano='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[1]',
        km='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[2]',
        comb='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[3]',
        # cambio='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[4]',
        final_placa='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[5]',
        portas='(//div[@class="col-3 pad-h_gutter-tb"]//text())[12]',
    )

    # links = pd.read_csv(links_filename, header=None)
    results = []
    count = 0
    for li in links:
        status, tree = requestator(li)
        chaves = []
        vals = []
        chaves.append('link')
        vals.append(li)

        #time
        chaves.append('download_date')
        vals.append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

        if status == 'ok':
            #htmlparser = etree.HTMLParser()
            #tree = etree.parse(response, htmlparser)

            for key, value in campos.iteritems():
                parsed = None
                parsed = tree.xpath(value)
                if parsed:
                    chaves.append(key)
                    vals.append(unidecode(parsed[0]))

            ### FIPE
            l1 = tree.xpath('//div[@class="pad-oh_gutter-tb pad-l-1 pad-r-1 bg-gray-light2"]//@href')
            if l1:
                status, tree1 = requestator(l1[0])
                chaves.append('FIPE')
                arv = tree1.xpath('//p[@class="size-21 bold alinha-preco show"]/text()')
                if arv:
                    vals.append(arv[0])
                else:
                    vals.append('0')
            else:
                chaves.append('FIPE')
                vals.append('0')

            results.append(pd.DataFrame(vals, index=chaves).T)

        count += 1
        if count % 10 == 0 or li == links[-1]:
            print count
            final = pd.concat(results, axis=0).reset_index(drop=True)
            #final.to_csv(filename + '.csv', index=False)

            with open(filename + '.csv', 'a') as f:
                final.to_csv(f, header=False, index=False, sep=';')
                f.close()
            results = []

    return final
