读取数据
================================

读取cdf数据
--------------------
spacepku提供了一个类data_obj来处理各种格式的数据输入，包括[cdf, h5, csv, txt]。这一数据类型类似于字典，通过键值对的方式存储数据。

.. code-block:: python

    import spacepku as sp
    Data = sp.data_obj('your_file.cdf')
    print(Data)

也可以输入一系列文件名，这些文件不需要属于同种类型，data_obj会自动按键值进行数据拼合。

.. code-block:: python

    Data = sp.data_obj(['file1', 'file2', 'file3'])

打印变量Data，得到输出

：：
    0 Epoch (7825,)

    1 FEDU_Alpha (11,)

    2 FEDU_Energy (7825, 25)

    3 FEDU (7825, 11, 25)

    4 FESA (7825, 25)

    5 L (7825,)

    6 B_Calc (7825,)

    7 MLT (7825,)

    8 Position (7825, 3)

输出列出了data_obj中包含的各个键值和其对应数据的形状。

获取变量
>>>>>>>>>>>>
取出变量有两种索引方式，键值或序号。以取出时间变量为例，下面两种写法都能正确地获得数据：

.. code-block:: python

    Data['Epoch']
    Data[0]

返回值为np.array对象

获取变量的属性
>>>>>>>>>>>>>
取出变量的属性同样有两种索引方式，键值或序号。以取出时间变量的属性为例：

.. code-block:: python

    Data.attrs['Epoch']
    Data.attrs[0]

返回值为字典

便捷画图
>>>>>>>>>>>>>
cdf_obj的tplot方法可以绘制某变量的时间序列，同样有键值和序号两种索引方式。

对于一维变量绘制线图：

.. code-block:: python

    Data.tplot(5)
    Data.tplot('L')

对于二维变量可选线图或谱图：

.. code-block:: python

    # 指定画线图，第二个维度被视作不同线的索引
    Data.tplot('Position', type='line')
    # 指定画谱图，同时必须指定y轴数据
    Data.tplot('FESA', y=Data['FEDU_Energy'][0,:], type='heatmap')

三维及以上变量暂不支持便捷画图

其余参数：

 - params: 字典。设置画图参数。参数列表见参数设置。
 - log: 布尔值。画谱图时是否对变量取对数。
 - showfig: 布尔值。是否显示图片。

保留画图参数
>>>>>>>>>>>>>>>>>
cdf_obj内部保存着绘制每个变量所使用的画图参数字典，便捷画图会默认使用data_obj内部保存的画图参数字典。有两种方式可以修改这一字典：

.. code-block:: python

    Data.set_param(var_name, params)
    Data.tplot(var_name, params)

上面两种方法均可使用params更新var_name变量的画图参数字典。更新的意义是，原字典包含，但params中没有的键值对不会被更新。例如原字典为 {'title':'Bx', 'name':'temp'}，params为{'name':'Bx'}，更新后的字典{'title':'Bx', 'name':'Bx'}

画图参数也可以被存储和读取

.. code-block:: python

    Data1.save_config('default_plot_config1')
    Data2.load_config('default_plot_config1')

存储与读取
>>>>>>>>>>>>>>>>>

.. code-block:: python

    Data.save('file_name')
    Data_loaded = load_cdf_obj('file_name')









