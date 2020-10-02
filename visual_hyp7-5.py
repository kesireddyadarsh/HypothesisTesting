import plotly.figure_factory as ff
from data_acq import *

colorscale = [
    '#f2f2f2',
    '#ccfff5',
    '#99ff99',
    '#ffff99',
    '#ff9966',
    '#ff6666',
]

date_param = '05-01~05-30'
fip_list = []
lv_list = []

county_list = get_population().keys()
for county in county_list:
    y = get_cases(county, date_range=date_param, number_form='infection')
    try:
        g1 = get_travel(county, attr='recreation', date_range=date_param)
    except:
        # no data in some counties from Mobility data
        continue
    g2 = get_travel(county, attr='grocery', date_range=date_param)
    g3 = get_travel(county, attr='park', date_range=date_param)
    g4 = get_travel(county, attr='transit', date_range=date_param)
    g5 = get_travel(county, attr='work', date_range=date_param)
    g6 = get_travel(county, attr='resident', date_range=date_param)
    g_mean = get_travel(county, attr='mean', date_range=date_param)
    #f_value, p_value = stats.f_oneway(y, g1, g2, g3, g4, g5, g6)
    f_value, p_value = stats.f_oneway(y, g6, g2, g4, g1, g5, g3)

    lv = round(1 - abs(p_value), 4) * 100 
    lv_list.append(lv)
    fip = get_fips(county)
    fip_list.append(fip)

fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='Confidence Level (%)', title='Spread vs (Residential + Grocery&Pharmary + Transit + Rereation + Work + Park)',
    binning_endpoints=[20, 40, 68, 95, 99.7],
    fips=fip_list, values=lv_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(215,215,215)', 'width': 0.3},
)

fig.layout.template = None

fig.show()
