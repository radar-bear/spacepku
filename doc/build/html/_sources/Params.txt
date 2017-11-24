绘图参数列表
================================

以字典的形式传入绘图参数，例如

.. code-block:: python

    plot_params = {'title':'First Figure',
                   'width':500,
                   'height':500,
                   'yrange':[0,10]}

现支持以下参数

**title**
:::::::::::::
标题，str

**showlegend**
:::::::::::::
是否显示图例，bool

**width**
:::::::::::::
宽度，int

**height**
:::::::::::::
高度，int

**ytitle**
:::::::::::::
纵轴标题，str

**yrange**
:::::::::::::
纵轴范围，list

**ytype**
:::::::::::::
纵轴类型，"linear"或"log"

**yticktext**
:::::::::::::
自定义y轴刻度文字，list

**ytickvals**
:::::::::::::
自定义y轴刻度的位置，list

**xtitle**
:::::::::::::
横轴标题，str

**xrange**
:::::::::::::
横轴范围，list

**xtype**
:::::::::::::
横轴类型，"linear"或"log"

**xticktext**
:::::::::::::
自定义x轴刻度文字，list

**xtickvals**
:::::::::::::
自定义x轴刻度的位置，list

**name**
:::::::::::::
图例名称，str

**text**
:::::::::::::
鼠标悬停显示文字，list

**line_color**
:::::::::::::
线颜色，str
格式为 'rgba(34, 67, 89, 1)'

**line_width**
:::::::::::::
线宽度，float

**line_dash**
:::::::::::::
实线或虚线，"solid"或"dot"或"dash"

**ctitle**
:::::::::::::
colorbar名称，str

**cticktext**
:::::::::::::
自定义colorbar刻度，list

**ctickvals**
:::::::::::::
自定义colorbar刻度的位置，list

**crange**
:::::::::::::
colorbar范围，list
