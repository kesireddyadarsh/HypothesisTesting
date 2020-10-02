import numpy as np
import matplotlib.pyplot as plt
from data_acq import *

# Hypothesis 5 (z test)
font = {
    #'family': 'Times New Roman',
    'color':  'orange',
    'weight': 'normal',
    'size': 12,
}
county_list = get_population().keys()
x, y = [], []


date_param = '04-12~09-21'
tsa = 'CORPUS CHRISTI'
x = get_hospitalization(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
y = get_fatality(tsa=tsa, date_range=date_param)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
level = round(1 - abs(p_value), 4) * 100 

print(p_value)
print(level)

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_info = 'R^2 = {}'.format(round(r_value**2, 3))
linear_eq = 'y = {}*x + {}'.format(
    round(slope,3), 
    round(intercept, 3),
    round(r_value**2, 3)
)

coef = np.polyfit(x, y, 1)
poly1d_fn = np.poly1d(coef)

fig, ax = plt.subplots()
plt.xlabel('Hospitalization Rate (%)')
plt.ylabel('Fatality Rate (%)')
ax.set_title('Corpus Christi ({})- Hospitalization Rate vs Fatality Rate'.format(date_param))
plt.text(
    x=30,
    y=2, 
    s=r_info,
    rotation=0,
    horizontalalignment='left',
    verticalalignment='top',
    multialignment='center',
    fontdict=font
)
plt.text(
    x=30,
    y=1, 
    s=linear_eq,
    rotation=0,
    horizontalalignment='left',
    verticalalignment='top',
    multialignment='center',
    fontdict=font
)

plt.plot(x,y, 'go', x, poly1d_fn(x), '--r')
png_name = 'output/{}.png'.format(__file__[:-3])
plt.savefig(png_name)

#plt.show()

