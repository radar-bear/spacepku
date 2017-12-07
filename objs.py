##################NOTES###########################
'''
plot.plot_line & plot.plot_heatmap 是最基础的画图函数
plot.tplot_line & plot.tplot_heatmap 提供了时间轴检查，tplot_heatmap额外提供了对数化&归一化参数
tplot_line_obj & tplot_heatmap_obj 提供了参数包装，参数更新，输入检查和数据保护
basic_data_obj 提供了两种索引方式和tplot
cdf_obj 提供了cdf数据读入，cdf数据预处理(to np.array)，cdf数据属性查询
data_obj 提供了数据整合功能(以所有文件key交集为准，在axis0上拼接)，可以输入数个文件名，文件可以使用不同格式，但必须以字典的形式读出。
理想中暴露给用户的应该是data_obj
'''
##################################################

import numpy as np
import pandas as pd
from .plot import *
from .utils import *
from .tools import *

###########################
# basic obj

class basic_obj():

    def __init__(self):
        pass

    def save(self, file_name):
        save(self, file_name)

###########################
# time series plot obj

class tplot_obj(basic_obj):

    def __init__(self, time, y, value, params={}):
        from copy import deepcopy, copy
        assert isinstance(params, dict)
        self._time = copy(time)
        self._value = deepcopy(value)
        self._y = copy(y)
        self._params = deepcopy(params)

    def __len__(self):
        return len(self._time)

    def set_time(self, time):
        from copy import copy
        self._time = copy(time)

    def set_y(self, y):
        from copy import copy
        self._y = copy(y)

    def set_value(self, value):
        from copy import deepcopy
        self._value = deepcopy(value)

    def set_param(self, params):
        from copy import deepcopy
        self._params.update(params)

    @property
    def time(self):
        from copy import copy
        return copy(self._time)

    @property
    def y(self):
        from copy import copy
        return copy(self._y)

    @property
    def value(self):
        from copy import deepcopy
        return deepcopy(self._value)

    @property
    def params(self):
        from copy import deepcopy
        return deepcopy(self._params)

class tplot_line_obj(tplot_obj):

    def __init__(self, time, value, params={}):
        time_shape = np.shape(time)
        value_shape = np.shape(value)
        assert time_shape == value_shape
        assert len(time_shape) == 1
        super(tplot_line_obj, self).__init__(time=time, y=None, value=value, params=params)

    def tplot(self, showfig=True):
        plotly_params = parse_params_to_plotly(self._params)
        return tplot_line(self._time,
                          [self._value],
                          trace_params=plotly_params['trace_params'],
                          layout_params=plotly_params['layout_params'],
                          showfig=showfig)

class tplot_heatmap_obj(tplot_obj):

    def __init__(self, time, y, value, params={}):
        # 这里我们假设value的形状是[time, y]，这种假设更符合cdf文件的原始形式
        # 在画图的时候要记得转置
        time_shape = np.shape(time)
        value_shape = np.shape(value)
        y_shape = np.shape(y)
        assert len(time_shape) == 1
        assert len(value_shape) == 2
        assert len(y_shape) == 1
        assert value_shape[0] == time_shape[0]
        assert value_shape[1] == y_shape[0]
        super(tplot_heatmap_obj, self).__init__(time=time, y=y, value=value, params=params)

    def tplot(self, log=False, dist_normalize=False, showfig=True):
        plotly_params = parse_params_to_plotly(self._params)
        return tplot_heatmap(self._time,
                             self._y,
                             self._value.T, # 转置value
                             trace_params=plotly_params['trace_params'],
                             layout_params=plotly_params['layout_params'],
                             colorbar_params=plotly_params['colorbar_params'],
                             log=log,
                             dist_normalize=dist_normalize,
                             showfig=showfig)

###########################
# raw data obj

class basic_data_obj(basic_obj):
    '''
    data 必须是类dict格式
    由于要支持key和序号两种索引方式，所以要对self._keys排序使key序列化
    TODO: basic存取功能，初步考虑继承自basic obj中的pickle save方式。但由于cdf文件以指针形式传递，不能序列化，所以cdf obj需要一套自己的接口。要实现两种存取，一种是保存全部数据，另一种是只保存画图参数等。只保存参数可以写一个方法，也可以提供一个访问画图参数的接口，让用户自己去存取。这一部分需要确定用户需求。
    '''
    def __init__(self, data):
        self._data = data
        self._keys = sorted(list(data.keys())) # 统一按照字母顺序排列键值
        self._shapes = [np.shape(self._data[key]) for key in self._keys]
        self._plot_params = {}
        for key in self._keys:
            self._plot_params[key] = {}

    def __getitem__(self, key):
        key = self.parse_key(key)
        return self.convert_raw_data(key)
    
    def __repr__(self, extra_info=None):
        if extra_info:
            print(extra_info)
        base_info = ''
        for i in range(len(self._keys)):
            base_info += "{} {} {}\n".format(i, self._keys[i], self._shapes[i])
        return base_info
    __str__ = __repr__
    
    def keys(self):
        from copy import deepcopy
        return deepcopy(self._keys)
    
    def parse_key(self, key):
        '''
        enable the ability to locate date by both key and index
        '''
        if isinstance(key, int):
            key = self._keys[key]
        return key
    
    def convert_raw_data(self, key):
        '''
        convert self._data[key] to np.array
        '''
        return self._data[key]
    
    def set_param(self, key, params):
        '''
        设置画图参数
        '''
        key = self.parse_key(key)
        self._plot_params[key].update(params)
    
    def tplot(self, key, y=[], time=[], params={}, type='Default', clog=False, showfig=True):
        key = self.parse_key(key)
        # check time data
        if len(time)==0:
            for time_key in DEFAULT_TIME_KEY:
                if time_key in self._data.keys():
                    time = self[time_key]
                    break
            # 如果不含有任何default time key则需要用户指定time数据
            if len(time)==0:
                raise ValueError('please specify time data when plot {}'.format(key))
        # prepare data
        value = self[key]
        value_dim = len(value.shape)
        # 如果用户提供了画图参数则更新这些参数
        if params:
            self._plot_params[key].update(params)
        # 自动适应数据维度画图
        # 如果画图类型是Default则自动判断类型
        if type == 'Default':
            type = tplot_default_type_parse(value_dim)   
        # 指定类型为line后如果是1维数据画单线图
        # 如果是2维数据画多线图
        if type == 'line':
            if value_dim == 1:
                obj = tplot_line_obj(time, value, params=self._plot_params[key])
                return obj.tplot(showfig=showfig)
            if value_dim == 2:
                line_num = value.shape[1]
                obj_list = [tplot_line_obj(time, value[:,i], params=self._plot_params[key])
                            for i in range(line_num)]
                fig_list = [obj.tplot(showfig=False) for obj in obj_list]
                return stack_traces(fig_list, showfig=showfig)
        # 指定类型为heatmap画谱图
        if type == 'heatmap':
            if len(y) == 0:
                raise ValueError('y data missed when plot {}'.format(key))
            obj = tplot_heatmap_obj(time, y, value, params=self._plot_params[key])
            return obj.tplot(log=clog, showfig=showfig)
        
        
class cdf_obj(basic_data_obj):
    
    def __init__(self, file_path):
        # load basic data and info
        if file_path.split('.')[-1] != 'cdf':
            raise ValueError('{} is not a cdf file'.format(cdf_file_path))
        super(cdf_obj, self).__init__(load_cdf(file_path))
        # set attrs and plot params
        self._origin_file_name = file_path
        self._attrs = {key:dict(self._data[key].attrs) for key in self._keys}
        self._attrs.update({i:self._attrs[self._keys[i]] for i in range(len(self._keys))})

    def __repr__(self):
        extra_info = "cdf data object generated from: \n {}\n".format(self._origin_file_name)
        return super(cdf_obj, self).__repr__(extra_info)
    __str__ = __repr__
    
    def convert_raw_data(self, key, fillval_key_list=DEFAULT_FILLVAL_KEY):
        raw_cdf_data = self._data[key]
        data = raw_cdf_data[:]
        if 'int' in data.dtype.name:
            data = data.astype(np.float)
        for fillval_key in fillval_key_list:
            if fillval_key in raw_cdf_data.attrs:
                fillval = raw_cdf_data.attrs[fillval_key]
                data[data==fillval] = np.nan
                break
        return data

    def save_config(self, file_name):
        config_info = {}
        config_info['origin_file_name'] = self._origin_file_name
        config_info['plot_params'] = self._plot_params
        save_dict(config_info, file_name)

    def save(self, file_name):
        self.save_config(file_name)

    def load_config(self, file_name):
        config_info = load_dict(file_name)
        self._plot_params = config_info['plot_params']

    @property
    def attrs(self):
        from copy import deepcopy
        return deepcopy(self._attrs)

        
class data_obj(basic_data_obj):

    def __init__(self, data_source, select_keys=[]):
        '''
        data_source: 
        1. file name
        2. list of file name
        3. dict-like origin data
        (dict-like means method keys() and __getitem__())
        '''
        # case1 string
        if isinstance(data_source, str):
            self.__init__([data_source])
        # case2 list
        elif isinstance(data_source, list):
            # data_source is a list of file
            file_type_map = {
                'cdf':cdf_obj,
            }
            self._data_obj_list = []
            for file_name in data_source:
                file_type = file_name.split('.')[-1]
                self._data_obj_list.append(file_type_map[file_type](file_name))
            # keys是全部data obj keys的交集
            keys = set(self._data_obj_list[0].keys())
            for obj in self._data_obj_list:
                keys = keys & set(obj.keys())
            if len(select_keys)>0:
                keys = keys & set(select_keys)
            # 拼接数据
            data = {}
            for key in keys:
                data[key] = np.concatenate([i[key] for i in self._data_obj_list], axis=0)
            # 初始化
            super(data_obj, self).__init__(data)
        # case3 dict-like
        elif ('__getitem__' in dir(data_source)) & ('keys' in dir(data_source)):
            # data_source is dict-like
            super(data_obj, self).__init__(data_source)
        # other case invalid
        else:
            raise ValueError('Data source invalid')
        
        
        
        
        