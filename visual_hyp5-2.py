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
fip_list = []
res_list = []
date_param = '05-21~07-25'

for county in county_list:
    trans_data = get_cases(county, date_range=date_param, number_form='transmission', mv_avg_days=42)
    trans_rate = trans_data[0]
    res_list.append(trans_rate)
    fip = get_fips(county)
    fip_list.append(fip)


fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title= '({})'.format(date_param), title='Transimission Rate',
    binning_endpoints=[10, 150, 300, 450, 600],
    fips=fip_list, values=res_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.3},
)



fig.layout.template = None
fig.show()
