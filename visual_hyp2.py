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

date_param = '04-23~09-21'
fip_list = []
lv_list = []

tsa_list = get_region2county().keys()
for tsa in tsa_list:
    county_list = get_region2county(tsa)
    for county in county_list:
        x = get_icu(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
        y = get_fatality(tsa=tsa, date_range=date_param)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        lv = round(1 - abs(p_value), 4) * 100 
        lv_list.append(lv)
        fip = get_fips(county)
        fip_list.append(fip)

fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='Confidence Level (%)', title='ICU Rate vs Fatality Rate (by TSA area)',
    binning_endpoints=[20, 40, 68, 95, 99.7],
    fips=fip_list, values=lv_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(215,215,215)', 'width': 0.9},
)

fig.layout.template = None

fig.show()
