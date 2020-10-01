from scipy import stats
import numpy as np
import statistics

x = [185, 192, 206, 177, 225, 168, 256, 239, 199, 218]
y = [169, 187, 193, 176, 194, 171, 228, 217, 204, 195]
z = [0] * len(x)
for i in range(len(x)):
    z[i] = y[i] - x[i]

avg = sum(z)/ len(z)
std = statistics.stdev(z)

print(z, avg, std)

se = std / len(z)**(1/2)
t_value = (avg - 0) / se

print(t_value)


#v = stats.ttest_1samp(z, avg)
print(v)


print(stats.ttest_ind(x,y))
