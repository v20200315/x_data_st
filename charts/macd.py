import plotly.graph_objects as go


def get_macd_figure(df_display):
    fig = go.Figure()

    text = [
        f"交易日: {row['trading_date'].strftime('%Y-%m-%d')}<br>"
        f"DIFF: {row['MACD']:.2f}<br>"
        f"DEA: {row['Signal_Line']:.2f}"
        for index, row in df_display.iterrows()
    ]

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["MACD"],
            mode="lines",
            name="MACD",
            line=dict(color="blue", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["Signal_Line"],
            mode="lines",
            name="信号线",
            line=dict(color="orange", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    # 更新 MACD 图的布局
    fig.update_layout(
        title="MACD 指标",
        yaxis_title="MACD 值",
        xaxis_title="交易日期",
        xaxis=dict(
            showticklabels=True,
            rangeslider_visible=False,
        ),
    )

    return fig
