import sys
import time
import pandas as pd
from get_cars import *
def main(arg1, arg2):
    links = pd.read_csv(arg1, sep=';', header=None)
    urls = list(links[0])
    get_cars2(urls, arg2)
    print links[0]

    return links

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

# ipython
import os
os.system("python run.py ./links/links_4.csv results_4")