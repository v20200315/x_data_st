import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# 设置页面标题
st.title("股票数据查询")

# 计算初始日期
today = datetime.now().date()
default_from_date = today - timedelta(days=60)

# 创建日期输入框
from_date = st.date_input("选择开始日期", default_from_date)
to_date = st.date_input("选择结束日期", today)

# 创建按钮，点击后调用接口
if st.button("获取股票数据"):
    # 确保两个日期都被选择
    if from_date and to_date:
        # 将日期格式化为字符串
        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")

        # 调用接口
        url = f"http://127.0.0.1:8000/api/stock/date_range/?from={from_str}&to={to_str}"  # 根据您的实际地址调整
        response = requests.get(url)

        # 检查响应状态
        if response.status_code == 200:
            # 将响应数据转换为 DataFrame
            data = response.json()
            df = pd.DataFrame(data)

            """
            MACD（移动平均收敛散发指数）通常由以下几个部分组成：
            1. 短期指数移动平均线（EMA）：通常使用 12 天的 EMA。
            2. 长期指数移动平均线（EMA）：通常使用 26 天的 EMA。
            3. MACD 线：短期 EMA 减去长期 EMA。
            4. 信号线：MACD 线的 9 天 EMA。
            5. 金叉：当 MACD 线从下向上穿过信号线时，称为金叉。
            """

            # 计算 MACD 并筛选出金叉股票
            df["trading_date"] = pd.to_datetime(df["trading_date"])
            df = df.sort_values(by=["stock_code", "trading_date"])

            # 计算MACD指标
            def calculate_macd(data):
                # 计算短期和长期 EMA
                short_ema = data["closing_price"].ewm(span=12, adjust=False).mean()
                long_ema = data["closing_price"].ewm(span=26, adjust=False).mean()
                # MACD线
                macd = short_ema - long_ema
                # 信号线
                signal_line = macd.ewm(span=9, adjust=False).mean()
                return macd, signal_line

            df["macd"], df["signal_line"] = zip(
                *df.groupby("stock_code").apply(calculate_macd)
            )

            # 检查金叉情况
            def check_macd_cross(data):
                # 检查最后两个交易日的 MACD 和信号线
                if len(data) < 2:
                    return None  # 不足两个交易日无法判断
                last_row = data.iloc[-1]
                second_last_row = data.iloc[-2]
                return (
                    second_last_row["macd"] < second_last_row["signal_line"]
                    and last_row["macd"] > last_row["signal_line"]
                )


            # 筛选出最后一个交易日发生金叉的股票
            golden_cross_stocks = df.groupby("stock_code").filter(check_macd_cross)
            # 获取最后一个交易日的股票列表
            last_trading_day = df["trading_date"].max()
            golden_cross_stocks_last_day = golden_cross_stocks[
                golden_cross_stocks["trading_date"] == last_trading_day
            ]

            # 显示结果
            if not golden_cross_stocks_last_day.empty:
                st.write("最后一个交易日发生金叉的股票：")
                st.dataframe(
                    golden_cross_stocks_last_day[["trading_date", "stock_code"]]
                )
            else:
                st.write("没有找到最后一个交易日发生金叉的股票。")

        else:
            st.error(
                f"错误：{response.json().get('error', '无法获取数据')}"
            )  # 显示错误信息
    else:
        st.warning("请确保选择了开始日期和结束日期。")
