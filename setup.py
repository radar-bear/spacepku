import os
import sys
from subprocess import call

platform = sys.platform

call('pip install -r requirements.txt', shell=True)

import numpy
package_dir = (numpy.__file__).split('numpy')[0]+'spacepku'
print(package_dir)

if not os.path.exists(package_dir):
    os.mkdir(package_dir)
else:
    call(['rm -r ' + package_dir], shell=True)
    os.mkdir(package_dir)

call(['cp -r ./src/* ' + package_dir], shell=True)

call(['git clone https://github.com/rstoneback/pysatCDF.git && cd pysatCDF && python setup.py install'], shell=True)

# dir_list = os.listdir('./pysatCDF/build')
# for dir in dir_list:
#     if dir[:3] == 'src':
#         break

call(['cp ./pysatCDF/build/src*/lib/libcdf* /usr/local/lib'], shell=True)

if platform=='linux':
    call(['echo "CDF_LIB = \\\"/usr/local/lib\\\"" >> /etc/environment'], shell=True)
elif platform=='darwin':
    call(['echo "export CDF_LIB=/usr/local/lib" >> /etc/bashrc'], shell=True)
    # call(['echo "export CDF_LIB=/usr/local/lib" >> ~/.bashrc'], shell=True)
    # call(['echo "export CDF_LIB=/usr/local/lib" >> ~/.profile'], shell=True)

else:
    raise ValueError('operation system not supported')

call(['python', 'test.py'])
