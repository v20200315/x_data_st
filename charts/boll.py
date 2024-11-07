import plotly.graph_objects as go


def get_boll_figure(df_display):
    fig = go.Figure()

    text = [
        f"交易日: {row['trading_date'].strftime('%Y-%m-%d')}<br>"
        f"UP: {row['Upper_Band']:.2f}<br>"
        f"MID: {row['SMA_20']:.2f}<br>"
        f"LOW: {row['Lower_Band']:.2f}"
        for index, row in df_display.iterrows()
    ]

    # 添加 Bollinger Bands 到图表
    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["Upper_Band"],
            mode="lines",
            name="上带",
            line=dict(color="red", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["SMA_20"],
            mode="lines",
            name="20日均线",
            line=dict(color="blue", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["Lower_Band"],
            mode="lines",
            name="下带",
            line=dict(color="green", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    # 更新图表布局
    fig.update_layout(
        title="BOLL 指标",
        yaxis_title="价格",
        xaxis=dict(
            showticklabels=False,
            rangeslider_visible=False,
        ),
    )

    return fig
