import time
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 记录开始时间
start_time = time.time()

st.title("股票查询数据")

# 设置默认时间
today = datetime.now().date()
default_from_date = today - timedelta(days=180)

# 创建输入框
from_date = st.date_input("选择开始日期", default_from_date)
to_date = st.date_input("选择结束日期", today)

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

        # 计算EMA
        def calculate_ema(prices, span):
            return prices.ewm(span=span, adjust=False).mean()

        # 按股票代码分组，计算MACD
        def calculate_macd(group):
            group = group.sort_values(by="trading_date", ascending=True)
            group["ema_12"] = calculate_ema(group["closing_price"], 12)
            group["ema_26"] = calculate_ema(group["closing_price"], 26)
            group["macd"] = group["ema_12"] - group["ema_26"]
            group["signal_line"] = calculate_ema(group["macd"], 9)
            group["golden_cross"] = (group["macd"] > group["signal_line"]) & (
                group["macd"].shift(1) <= group["signal_line"].shift(1)
            )
            return group

        # 应用MACD计算，选择需要的列以避免警告
        df = (
            df[["trading_date", "stock_code", "closing_price"]]
            .groupby("stock_code")
            .apply(calculate_macd, include_groups=False)
        )

        # 获取最后一个交易日
        last_trading_day = df["trading_date"].max()
        last_day_data = df[df["trading_date"] == last_trading_day]

        # 检查最后一个交易日是否出现金叉
        golden_cross_today = last_day_data[last_day_data["golden_cross"]]

        if not golden_cross_today.empty:
            st.write(
                f"在最后一个交易日 {last_trading_day} 出现金叉的股票({len(golden_cross_today)})："
            )
            st.dataframe(golden_cross_today)
        else:
            st.write(f"在最后一个交易日 {last_trading_day} 没有出现金叉的股票。")
    else:
        st.write(f"请求失败，状态码: {response.status_code}，信息: {response.text}")

# 记录结束时间
end_time = time.time()
# 计算执行时间
execution_time = end_time - start_time

st.write(f"计算完成！执行时间为 {execution_time:.2f} 秒。")
