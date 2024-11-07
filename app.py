import streamlit as st
import pandas as pd
import requests

from charts.boll import get_boll_figure
from charts.candlestick import get_candlestick_figure
from charts.kdj import get_kdj_figure
from charts.macd import get_macd_figure

# 设置页面标题
st.title("股票蜡烛图")

# 用户输入股票代码和日期范围 eg.301628
stock_code = st.text_input("股票代码", "600519")

# 获取数据的按钮
if st.button("获取数据"):
    # 构建API URL
    url = f"http://127.0.0.1:8000/api/stock/{stock_code}/"

    # 调用API
    response = requests.get(url)

    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        df = pd.DataFrame(data)

        # 将交易日期转换为datetime格式
        df["trading_date"] = pd.to_datetime(df["trading_date"])

        # 按照交易日期排列数据
        df = df.sort_values(by="trading_date", ascending=True)
        # 计算日均线
        df["5_day_ma"] = df["closing_price"].rolling(window=5).mean().round(2)
        df["20_day_ma"] = df["closing_price"].rolling(window=20).mean().round(2)
        df["60_day_ma"] = df["closing_price"].rolling(window=60).mean().round(2)
        df["120_day_ma"] = df["closing_price"].rolling(window=120).mean().round(2)
        df["250_day_ma"] = df["closing_price"].rolling(window=250).mean().round(2)

        # 计算 MACD
        df["EMA_12"] = df["closing_price"].ewm(span=12, adjust=False).mean()
        df["EMA_26"] = df["closing_price"].ewm(span=26, adjust=False).mean()
        df["MACD"] = df["EMA_12"] - df["EMA_26"]
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

        # 计算 KDJ
        low_min = df["lowest_price"].rolling(window=9).min()
        low_max = df["highest_price"].rolling(window=9).max()
        df["RSV"] = (df["closing_price"] - low_min) / (low_max - low_min) * 100
        df["K"] = df["RSV"].ewm(alpha=1 / 3, adjust=False).mean()
        df["D"] = df["K"].ewm(alpha=1 / 3, adjust=False).mean()
        df["J"] = 3 * df["K"] - 2 * df["D"]

        # 计算 Bollinger Bands
        window = 20  # 使用20日SMA
        df["SMA_20"] = df["closing_price"].rolling(window=window).mean()
        df["Std_Dev"] = df["closing_price"].rolling(window=window).std()
        df["Upper_Band"] = df["SMA_20"] + (df["Std_Dev"] * 2)  # 上带
        df["Lower_Band"] = df["SMA_20"] - (df["Std_Dev"] * 2)  # 下带

        # 将数据存储在session_state中
        st.session_state.df = df

# 检查session_state中是否有数据
if "df" in st.session_state:
    df = st.session_state.df
    default_display = 100
    total_data = len(df)

    # 使用滑块选择显示的数据范围，最大为100条
    num_to_display = st.slider(
        "选择显示的数据条数",
        min_value=50,
        max_value=max(100, total_data),
        value=default_display,
    )

    df_display = df.tail(num_to_display)

    # 显示图表
    st.plotly_chart(get_candlestick_figure(df_display))

    # 创建 MACD 图
    st.plotly_chart(get_macd_figure(df_display))

    # 创建 KDJ 图
    st.plotly_chart(get_kdj_figure(df_display))

    # 创建 BOLL 图
    st.plotly_chart(get_boll_figure(df_display))

    st.write(df_display)
else:
    st.write("请先点击“获取数据”按钮以加载数据。")
