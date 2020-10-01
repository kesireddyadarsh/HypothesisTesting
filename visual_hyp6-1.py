import plotly.figure_factory as ff
from data_acq import *

colorscale = [
    '#004400',
    '#AABBCC',
]
r_list, u_list= get_rural_urban_counties()
county_list = get_population().keys()

fip_list = []
res_list = []
date_param = '06-04~07-15'


no_urban_adj = []
with_urban_adj = []

count = 0
for county in county_list:
    adj_counties = get_adj_counties(county)
    is_dirty = False
    for i, adj in enumerate(adj_counties):
        if adj in u_list:
            is_dirty = True
        else:
            pass
    # self is urban
    if county in u_list:
        is_dirty = True

    if is_dirty == True:
        res_list.append(199)
    else:
        res_list.append(55)
        count += 1
    fip = get_fips(county)
    fip_list.append(fip)

# 55 rural counties qualified
print(count)
fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='', title='Rural Counties without Urban Counties Adjacent',
    #binning_endpoints=[100, ],
    fips=fip_list, values=res_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.3},
)



fig.layout.template = None
fig.show()
