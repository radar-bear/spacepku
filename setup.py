import os
import sys
from subprocess import call

# platform = sys.platform
call('pip install -r requirements.txt', shell=True)

import numpy
package_dir = (numpy.__file__).split('numpy')[0]+'spacepku'
print(package_dir)

if not os.path.exists(package_dir):
    os.mkdir(package_dir)

call(['cp', '-r', './src/*', package_dir])

call(['cd pysatCDF && python setup.py install'], shell=True)

call(['python', 'test.py'])
