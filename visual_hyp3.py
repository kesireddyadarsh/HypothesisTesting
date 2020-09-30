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
lv_list = []

for county in county_list:
    bf_restrict = get_cases('NUECES', date_range='03-26~05-20', number_form='infection')
    af_restrict = get_cases('NUECES', date_range='05-21~07-15', number_form='infection')
    t_value, p_value = stats.ttest_rel(bf_restrict, af_restrict)
    lv = round((1 - abs(p_value)) * 100, 1) 
    lv_list.append(lv)
    fip = get_fips(county)
    fip_list.append(fip)


fig = ff.create_choropleth(
    scope=['TX',], 
    legend_title='Confidence Level (%)', title='Restiction Lifted vs Infection Rate',
    binning_endpoints=[20, 40, 68, 95, 99.7],
    fips=fip_list, values=lv_list,
    colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.3},
)



fig.layout.template = None
fig.show()
