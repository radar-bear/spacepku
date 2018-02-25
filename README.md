# spacepku
spacepku致力于使空间物理研究中的数据可视化变得简单有趣。
当前版本为V0.0.1

## 安装

### 准备工作

如果你的电脑已经装有gcc编译器可以跳过此节。

对于Mac用户，使用brew安装gcc。打开终端，执行下面的命令：

    # 安装brew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
    # 使用brew安装gcc
    brew install gcc

对于Linux用户，使用apt-get安装一系列依赖

    sudo apt-get install gcc gfortran g++

### 安装spacepku

我们推荐大家安装[Anaconda3](https://www.anaconda.com/download/)，这样会省去很多麻烦。

打开终端，执行下面的命令（这可能会花费几分钟）：

    git clone https://github.com/radar-bear/spacepku.git
    cd spacepku
    sudo python setup.py

最后显示“Successfully installed spacepku! Enjoy!”即安装成功！

### 升级spacepku

spacepku当前版本为 **0.0.1**

如果之前已经安装过较低版本的spacepku，执行下面的命令可升级至最高版本

    git clone https://github.com/radar-bear/spacepku.git
    cd spacepku
    sudo python upgrade.py

## 开发与维护
北京大学空间科学与技术中心
leimingda@pku.edu.cn
