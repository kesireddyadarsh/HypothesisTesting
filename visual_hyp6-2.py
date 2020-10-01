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
county_list = get_population().keys()

clean_counties = []
dirty_counties = []

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
        dirty_counties.append(county)
    else:
        clean_counties.append(county)

date_param = '05-21~07-15'

dirty_all, clean_all = [], []
for county in dirty_counties:
    one = get_cases(county, date_range=date_param, number_form='infection')
    dirty_all.append(one)

dirty_avg = [sum(i)/len(dirty_all) for i in zip(*dirty_all)]

for county in clean_counties:
    one = get_cases(county, date_range=date_param, number_form='infection')
    clean_all.append(one)

clean_avg = [sum(i)/len(clean_all) for i in zip(*clean_all)]

# z test
print('z test', ztest(clean_avg, dirty_avg))

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data
df=pd.DataFrame({
    'x': range(len(dirty_avg)), 
    'WithUrban': dirty_avg, 
    'NoUrban': clean_avg, 
})

# multiple line plot
plt.title('Rural Counties with/without Urban Adjacent - Infection Rate')
plt.ylabel('Average Cases per million population')
plt.xticks([1, 19, 37, 55], ["05-21", "06-10", "06-25", "07-15"])
plt.plot( 'x', 'WithUrban', data=df, marker='', color='salmon', linewidth=2)
plt.plot( 'x', 'NoUrban', data=df, marker='', color='royalblue', linewidth=2, linestyle='dashed')
plt.legend()

png_name = 'output/{}.png'.format(__file__[:-3])
plt.savefig(png_name)
plt.show()
