import plotly.graph_objects as go


def get_candlestick_figure(df_display):
    text = [
        f"交易日: {row['trading_date'].strftime("%Y-%m-%d")}<br>"
        + f"开盘价: {row['opening_price']}<br>"
        + f"最高价: {row['highest_price']}<br>"
        + f"最低价: {row['lowest_price']}<br>"
        + f"收盘价: {row['closing_price']}<br>"
        + f"成交量: {row['trading_volume']}<br>"
        + f"成交额: {row['trading_amount']}<br>"
        + f"振幅: {row['price_range']}<br>"
        + f"涨跌幅: {row['price_change_percentage']}<br>"
        + f"涨跌额: {row['price_change_amount']}<br>"
        + f"换手率: {row['turnover_rate']}<br>"
        + f"5均线: {row['5_day_ma']}<br>"
        + f"20均线: {row['20_day_ma']}<br>"
        + f"60均线: {row['60_day_ma']}<br>"
        + f"120均线: {row['120_day_ma']}<br>"
        + f"250均线: {row['250_day_ma']}"
        for index, row in df_display.iterrows()
    ]

    # 创建蜡烛图
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df_display["trading_date"],
                open=df_display["opening_price"],
                high=df_display["highest_price"],
                low=df_display["lowest_price"],
                close=df_display["closing_price"],
                name="蜡烛图",
                hoverinfo="text",
                text=text,
            )
        ]
    )

    fig.update_traces(
        increasing_line_color="red",
        decreasing_line_color="green",
    )

    dict(name="5_day_ma", color="green")

    # 添加均线到图表
    for ma in [
        dict(key="5_day_ma", name="5日均线", color="darkgreen"),
        dict(key="20_day_ma", name="20日均线", color="gold"),
        dict(key="60_day_ma", name="60日均线", color="darkblue"),
        dict(key="120_day_ma", name="120日均线", color="brown"),
        dict(key="250_day_ma", name="250日均线", color="gray"),
    ]:
        fig.add_trace(
            go.Scatter(
                x=df_display["trading_date"],
                y=df_display[ma["key"]],
                mode="lines",
                name=ma["name"],
                line=dict(color=ma["color"], width=1),
                hoverinfo="text",
                text=text,
            )
        )

    # 更新图表布局
    fig.update_layout(
        yaxis_title="价格",
        xaxis=dict(
            showticklabels=True,
            rangeslider_visible=False,
            title="交易日期",
        ),
    )

    return fig
