import matplotlib.pyplot as plt
import matplotlib
from data_acq import *

tsa_list = get_region2county().keys()
lv_list1 = []
lv_list2 = []
for tsa in tsa_list:
    # Hypothesis 1 (z-test)
    date_param = '04-12~09-21'
    x = get_hospitalization(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
    y = get_fatality(tsa=tsa, date_range=date_param)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    level = round(1 - abs(p_value), 4) * 100
    lv_list1.append(level)

    # Hypothesis 2 (z-test)
    date_param = '04-23~09-21'
    x = get_icu(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
    y = get_fatality(tsa=tsa, date_range=date_param)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    level = round(1 - abs(p_value), 4) * 100
    lv_list2.append(level)


x = np.arange(len(tsa_list))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, lv_list1, width, label='Hospitalization')
rects2 = ax.bar(x + width/2, lv_list2, width, label='ICU')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Confidence Level (%)')
ax.set_title('Fatality to Hopitalization and ICU')
ax.set_xticks(x)
ax.set_xticklabels(tsa_list)
ax.legend()

#fig.tight_layout()

plt.xticks(fontsize=7, rotation=-80)
png_name = 'output/{}.png'.format(__file__[:-3])
plt.savefig(png_name)
#plt.show()
