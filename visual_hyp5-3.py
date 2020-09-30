import numpy as np
import matplotlib.pyplot as plt
from data_acq import *

# Hypothesis 5 (z test)
font = {
    #'family': 'Times New Roman',
    'color':  'green',
    'weight': 'normal',
    'size': 12,
}
county_list = get_population().keys()
date_param = '06-04~07-15'
x, y = [], []
for county in county_list:
    tran_data = get_cases(county, date_range=date_param, number_form='transmission', mv_avg_days=42)
    tran_rate = round(tran_data[0], 1)
    density = get_density(county)
    x.append(density)
    y.append(tran_rate)

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_info = 'R^2 = {}'.format(round(r_value**2, 3))
linear_eq = 'y = {}*x + {}'.format(
    round(slope,3), 
    round(intercept, 3),
    round(r_value**2, 3)
)

coef = np.polyfit(x, y, slope)
poly1d_fn = np.poly1d(coef) 

fig, ax = plt.subplots()
plt.xlabel('Population Density (per sq mi)')
plt.ylabel('Cases per million population ({})'.format(date_param))
ax.set_title('Population Density vs Transmission Rate')
plt.text(
    x=1500,
    y=50, 
    s=r_info,
    rotation=0,
    horizontalalignment='left',
    verticalalignment='top',
    multialignment='center',
    fontdict=font
)
plt.text(
    x=1500,
    y=140, 
    s=linear_eq,
    rotation=0,
    horizontalalignment='left',
    verticalalignment='top',
    multialignment='center',
    fontdict=font
)

plt.plot(x,y, 'yo', x, poly1d_fn(x), '--k')
png_name = 'output/{}.png'.format(__file__[:-3])
plt.savefig(png_name)

#plt.show()

