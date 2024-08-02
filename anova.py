import pandas as pd
import os
from scipy import stats


csv_path = os.path.join('csv', 'Code Rate KS = 10,000, BS = 1, DROP = 0.csv')

df = pd.read_csv(csv_path, header=None)

list1 = df.iloc[:, 0]
list2 = df.iloc[:, 1]
list3 = df.iloc[:, 2]
list4 = df.iloc[:, 3]
list5 = df.iloc[:, 4]
list6 = df.iloc[:, 5]
list7 = df.iloc[:, 6]
list8 = df.iloc[:, 7]
list9 = df.iloc[:, 8]

f_statistic, p_value = stats.f_oneway(list1, list2, list3, list4, list5, list6, list7, list8, list9)

print("F-Statistic:", f_statistic)
print("P-Value:", p_value)

if p_value < 0.05:
    print("The difference in means is statistically significant.")
else:
    print("The difference in means is not statistically significant.")
