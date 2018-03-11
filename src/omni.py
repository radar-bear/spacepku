import pandas as pd
import numpy as np
import spacepy as sp
import os

OMNI_PATH = '/data/omni'


def parse_omni_dir(date, parrent_dir=OMNI_PATH):
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).year
    end = pd.to_datetime(date[-1]).year
    res = []
    for i in range(begin, end + 1):
        path = os.path.join(parrent_dir, str(i))
        filenameList = os.listdir(path)
        for f in filenameList:
            if f[-3:] == 'cdf':
                res.append(os.path.join(path, f))
    return res


def get_omni(date):
    return sp.data_obj(parse_omni_dir(date))
