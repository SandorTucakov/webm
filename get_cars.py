import pandas as pd
import numpy as np
from bs4 import BeautifulSoup, SoupStrainer
import urllib
from urllib2 import Request, urlopen
from urllib2 import URLError
import time
import requests
import re
from lxml import etree
import urllib2
from unidecode import unidecode
from time import gmtime, strftime
import copy
# import sys
# sys.path.append('./webm/')
# import get_cars



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


def fipeitor(url):
    status, arvore = requestator(url)
    arv = arvore.xpath('//p[@class="size-21 bold alinha-preco show"]/text()')
    if arv:
        val = arv[0]
    else:
        val = 0

    return val


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
        final_placa='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[5]',
        portas='(//div[@class="col-3 pad-h_gutter-tb"]//text())[12]',
    )

    output_ini = dict(
        link='',
        download_date='',
        ativo='',
        estado='',
        cidade='',
        marca='',
        dt_mod='',
        combustivel='',
        cambio='',
        codigo='',
        cor='',
        preco='',
        carroceria='',
        anomod='',
        tipo='',
        tpag='',
        tipoc='',
        idk='',
        ano='',
        km='',
        comb='',
        final_placa='',
        portas='',
        FIPE='',
        FIPE_data='',
        FIPE_link='',

    )

    ### Get FIPE
    previous = pd.read_csv(filename+'.csv', sep=';')
    previous['FIPE_INDEX'] = previous.ix[:, 0].apply(str) + ' - ' + previous.ix[:, 10].apply(str)

    results = []
    count = 0
    for li in links:
        output = copy.deepcopy(output_ini)
        status, tree = requestator(li)
        output['link'] = li

        ano = gmtime().tm_year
        mes = gmtime().tm_mon
        #dia = gmtime().tm_year
        output['download_date'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        output['FIPE_data'] = ano*100 + mes

        ativo = True
        desativado = tree.xpath("(//div[@class='size-xbigger bold mrg-gutter-b']//text())")
        if desativado:
            ativo = unidecode(desativado[0]) != 'Anuncio Desativado.'

        if status == 'ok' and ativo:
            for key, value in campos.iteritems():
                parsed = None
                parsed = tree.xpath(value)
                if parsed:
                    #chaves.append(key)
                    output[key] = unidecode(parsed[0])
                    #vals.append(unidecode(parsed[0]))

            ### FIPE
            l1 = tree.xpath('//div[@class="pad-oh_gutter-tb pad-l-1 pad-r-1 bg-gray-light2"]//@href')

            if l1:
                output['FIPE_link'] = l1[0]
                output['FIPE'] = fipeitor(l1[0])

            else:
                output['FIPE'] = '0'
                output['FIPE_link'] = '-'

        results.append(pd.DataFrame.from_dict(output, orient='index').T)

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


# campos = dict(
#     estado='//head/meta[@name="wm.dt_estado"]/@content',
#     cidade='//head/meta[@name="wm.dt_cidade"]/@content',
#     marca='//head/meta[@name="wm.dt_marca"]/@content',
#     dt_mod='//head/meta[@name="wm.dt_mod"]/@content',
#     combustivel='//head/meta[@name="wm.dt_combustivel"]/@content',
#     cambio='//head/meta[@name="wm.dt_cambio"]/@content',
#     codigo='//head/meta[@name="wm.dt_codanunc"]/@content',
#     cor='//head/meta[@name="wm.dt_cor"]/@content',
#     preco='//head/meta[@name="wm.dt_prc"]/@content',
#     carroceria='//head/meta[@name="wm.dt_carroceria"]/@content',
#     anomod='//head/meta[@name="wm.dt_anomod"]/@content',
#     tipo='//head/meta[@name="wm.dt_tipoa"]/@content',
#     tpag='//head/meta[@name="wm.tpag"]/@content',
#     tipoc='//head/meta[@name="wm.dt_tipoc"]/@content',
#     idk='//span[@class="dis-b pad-q_gutter-b"]/text()',
#     ano='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[1]',
#     km='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[2]',
#     comb='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[3]',
#     final_placa='(//div[@class="dis-tc col-4 last valign-m"]//strong/text())[5]',
#     portas='(//div[@class="col-3 pad-h_gutter-tb"]//text())[12]',
# )


def requestator_2(url):
#if True:
    output_ini = dict(
        link='',
        download_date='',
        ativo='',
        estado='',
        cidade='',
        marca='',
        modelo='',
        combustivel='',
        cambio='',
        codigo='',
        cor='',
        preco='',
        carroceria='',
        anomod='',
        tipo='',
        tpag='',
        tipoc='',
        idk='',
        ano='',
        km='',
        comb='',
        final_placa='',
        portas='',
        FIPE='',
        FIPE_data='',
        FIPE_link='',
    )

    output = copy.deepcopy(output_ini)

    output['link'] = url
    ano = gmtime().tm_year
    mes = gmtime().tm_mon
    # dia = gmtime().tm_year
    output['download_date'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    output['FIPE_data'] = ano * 100 + mes

    try:
        session = requests.Session()
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)

        print 'fail'
        return output

    response = session.get(url)

    strainer = SoupStrainer('div')
    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

    try:
        output['ativo'] = unidecode(soup.find('div', {'class': 'size-xbigger bold mrg-gutter-b'}).text)
    except:
        output['ativo'] = '1'
        divTag = soup.find_all('div', {'class': 'dis-tc col-4 last valign-m'})
        output['ano'] = divTag[0].find_all('strong')[0].text
        output['km'] = divTag[1].find_all('strong')[0].text
        output['comb'] = divTag[2].find_all('strong')[0].text
        output['final_placa'] = divTag[4].find_all('strong')[0].text
        output['portas'] = int(soup.find_all('div', {'class': 'col-3 pad-h_gutter-tb'})[-1].contents[-1])

        for link in soup.find_all('a', href=re.compile('http://www.webmotors.com.br/tabela-fipe/')):
            output['FIPE_link'] = link['href']

        if output['FIPE_link']:
            output['FIPE'] = fipeitor(output['FIPE_link'])

        # parse the search page using SoupStrainer and lxml
        strainer = SoupStrainer('head')
        soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

        output['estado'] = soup.find('meta', {'name': 'wm.dt_estado'})['content']
        output['cidade'] = soup.find('meta', {'name': 'wm.dt_cidade'})['content']
        output['marca'] = soup.find('meta', {'name': 'wm.dt_marca'})['content']
        output['modelo'] = soup.find('meta', {'name': 'wm.dt_mod'})['content']
        output['combustivel'] = soup.find('meta', {'name': 'wm.dt_combustivel'})['content']
        output['cambio'] = soup.find('meta', {'name': 'wm.dt_cambio'})['content']
        output['codigo'] = soup.find('meta', {'name': 'wm.dt_codanunc'})['content']
        output['cor'] = soup.find('meta', {'name': 'wm.dt_cor'})['content']
        output['preco'] = soup.find('meta', {'name': 'wm.dt_prc'})['content']
        output['carroceria'] = soup.find('meta', {'name': 'wm.dt_carroceria'})['content']
        output['anomod'] = soup.find('meta', {'name': 'wm.dt_anomod'})['content']
        output['tipo'] = soup.find('meta', {'name': 'wm.dt_tipoa'})['content']
        output['tpag'] = soup.find('meta', {'name': 'wm.tpag'})['content']
        output['tipoc'] = soup.find('meta', {'name': 'wm.dt_tipoc'})['content']

        unidecodables = ['estado', 'cidade', 'cor', 'modelo', 'carroceria', 'combustivel']
        for u in unidecodables:
            output[u] = unidecode(output[u].strip())



    return output



def get_cars2(urls, filename='./webm/results'):
    assert isinstance(urls, list)
    cars = []
    count = 0
    for u in urls:

        try:
            carro = requestator_2(u)
        except:
            pass
        else:
            carro = pd.DataFrame.from_dict(carro, orient='index').T
            cars.append(carro)

            count += 1
            if count % 1000 == 0:
                print count
                final = pd.concat(cars, axis=0).reset_index(drop=True)
                # final.to_csv(filename + '.csv', index=False)

                with open(filename + '.csv', 'a') as f:
                    final.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
                    f.close()
                cars = []


    final = pd.concat(cars, axis=0).reset_index(drop=True)
    with open(filename + '.csv', 'a') as f:
        final.to_csv(f, header=False, index=False, sep=';', encoding='utf-8')
        f.close()


    return final

# req = soup.find('meta', {'name':'wm.dt_cor'})['content']
# ss.find('div', {'class': 'pad-oh_gutter-tb pad-l-1 pad-r-1 bg-gray-light2'})
# for link in ss.find_all('a', href=re.compile('http://www.webmotors.com.br/tabela-fipe/')):
#     print link['href']
#
# import re




# divTag = ss.find_all('div', {'class': 'col-3 pad-h_gutter-tb'})
# for tag in divTag:
#     tdTags = tag.find_all("strong")
#     for tag in tdTags:
#         print tag.text

# for s in soup.find_all('div', {'class': 'col-3 pad-h_gutter-tb'})[-1]:
#     s.next_sibiling

######################################
# import pandas as pd
# links = pd.read_csv('./webm/links_3.csv', header=None)
# url = list(links[0])[4]
#
# import sys
# sys.path.append('./webm')
# import get_cars

links_csv = './webm/links/links_full.csv'
import numpy as np
def links_splitator(links_csv, chunks=8):
    links = pd.read_csv(links_csv, sep=';', header=None)
    chunk = np.array_split(np.array(links[0]),chunks)

    count = 1
    for c in chunk:
        print pd.DataFrame(c).to_csv('./webm/links/links_' + str(count) + '.csv', sep=';', header=None, index=False)
        count += 1

    return count