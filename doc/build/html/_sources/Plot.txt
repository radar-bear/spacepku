绘图
================================

线图
>>>>>>>>>>>>>>>>>
绘制线图需要传入 **时间序列** 及 **二维数组** ，二维数组的第一个维度会被解释为不同的线。例如传入尺寸为(3, 50)的数组，将会得到3条由50个点组成的线。

.. code-block:: python

    import spacepku as sp
    x = np.array(range(50))
    value1 = np.random.random(50)
    value2 = np.random.random(50)
    fig_lines = sp.plot_lines(x, [value1, value2], {'title':'multi_lines'})
    # 如果只想画一条线，也要将数据包装成二维
    # 注意下面语句中的中括号
    fig_singleline = sp.plot_lines(time, [value1]) 

谱图
>>>>>>>>>>>>>>>>>
绘制谱图需要传入 **时间序列** ， **y轴序列** 及 **二维数组** 。可以选择传入一组绘图参数。

.. code-block:: python

    x = np.array(range(50))
    y = np.array(range(10))
    value = np.random.random([50,10])
    fig_heatmap = sp.plot_heatmap(x, y, value, {'title':'test_heatmap', 'ytitle':'placeholder'})

时间序列图
>>>>>>>>>>>>>>>>>
当横轴为时间时，传入参数**timeseries=True**。

.. code-block:: python

    import pandas as pd
    time = pd.date_range('2017-6-20','2017-8-20')
    value = np.random.random(len(time))
    fig_timeseries = sp.plot_lines(time, [value], timeseries=True)

修改图像
================================
前文中的plot返回的变量fig是图像句柄，我们可以通过它来修改图像。

.. code-block:: python

    set_params(fig, {'ytitle':'B(nT)', 'xtitle':'time'})

使用show函数查看fig(推荐使用jupyter notebook环境)

.. code-block:: python

    show(fig)

fig默认以基于网页浏览器的 `可交互模式 <mag.pku-space.cn/Data/library/spacepku/doc/source/figs/spacepku_demo.html>`_  展现。我们可以把fig保存为网页，也可以保存为png格式图片。

.. code-block:: python

    save_png(fig, 'figure_name.png')
    save_html(fig, 'figure_name.html')

句柄中包含了图像所使用的参数和原始数据，可以使用以下函数保存和读取完整的图像句柄。

.. code-block:: python

    save_fig(fig, 'figure_name.source')
    fig_reload = load_fig('figure_name.source')



