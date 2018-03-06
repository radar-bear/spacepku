import os
os.environ['CDF_LIB'] = '/usr/local/lib'

import spacepku as sp
from spacepku import data_obj
from spacepku import plot_lines
from spacepku.config import VERSION

print('Successfully installed spacepku@{}! Enjoy!'.format(VERSION))
