
layout_keys = ['title', 'showlegend', 'width', 'height']
yaxis_keys = ['ytitle', 'yrange', 'ytype', 'yticktext', 'ytickvals']
xaxis_keys = ['xtitle', 'xrange', 'xtype', 'xticktext', 'xtickvals']
trace_keys = ['name', 'text']
line_keys = ['line_color', 'line_width', 'line_dash']
colorbar_keys = ['ctitle', 'cticktext', 'ctickvals']
colorbar_range = 'crange'

def parse_params_to_plotly(params):

    layout_params = {'yaxis':{}, 'xaxis':{}}
    for key in layout_keys:
        if key in params:
            layout_params[key] = params[key]
    for key in yaxis_keys:
        if key in params:
            layout_params['yaxis'][key[1:]] = params[key]
    for key in xaxis_keys:
        if key in params:
            layout_params['xaxis'][key[1:]] = params[key]
    if 'range' in layout_params['yaxis']:
        layout_params['yaxis']['autorange'] = False
    if 'range' in layout_params['xaxis']:
        layout_params['xaxis']['autorange'] = False

    trace_params = {}
    for key in trace_keys:
        if key in params:
            trace_params[key] = params[key]
    if colorbar_range in params:
        trace_params['zmin'] = params[colorbar_range][0]
        trace_params['zmax'] = params[colorbar_range][1]

    line_params = {}
    for key in line_keys:
        if key in params:
            line_params[key[5:]] = params[key]
    if line_params:
        trace_params['line'] = line_params

    colorbar_params = {}
    for key in colorbar_keys:
        if key in params:
            colorbar_params[key[1:]] = params[key]

    return {'layout_params':layout_params, 'trace_params':trace_params, 'colorbar_params':colorbar_params}