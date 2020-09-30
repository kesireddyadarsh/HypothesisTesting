import plotly.figure_factory as ff
from data_acq import *

colorscale = [
    'rgb(193, 193, 193)',
    'rgb(239,239,239)',
    'rgb(195, 196, 222)',
    'rgb(144,148,194)',
    'rgb(101,104,168)',
    'rgb(65, 53, 132)'
]

county_list = get_population().keys()
date_param = '04-21~09-11'
fip_list = []
lv_list = []

for county in county_list:
    x = get_testings(county, date_range=date_param)
    y = get_cases(county, date_range=date_param, number_form='transmission', mv_avg_days=7)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    lv = round((1 - abs(p_value)) * 100, 1) 
    lv_list.append(lv)
    fip = get_fips(county)
    fip_list.append(fip)


fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='Confidence Level (%)', title='Testing vs Transmission Rate',
    binning_endpoints=[20, 40, 68, 95, 99.7],
    fips=fip_list, values=lv_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.3},
)



fig.layout.template = None
fig.show()
