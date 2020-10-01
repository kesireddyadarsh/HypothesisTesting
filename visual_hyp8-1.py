import plotly.figure_factory as ff
from data_acq import *

colorscale = [
    '#006600',
    '#CCFFCC',
]
r_list, u_list= get_rural_urban_counties()
county_list = get_population().keys()
fip_list = []
res_list = []
date_param = '06-04~07-15'

for county in u_list:
    res_list.append(82)
    fip = get_fips(county)
    fip_list.append(fip)

for county in r_list:
    res_list.append(172)
    fip = get_fips(county)
    fip_list.append(fip)

fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='', title='Texas Counties, Urban(82) Rural (172)',
    #binning_endpoints=[100, ],
    fips=fip_list, values=res_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.3},
)



fig.layout.template = None
fig.show()
