#%%
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import fastf1 as fastf1
from sklearn.metrics import r2_score
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
scale = StandardScaler()




sns.set()

session = fastf1.get_session(2025, 'Monaco', 'R')
session.load()
albon = session.get_driver('ALB')
alb = session.laps.pick_drivers('ALB')
sainz = session.get_driver('SAI')
sai = session.laps.pick_drivers('SAI')

alb_df = pd.DataFrame(data=alb)
alb_car_data = alb.get_car_data()
sai_df = pd.DataFrame(data=sai)
sai_car_data = sai.get_car_data()

alb_speed = alb_car_data['Speed']
alb_time = alb_car_data['Time']
#plt.plot(alb_time,alb_speed)

alb_df2 = alb_df[['LapTime', 'Sector1Time','Sector2Time', 'Sector3Time', 'TyreLife', 'IsAccurate']]
alb_df2 = alb_df2.query("IsAccurate == True")
sai_df2 = sai_df[['LapTime', 'Sector1Time','Sector2Time', 'Sector3Time', 'TyreLife', 'IsAccurate']]
sai_df2 = sai_df2.query("IsAccurate == True")

#plt.ylabel('seconds')
#plt.xlabel('laps')

x_values = np.arange(1, alb_df2.get('IsAccurate').count() + 1 ,1)

for col in ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']:
    alb_df2[col] = alb_df2[col].dt.total_seconds()
    sai_df2[col] = sai_df2[col].dt.total_seconds()

'''
plt.plot(x_values, alb_df2['LapTime'], label = 'LapTime')
plt.plot(x_values, alb_df2['Sector1Time'], label = 'Sector1')
plt.plot(x_values, alb_df2['Sector2Time'], label = 'Sector2')
plt.plot(x_values, alb_df2['Sector3Time'], label = 'Sector3')
'''

'''
plt.scatter(x_values,alb_df2['LapTime'], c='b')
plt.scatter(x_values,sai_df2['LapTime'], c='r')
funcALB = np.poly1d(np.polyfit(x_values,alb_df2['LapTime'],6))
funcSAI = np.poly1d(np.polyfit(x_values,sai_df2['LapTime'],7))

rSquaredALB = r2_score(alb_df2['LapTime'], funcALB(x_values))
rSquaredSAI = r2_score(sai_df2['LapTime'], funcSAI(x_values))
print(str(rSquaredALB) + ": ALB r2")
print(str(rSquaredSAI) + ": SAI r2")
print(str(funcSAI(x_values).mean()) + ": SAI avr round times")
print(str(funcALB(x_values).mean()) + ": ALB avr round times")

plt.plot(x_values, funcALB(x_values), c='b', label = 'alb lap times')
plt.plot(x_values, funcSAI(x_values), c='r', label = 'sai lab times')
plt.legend()
#plt.show()
'''

'''
idee für morgen:
- get_car data anschauen für ein fahrer
- welche column haben am meisten einfluss auf den speed
- unnötige data entfernen
- model bauen die speed predicted

multiple regression
'''
carDataWilliams = sai_car_data._append(alb_car_data)
carDataWilliamsX = carDataWilliams[['RPM', 'nGear']]
carDataWilliamsY = carDataWilliams[['Speed']]

carDataWilliamsX[['RPM', 'nGear']] = scale.fit_transform(carDataWilliamsX[['RPM', 'nGear']].values)
carDataWilliamsX = sm.add_constant(carDataWilliamsX)

est = sm.OLS(carDataWilliamsY,carDataWilliamsX).fit()
print(est.summary())

predictionSet = scale.transform([[11000, 8]])
predictionSet = np.insert(predictionSet[0],0,1)
predicted = est.predict(predictionSet)
print(predicted)

#sns.pairplot(carDataWilliamsDF)
#plt.show()
# %%