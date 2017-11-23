读取数据
================================

读取cdf数据
--------------------
spacepku提供了一个类cdf_obj来处理cdf数据输入

.. code-block:: python

    from spacepku import *
    Data = cdf_obj('your_file.cdf')
    print(Data)

得到输出
：：

    cdf data object generated from:
    /data/mentor_data.cdf

    0 Epoch (7825,)

    1 FEDU_Alpha (11,)

    2 FEDU_Energy (7825, 25)

    3 FEDU (7825, 11, 25)

    4 L (7825,)

    5 B_Calc (7825,)

    6 MLT (7825,)

    7 Position (7825, 3)

输出中包括两部分内容，第一行显示了这个cdf_obj对象读取自哪个文件。接下来的若干行显示了这个cdf_obj对象包含的变量。

取出变量
>>>>>>>>>>>>
取出变量有两种索引方式，键值或序号。以取出时间变量为例：

.. code-block:: python

    Data['Epoch']
    Data[0]





