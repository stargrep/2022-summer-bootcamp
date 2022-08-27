import pandas as pd
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')
#%%
# Task1,2
# Read data, select target fund
data = pd.DataFrame(pd.read_csv(r'data\QQQ.csv'))
mydata = data[data['CODES'] == 'QQQ']
# Mark Monday, buy 100 shares if Monday
mydata['DATES'] = pd.to_datetime(mydata['DATES'])
mydata['Signal'] = 0
mydata['Signal'][mydata['DATES'].dt.strftime('%A').astype(str) == 'Monday'] = 1
mydata['Shares'] = mydata['Signal'] * 100
# Calculate total shares, cost and assets
mydata['Shares_sum'] = mydata['Shares'].cumsum()
mydata['Cost'] = (mydata['Signal'] * 100 * mydata['OPEN']).cumsum()
mydata['Asset'] = mydata['Shares_sum'] * mydata['CLOSE']
# Evaluating performance
mydata['Profit'] = mydata['Asset'] - mydata['Cost']
acc_ret_t1 = mydata['Profit'].iloc[-1] / mydata['Cost'].iloc[-1]
annual_ret_t1 = acc_ret_t1 * 360 / len(mydata)
# Save the record
mydata_t1 = mydata.copy()
#%%
#Task 3
# Read data and select target fund
data = pd.DataFrame(pd.read_csv(r'data\QQQ.csv'))
mydata = data[data['CODES'] == 'QQQ']
# Mark Monday, buy integral quantity of shares that equals to 1000 dollars if Monday
mydata['DATES'] = pd.to_datetime(mydata['DATES'])
mydata['Signal'] = 0
mydata['Signal'][mydata['DATES'].dt.strftime('%A').astype(str) == 'Monday'] = 1
mydata['Shares'] = mydata['Signal'] * round(1000/mydata['OPEN'])
# initialize parameters that record shares, shares to be sold and cash flow occured with selling
mydata['Shares_sum'] = 0
mydata['Cost'] = (mydata['Signal'] * mydata['Shares'] * mydata['OPEN']).cumsum()
mydata['Asset'] = 0
mydata['Shares_sold'] = 0
mydata['Cost_Asset'] = (mydata['OPEN'] * mydata['Shares']).cumsum()
mydata['Cash_in'] = 0
for t in range(mydata.index[0],mydata.index[-1]+1):
    # At each day, update current shares
    mydata['Shares_sum'].loc[t] = mydata['Shares'].loc[:t].sum()
    # If current revenue is above 50%, sell 25% of total shares
    if mydata['Shares_sum'].loc[t] * mydata['OPEN'].loc[t] / mydata['Cost_Asset'].loc[t] > 1.5:
        # Record how many shares is to be sold
        mydata['Shares_sold'].loc[t] = round(0.25 * mydata['Shares_sum'].loc[t])
        # Subtract sold shares
        mydata['Shares_sum'].loc[t] -= mydata['Shares_sold'].loc[t]
        # Record how much cash received currently
        mydata['Cash_in'].loc[t] = mydata['Shares_sold'].loc[t] * mydata['OPEN'].loc[t]
        # Re-evaluating cost, using first in first out rule
        sold = mydata['Shares_sold'].loc[t]
        for s in range(mydata.index[0],t+1):
            # Find the "first-in"
            if mydata['Shares'].loc[s] > 0:
                # If the "first-in" covers the quantity sold, simply remove the cover part
                if mydata['Shares'].loc[s] >= sold:
                    # Temp records how much does "first-in" cost
                    temp = sold * mydata['OPEN'].loc[s]
                    mydata['Shares'].loc[s] -= sold
                    # Update future asset cost because of selling
                    mydata['Cost_Asset'].loc[t:] -= temp
                    break
                # If single "first-in" cannot cover, keep looking downward until the sold shares is covered
                else:
                    temp = mydata['Shares'].loc[s] * mydata['OPEN'].loc[s]
                    sold -= mydata['Shares'].loc[s]
                    mydata['Shares'].loc[s] = 0
                    # Update future asset cost because of selling
                    mydata['Cost_Asset'].loc[t:] -= temp
    # Update current asset and total cash received
    mydata['Asset'].loc[t] = mydata['Shares_sum'].loc[t] * mydata['CLOSE'].loc[t]
mydata['Cash'] = mydata['Cash_in'].cumsum()
# Evaluating performance and compare with task1,2
mydata['Profit'] = mydata['Asset'] + mydata['Cash'] - mydata['Cost']
acc_ret = mydata['Profit'].iloc[-1] / mydata['Cost'].iloc[-1]
annual_ret = acc_ret * 360 / len(mydata)
plt.plot(mydata_t1['Profit']/mydata_t1['Cost'],color='blue')
plt.plot(mydata['Profit']/mydata['Cost'],color='red')
plt.legend(['Task1,2','Task3'])
plt.annotate(
    'Task1,2 annual return rate: %.2f%%, total return rate: %.2f%%\nTask3 annual return rate: %.2f%%, total return rate: %.2f%%' % (
    annual_ret_t1 * 100, acc_ret_t1 * 100, annual_ret * 100, acc_ret * 100),
    xy=(0.001 * len(mydata_t1), 0.8 * (mydata_t1['Profit'] / mydata_t1['Cost']).max()))
plt.show()