import plotly.express as px
import plotly.graph_objects as go


def create_radar_chart(df):
    fig = px.line_polar(df, r="Score", theta="Category", line_close=True)
    fig.update_traces(fill="toself")
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False
    )
    return fig


def create_gauge_chart(score):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Overall AI Readiness Score"},
            gauge={
                "axis": {"range": [0, 5], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 1], "color": "red"},
                    {"range": [1, 2], "color": "orange"},
                    {"range": [2, 3], "color": "yellow"},
                    {"range": [3, 4], "color": "lightgreen"},
                    {"range": [4, 5], "color": "green"},
                ],
            },
        )
    )
    return fig


def create_bar_chart(scores, title):
    fig = go.Figure(
        go.Bar(
            x=list(scores.keys()),
            y=list(scores.values()),
            text=list(scores.values()),
            textposition='auto',
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Category",
        yaxis_title="Score",
        yaxis=dict(range=[0, 5])
    )
    return fig
