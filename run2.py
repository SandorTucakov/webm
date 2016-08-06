import sys
sys.path.append('./webm')
import time
import pandas as pd
from get_cars import *
from multiprocessing import Pool
from time import sleep

def pega(arg1, arg2):
    links = pd.read_csv(arg1, sep=';', header=None)
    urls = list(links[0])
    get_cars2(urls, arg2)
    print links[0]

    return links

pool = Pool(processes=20)
result_squares = pool.map_async(pega, './webm/links/delta_links.csv')
