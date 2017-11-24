绘图
================================

时间序列图
-----------------
使用tplot(time series plot)系列对象绘制以时间为横轴的图。

使用方法
>>>>>>>>>>>>>>>>>
tplot系列对象并不是图像本身，它保存了画图所需的全部参数和原始数据。

tplot系列对象都可以调用 **tplot** 方法（假设我们得到了变量名为obj1的某个tplot对象）

.. code-block:: python

    fig = obj1.tplot()

这里变量fig是图片句柄，我们可以通过它来修改图片。

.. code-block:: python

    set_params(fig, {'ytitle':'B(nT)', 'xtitle':'time'})

使用show函数查看fig(推荐使用jupyter notebook环境)

.. code-block:: python

    show(fig)

fig默认以基于网页浏览器的 `可交互模式 <https://github.com/radar-bear/spacepku/blob/master/doc/source/figs/fig_stack.html>`_  展现。我们可以把fig保存为网页，也可以保存为png格式图片

.. code-block:: python

    save_png(fig, 'figure_name.png')
    save_html(fig, 'figure_name.html')

句柄中包含了画图所使用的参数和原始数据，可以使用以下函数保存和读取句柄

.. code-block:: python

    save_fig(fig, 'figure_name.source')
    fig_reload = load_fig('figure_name.source')



线图
>>>>>>>>>>>>>>>>>
绘制线图需要传入 **时间序列** 及 **一维数值序列** 。可以选择传入一组绘图参数。

.. code-block:: python

    time = np.array(range(50))
    value = np.random.random(50)
    line_obj = tplot_line_obj(time, value, {'title':'test_line'})
    fig = line_obj.tplot()

谱图
>>>>>>>>>>>>>>>>>
绘制谱图需要传入 **时间序列** ， **y轴序列** 及 **二维数值矩阵** 。可以选择传入一组绘图参数。

.. code-block:: python

    time = np.array(range(50))
    y = np.array(range(10))
    value = np.random.random([50,10])
    heatmap_obj = tplot_heatmap_obj(time, y, value, {'title':'test_heatmap', 'ytitle':'placeholder'})
    fig = heatmap_obj.tplot()

修改tplot对象
>>>>>>>>>>>>>>>>>



