##################NOTES###########################
'''
plot.tplot_line & plot.tplot_particle 是最基础的画图函数
tplot_line_obj & tplot_particle_obj 提供了参数包装，参数更新，输入检查和数据保护
cdf_data 提供了数据读入，数据预处理，数据提取
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
# plot obj

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
        return tplot_particle(self._time,
                              self._y,
                              self._value.T, # 转置value
                              trace_params=plotly_params['trace_params'],
                              layout_params=plotly_params['layout_params'],
                              colorbar_params=plotly_params['colorbar_params'],
                              log=log,
                              dist_normalize=dist_normalize,
                              showfig=showfig)

###########################
# basic data obj

def #TODO load其他cdfdata的画图配置文件，cdfdata的保存功能可能要修改

class cdf_data(basic_obj):
    # TODO parrent class raw_data
    # inherit tplot from patte
    def __init__(self, file_path):
        if file_path.split('.')[-1] != 'cdf':
            raise ValueError('{} is not a cdf file'.format(cdf_file_path))
        self._origin_file_name = file_path
        self._cdf = load_cdf(file_path)
        self._keys = list(self._cdf.keys())
        self._shapes = [self._cdf[key].shape for key in self._keys]
        self._attrs = {key:dict(self._cdf[key].attrs) for key in self._keys}
        self._plot_params = {}
        for key in self._keys:
            self._plot_params[key] = {}
        if 'Epoch' in self._cdf.keys():
            self._default_time = self.convert_raw_cdf_data(self._cdf['Epoch'])
        else:
            self._default_time = []
        
    def __str__(self):
        base_info = "tplot object generated from: \n {}\n".format(self._origin_file_name)
        for i in range(len(self._keys)):
            base_info += "{} {} {}\n".format(i, self._keys[i], self._shapes[i])
        return base_info
    __repr__ = __str__
        
    def __getitem__(self, key):
        key = self.parse_key(key)
        return self.convert_raw_cdf_data(self._cdf[key])
    
    def save(self, file_name):
        save_info = {}
        save_info['origin_file_name'] = self._origin_file_name
        save_info['plot_params'] = self._plot_params
        save_dict(save_info, file_name)
    
    @property
    def attrs(self):
        from copy import deepcopy
        return deepcopy(self._attrs)
    
    def parse_key(self, key):
        if isinstance(key, int):
            key = self._keys[key]
        return key
    
    def set_param(self, key, params):
        key = self.parse_key(key)
        self._plot_params[key].update(params)
        
    def convert_raw_cdf_data(self, raw_cdf_data, fillval_key='FILLVAL'):
        data = raw_cdf_data[:]
        if fillval_key in raw_cdf_data.attrs:
            fillval = raw_cdf_data.attrs[fillval_key]
            data[data==fillval] = np.nan
        return data
    
    def tplot(self, key, y=[], time=[], params={}, type='Default', clog=False, showfig=True):

        key = self.parse_key(key)
        if len(time)==0:
            time = self._default_time
        if len(time)==0:
            raise ValueError('time data missed when plot {}'.format(key))
        value = self.convert_raw_cdf_data(self._cdf[key])
        value_dim = len(value.shape)
        
        # 如果画图类型是Default则自动判断类型
        if type == 'Default':
            type = tplot_default_type_parse(value_dim)
                
        if params:
            self._plot_params[key].update(params)
            
        if type == 'line':
            # 指定类型为line后如果是1维数据画普通线图
            # 如果是2为数据画多线图
            if value_dim == 1:
                obj = tplot_line_obj(time, value, params=self._plot_params[key])
                return obj.tplot(showfig=showfig)
            if value_dim == 2:
                line_num = value.shape[1]
                obj_list = [tplot_line_obj(time, value[:,i], params=self._plot_params[key]) 
                            for i in range(line_num)]
                fig_list = [obj.tplot(showfig=False) for obj in obj_list]
                return stack_traces(fig_list, showfig=showfig)
        
        if type == 'heatmap':
            if len(y) == 0:
                raise ValueError('y data missed when plot {}'.format(key))
            obj = tplot_heatmap_obj(time, y, value, params=self._plot_params[key])
            return obj.tplot(log=clog, showfig=showfig)