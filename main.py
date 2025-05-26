#%%
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastf1 as fastf1
from sklearn.metrics import r2_score

session = fastf1.get_session(2025, 'Monaco', 'R')
session.load()
albon = session.get_driver('ALB')
alb = session.laps.pick_drivers('ALB')

alb_df = pd.DataFrame(data=alb)
alb_car_data = alb.get_car_data()

alb_speed = alb_car_data['Speed']
alb_time = alb_car_data['Time']
#plt.plot(alb_time,alb_speed)

alb_df2 = alb_df[['LapTime', 'Sector1Time','Sector2Time', 'Sector3Time', 'TyreLife', 'IsAccurate']]
alb_df2 = alb_df2.query("IsAccurate == True")

plt.ylabel('seconds')
plt.xlabel('laps')

x_values = np.arange(1, alb_df2.get('IsAccurate').count() + 1 ,1)

for col in ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']:
    alb_df2[col] = alb_df2[col].dt.total_seconds()

'''
plt.plot(x_values, alb_df2['LapTime'], label = 'LapTime')
plt.plot(x_values, alb_df2['Sector1Time'], label = 'Sector1')
plt.plot(x_values, alb_df2['Sector2Time'], label = 'Sector2')
plt.plot(x_values, alb_df2['Sector3Time'], label = 'Sector3')
'''
plt.scatter(x_values,alb_df2['LapTime'])
func = np.poly1d(np.polyfit(x_values,alb_df2['LapTime'],6))

rSquared = r2_score(alb_df2['LapTime'], func(x_values))
print(rSquared)
plt.plot(x_values, func(x_values), c='r')
plt.legend()
plt.show()


'''
idee für morgen:
- get_car data anschauen für ein fahrer
- welche column haben am meisten einfluss auf den speed
- unnötige data entfernen
- model bauen die speed predicted

multiple regression
'''
# %%