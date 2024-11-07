import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

st.title("股票查询数据")

# 设置默认时间
today = datetime.now().date()
default_from_date = today - timedelta(days=10)

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

        st.dataframe(df)
    else:
        st.write(f"请求失败，状态码: {response.status_code}，信息: {response.text}")
