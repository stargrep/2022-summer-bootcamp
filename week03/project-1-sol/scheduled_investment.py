import pandas as pd
import datetime as dt

RAW_DATA_NAME = "data/QQQ.csv"
ANALYSIS_RESULT_DATA_NAME = "data/QQQ-result.csv"
ANALYSIS_FIXED_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost.csv"
ANALYSIS_FIXED_SELL_RESULT_DATA_NAME = "data/QQQ-result-fixed-cost-sell.csv"


def read_data() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_NAME)


def write_data(data: pd.DataFrame, file_name: str = ANALYSIS_RESULT_DATA_NAME) -> None:
    return data.to_csv(file_name, index=False)


def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y-%m-%d').strftime('%A') == 'Monday'


# 从年数，回报倍数得到年化收益. e.g. 0.1 -> 10% 年化收益
def annual_return(num_of_year: int, times: float) -> float:
    return pow(times, 1 / num_of_year) - 1.0


def calculate_scheduled_investment(data: pd.DataFrame, shares: int = 10) -> ():
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
            positions.append(positions[-1] + shares)
            cost.append(cost[i - 1] + open_price * shares)
        else:
            positions.append(positions[-1])
            cost.append(cost[i - 1])
        assets.append(open_price * positions[-1])
        if cost[i] > 0:
            percentage.append(assets[i] / cost[i])
        else:
            percentage.append(0)
    return positions, cost, assets, percentage


def export_result() -> float:
    # 生成 {first_name}_QQQ-result.csv, 目标是跟QQQ-result-expected.csv 一致
    # 在这里调用 calculate_scheduled_investment, 并且赋值
    # 到asset 和cost.
    # 最后返回十年的年化率
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


# -- Recommend to copy and write to a new .csv file, so we will not mix Part 3 with Part 1 or 2
def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame, fixed_cost: float = 1000) -> ():
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
            shares = fixed_cost // open_price
            positions.append(positions[-1] + shares)
            cost.append(cost[i - 1] + open_price * shares)
        else:
            positions.append(positions[-1])
            cost.append(cost[i - 1])
        assets.append(open_price * positions[-1])
        if cost[i] > 0:
            percentage.append(assets[i] / cost[i])
        else:
            percentage.append(0)
    return positions, cost, assets, percentage


def get_annual_return_fixed_cost() -> float:
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment_fixed_cost(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_FIXED_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


def calculate_scheduled_investment_fixed_cost_with_sell(data: pd.DataFrame,
                                                        fixed_cost: float = 1000,
                                                        sell_multiply: float = 2.0,
                                                        sell_percentage: float = 0.25) -> ():
    """

    :param data:
    :param sell_point: e.g. when asset equals to double of cost we can sell.
    :param sell_percentage: e.g. we can sell 25%.
    :return:
    """
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    percentage = [0.0]
    min_asset = 30000
    min_days = 5
    profit = 0
    days = 0
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        if assets[i - 1] >= min_asset and days >= min_days and assets[i - 1] >= sell_multiply * cost[i - 1]:
            # sell
            sell_share = int(positions[i - 1] * sell_percentage)
            positions.append(positions[i - 1] - sell_share)
            cost.append(cost[i - 1] - cost[i - 1] / positions[i - 1] * sell_share)
            assets.append(assets[i - 1] - assets[i - 1] / positions[i - 1] * sell_share)
            profit += assets[i - 1] - assets[i]
            days = 0
            if cost[i] > 0:
                percentage.append(assets[i] / cost[i])
            else:
                percentage.append(0)
            continue
        else:
            days += 1

        if is_monday(date):
            shares = fixed_cost // open_price
            positions.append(positions[-1] + shares)
            cost.append(cost[i - 1] + open_price * shares)
        else:
            positions.append(positions[-1])
            cost.append(cost[i - 1])
        assets.append(open_price * positions[-1])
        if cost[i] > 0:
            percentage.append(assets[i] / cost[i])
        else:
            percentage.append(0)
    print("profit: ", profit)
    return positions, cost, assets, percentage


def get_annual_return_fixed_cost_with_sell() -> float:
    df = read_data()
    df['POSITIONS'], cost, assets, percentage = calculate_scheduled_investment_fixed_cost_with_sell(df)
    df['COST'] = cost
    df['ASSETS'] = assets
    df['PERCENTAGE'] = percentage
    write_data(df, ANALYSIS_FIXED_SELL_RESULT_DATA_NAME)
    return annual_return(10, assets[-1] / cost[-1])  # 10 years


# -- TODO: Part 3 (END)


if __name__ == '__main__':
    print("Investment Return: ", export_result() * 100, "%")
    print("Investment Return: ", get_annual_return_fixed_cost() * 100, "%")
    print("Investment Return: ", get_annual_return_fixed_cost_with_sell() * 100, "%")