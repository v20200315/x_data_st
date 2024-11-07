import plotly.graph_objects as go


def get_kdj_figure(df_display):
    fig = go.Figure()

    text = [
        f"交易日: {row['trading_date'].strftime('%Y-%m-%d')}<br>"
        f"K: {row['K']:.2f}<br>"
        f"D: {row['D']:.2f}<br>"
        f"J: {row['J']:.2f}"
        for index, row in df_display.iterrows()
    ]

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["K"],
            mode="lines",
            name="K值",
            line=dict(color="blue", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["D"],
            mode="lines",
            name="D值",
            line=dict(color="orange", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_display["trading_date"],
            y=df_display["J"],
            mode="lines",
            name="J值",
            line=dict(color="green", width=1),
            hoverinfo="text",
            text=text,
        )
    )

    # 更新 KDJ 图的布局
    fig.update_layout(
        title="KDJ 指标",
        yaxis_title="值",
        xaxis_title="交易日期",
        xaxis=dict(
            showticklabels=False,
            rangeslider_visible=False,
        ),
    )

    return fig
