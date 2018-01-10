import os
import sys
from subprocess import call

platform = sys.paltform

conda_package_list = ['plotly']
pip_package_list = ['spacepy'] # some packages missed in conda

package_dir = os.path.join(os.path.dirname(os.__file__),
                           'site-packages', 'spacepku')
print(package_dir)

call(['pip', 'install'] + pip_package_list)

call(['conda', 'install'] + conda_package_list)

if not os.path.exists(package_dir):
    os.mkdir(package_dir)

call(['cp', '-r', './src/*', package_dir])

call(['cd pysatCDF && python setup.py install'], shell=True)

call(['python', 'test.py'])
