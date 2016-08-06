import glob
import pandas as pd
import numpy as np

links = glob.glob('./webm/links/*raw*')

### Count total of links available
urls = []
for l in links:
    urls += list(pd.read_csv(l, header=None)[0])

### Count total of links downloaded
datalinks = glob.glob('./webm/data/*results*')

urls2 = []
for d in datalinks:
    urls2 += list(pd.read_csv(d, header=None, sep=';')[14])


delta = pd.DataFrame(list(set(urls) - set(urls2)))
delta.to_csv('./webm/links/delta_links.csv', index=False, sep=';', header=None)