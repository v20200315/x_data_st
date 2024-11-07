import time
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 记录开始时间
start_time = time.time()

st.title("股票查询数据")


# 定义获取最后一个交易日的函数
def get_last_trading_date():
    resp = requests.get("http://127.0.0.1:8000/api/stock/last_trading_date/")
    if resp.status_code == 200:
        data = resp.json()
        return data["last_trading_date"]  # 假设返回的数据中有 trading_date 字段
    else:
        return None


# 尝试获取最后一个交易日
last_trading_date = get_last_trading_date()

# 根据获取结果设置 today
if last_trading_date:
    last_trading_date = pd.to_datetime(last_trading_date).date()  # 将字符串转换为日期
else:
    last_trading_date = datetime.now().date()  # 获取当前日期

# 设置默认时间
default_from_date = last_trading_date - timedelta(days=10)

# 创建输入框
from_date = st.date_input("选择开始日期", default_from_date)
to_date = st.date_input("选择结束日期", last_trading_date)

# 创建按钮
if st.button("获取股票数据"):
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    # 调用接口
    url = f"http://127.0.0.1:8000/api/stock/date_range/?from={from_str}&to={to_str}"  # 根据您的实际地址调整
    response = requests.get(url)

    if response.status_code == 200:
        # 将返回的数据转换为 DataFrame
        stock_data = response.json()
        df = pd.DataFrame(stock_data)

        # 确保日期列是日期格式
        df["trading_date"] = pd.to_datetime(df["trading_date"]).dt.date
        # large bullish candle
        # medium bullish candle
        # small bullish candle
        # large bearish candle
        # medium bearish candle
        # small bearish candle

        # 根据涨跌幅度标记蜡烛图类型
        def classify_candle(row):
            change = row["price_change_percentage"]
            if change >= 5:
                return "large bullish candle"
            elif 2 <= change < 5:
                return "medium bullish candle"
            elif 0 <= change < 2:
                return "small bullish candle"
            elif change <= -5:
                return "large bearish candle"
            elif -5 < change <= -2:
                return "medium bearish candle"
            elif -2 < change < 0:
                return "small bearish candle"
            else:
                return "no change"

        # 应用分类函数到每一行
        df["candle_type"] = df.apply(classify_candle, axis=1)

        # 根据 stock_code 正序，trading_date 倒序排序
        sorted_df = df.sort_values(
            by=["stock_code", "trading_date"], ascending=[True, False]
        )

        # 根据 candle_type 统计各类型蜡烛图的数量
        candle_counts = (
            sorted_df.groupby(["trading_date", "candle_type"])
            .size()
            .reset_index(name="count")
        )

        # 显示蜡烛图类型及其数量
        st.write(candle_counts)

        # 查找最近三个交易日都是阳线的股票
        bullish_stocks = []
        for stock_code, group in sorted_df.groupby("stock_code"):
            # 获取当前股票的交易记录
            if len(group) >= 3:  # 确保有至少三天的记录
                # 检查最后三个交易日是否都是阳线
                if all("bullish candle" in x for x in group["candle_type"].head(3)):
                    bullish_stocks.append(group.head(3))  # 添加符合条件的最后三行记录

        # 将结果转换为 DataFrame
        bullish_df = (
            pd.concat(bullish_stocks).reset_index(drop=True)
            if bullish_stocks
            else pd.DataFrame(columns=df.columns)
        )

        # 获取最后一个交易日的数据
        last_day_data = bullish_df[bullish_df["trading_date"] == last_trading_date]
        # 重置索引
        last_day_data = last_day_data.reset_index(drop=True)

        # 显示结果
        st.write(f"最近三个交易日都是阳线的股票({len(bullish_df)})：")
        st.write(bullish_df)
        st.write(
            f"最近三个交易日都是阳线的股票(显示最后一个交易日)({len(last_day_data)})："
        )
        st.write(last_day_data)

# 记录结束时间
end_time = time.time()
# 计算执行时间
execution_time = end_time - start_time

st.write(f"计算完成！执行时间为 {execution_time:.2f} 秒。")
