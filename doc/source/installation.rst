安装
===============================

目前自动安装只支持Mac和Linux用户，Windows用户的安装说明还在路上。

请打开终端，进行以下操作

对于Mac用户，需要用brew安装gcc

.. code-block:: shell

    # 安装brew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    # 使用brew安装gcc
    brew install gcc

对于Linux用户，需要用apt-get安装一系列依赖

.. code-block:: shell

    sudo apt-get install gcc gfortran g++

对于Mac和Linux用户，完成上述准备工作后执行下面的命令。最后显示Enjoy!即安装成功，我们可以开始后面的教程了！

.. code-block:: shell

    git clone https://github.com/radar-bear/spacepku.git
    cd spacepku
    sudo python setup.py