from .objs import *
def load_cdf_obj(file_name):
    config_info = load_dict(file_name)
    obj = cdf_obj(config_info['origin_file_name'])
    obj.load_config(file_name)
    return obj