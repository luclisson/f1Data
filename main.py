#%%
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastf1 as fastf1



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


x_values = np.arange(1, alb_df2.get('IsAccurate').count() + 1 ,1)


plt.plot(x_values, alb_df2['LapTime'], label = 'LapTime')
plt.plot(x_values, alb_df2['Sector1Time'], label = 'Sector1')
plt.plot(x_values, alb_df2['Sector2Time'], label = 'Sector2')
plt.plot(x_values, alb_df2['Sector3Time'], label = 'Sector3')
plt.show()
