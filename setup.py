import os
import sys
from subprocess import call

# platform = sys.platform

pip_package_list = ['numpy', 'pandas', 'h5py', 'spacepy', 'plotly']

package_dir = os.path.join(os.path.dirname(os.__file__),
                           'site-packages', 'spacepku')
print(package_dir)

call('pip install -r requirements.txt', shell=True)

if not os.path.exists(package_dir):
    os.mkdir(package_dir)

call(['cp', '-r', './src/*', package_dir])

call(['cd pysatCDF && python setup.py install'], shell=True)

call(['python', 'test.py'])
