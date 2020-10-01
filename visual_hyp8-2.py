import numpy as np
from data_acq import *

# Hypothesis 5 (z test)
font = {
    #'family': 'Times New Roman',
    'color':  'green',
    'weight': 'normal',
    'size': 12,
}
r_list, u_list= get_rural_urban_counties()
date_param = '05-21~07-15'
x, y = [], []

r_all, u_all = [], []
for county in u_list:
    one = get_cases(county, date_range=date_param, number_form='infection')
    u_all.append(one)

u_avg = [sum(i)/len(u_list) for i in zip(*u_all)]

for county in r_list:
    one = get_cases(county, date_range=date_param, number_form='infection')
    r_all.append(one)

r_avg = [sum(i)/len(r_list) for i in zip(*r_all)]

# z test
print('z test', ztest(r_avg, u_avg))

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data
df=pd.DataFrame({
    'x': range(len(u_avg)), 
    'Rural': u_avg, 
    'Urban': r_avg, 
})

# multiple line plot
plt.title('Rural and Urban Infection Rate')
plt.ylabel('Average Cases per million population')
plt.xticks([1, 19, 37, 55], ["05-21", "06-10", "06-25", "07-15"])
plt.plot( 'x', 'Rural', data=df, marker='', color='green', linewidth=2)
plt.plot( 'x', 'Urban', data=df, marker='', color='blue', linewidth=2, linestyle='dashed')
plt.legend()

png_name = 'output/{}.png'.format(__file__[:-3])
plt.savefig(png_name)
plt.show()
