import pandas as pd
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')
#%%
# Task1,2
data = pd.DataFrame(pd.read_csv(r'C:\Users\78450\Desktop\INT\2022-summer-bootcamp-main\2022-summer-bootcamp-main\week03\mini-project-1\data\QQQ.csv'))
mydata = data[data['CODES'] == 'QQQ']
mydata['DATES'] = pd.to_datetime(mydata['DATES'])
mydata['Signal'] = 0
mydata['Signal'][mydata['DATES'].dt.strftime('%A').astype(str) == 'Monday'] = 1
mydata['Cost'] = mydata['Signal'] * 100 * mydata['OPEN']
mydata['Shares'] = mydata['Signal'] * 100
mydata['Shares_sum'] = mydata['Shares'].cumsum()
mydata['Cost_sum'] = mydata['Cost'].cumsum()
mydata['Asset'] = mydata['Shares_sum'] * mydata['CLOSE']
mydata['Profit'] = mydata['Asset'] - mydata['Cost_sum']
acc_ret = mydata['Profit'].iloc[-1] / mydata['Cost_sum'].iloc[-1]
annual_ret = acc_ret * 360 / len(mydata)
plt.plot(mydata['Profit']/mydata['Cost_sum'])
plt.annotate('Annual return rate: %.2f%%, total return rate: %.2f%%' % (annual_ret*100, acc_ret*100),
             xy=(0.01 * len(mydata), 0.8 * (mydata['Profit']/mydata['Cost_sum']).max()))
plt.show()
#%%
#Task 3
data = pd.DataFrame(pd.read_csv(r'C:\Users\78450\Desktop\INT\2022-summer-bootcamp-main\2022-summer-bootcamp-main\week03\mini-project-1\data\QQQ.csv'))
mydata = data[data['CODES'] == 'QQQ']
mydata['DATES'] = pd.to_datetime(mydata['DATES'])
mydata['Signal'] = 0
mydata['Signal'][mydata['DATES'].dt.strftime('%A').astype(str) == 'Monday'] = 1
mydata['Shares'] = mydata['Signal'] * round(1000/mydata['OPEN'])
mydata['Shares_sum'] = 0
mydata['Cost'] = (mydata['Signal'] * mydata['Shares'] * mydata['OPEN']).cumsum()
mydata['Asset'] = 0
mydata['Shares_sold'] = 0
mydata['Cost_Asset'] = (mydata['OPEN'] * mydata['Shares']).cumsum()
mydata['Cash_in'] = 0
for t in range(mydata.index[0],mydata.index[-1]+1):
    mydata['Shares_sum'].loc[t] = mydata['Shares'].loc[:t].sum()
    if mydata['Shares_sum'].loc[t] * mydata['OPEN'].loc[t] / mydata['Cost_Asset'].loc[t] > 1.5:
        mydata['Shares_sold'].loc[t] = round(0.25 * mydata['Shares_sum'].loc[t])
        mydata['Shares_sum'].loc[t] -= mydata['Shares_sold'].loc[t]
        mydata['Cash_in'].loc[t] = mydata['Shares_sold'].loc[t] * mydata['OPEN'].loc[t]
        sold = mydata['Shares_sold'].loc[t]
        for s in range(mydata.index[0],t+1):
            if mydata['Shares'].loc[s] > 0:
                if mydata['Shares'].loc[s] >= sold:
                    temp = mydata['Shares'].loc[s] * mydata['OPEN'].loc[s]
                    mydata['Shares'].loc[s] -= sold
                    mydata['Cost_Asset'].loc[t] -= temp
                    break
                else:
                    temp = mydata['Shares'].loc[s] * mydata['OPEN'].loc[s]
                    sold -= mydata['Shares'].loc[s]
                    mydata['Shares'].loc[s] = 0
                    mydata['Cost_Asset'].loc[t] -= temp
    mydata['Asset'].loc[t] = mydata['Shares_sum'].loc[t] * mydata['CLOSE'].loc[t]
mydata['Cash'] = mydata['Cash_in'].cumsum()
mydata['Profit'] = mydata['Asset'] + mydata['Cash'] - mydata['Cost']
acc_ret = mydata['Profit'].iloc[-1] / mydata['Cost'].iloc[-1]
annual_ret = acc_ret * 360 / len(mydata)
plt.plot(mydata['Profit']/mydata['Cost'])
plt.annotate('Annual return rate: %.2f%%, total return rate: %.2f%%' % (annual_ret*100, acc_ret*100),
             xy=(0.01 * len(mydata), 0.8 * (mydata['Profit']/mydata['Cost']).max()))
plt.show()