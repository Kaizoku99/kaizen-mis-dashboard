"""Plotly chart components for Streamlit dashboard."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Consistent color palette
COLORS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]
RYG_CHART_COLORS = {"green": "#10B981", "yellow": "#F59E0B", "red": "#EF4444"}


def line_chart(series_list: list[dict], title: str, y_title: str = "", height: int = 350):
    """
    Render a line chart from API chart series data.
    
    series_list: [{"name": "...", "data": [{"label": "date", "value": num}, ...]}]
    """
    fig = go.Figure()
    
    for i, series in enumerate(series_list):
        labels = [d["label"] for d in series["data"]]
        values = [d["value"] for d in series["data"]]
        
        fig.add_trace(go.Scatter(
            x=labels,
            y=values,
            name=series["name"],
            mode="lines+markers",
            line=dict(color=COLORS[i % len(COLORS)], width=2),
            marker=dict(size=4),
        ))
    
    fig.update_layout(
        title=dict(text=title, font_size=16, x=0.05),
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor="white",
        plot_bgcolor="#F9FAFB",
    )
    
    if y_title:
        fig.update_yaxis(title_text=y_title)
    
    st.plotly_chart(fig, use_container_width=True)


def bar_chart(categories: list[str], values: list[float], 
              title: str, colors: list[str] | None = None,
              status_labels: list[str] | None = None, height: int = 350):
    """Render a bar chart with optional RYG coloring."""
    if colors is None:
        colors = COLORS[:len(categories)]
    
    fig = go.Figure()
    
    # Custom colors per bar based on status
    bar_colors = []
    text_colors = []
    for c in (colors or []):
        if c in RYG_CHART_COLORS:
            bar_colors.append(RYG_CHART_COLORS[c])
            text_colors.append("white")
        else:
            bar_colors.append(c)
            text_colors.append("#374151")
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=(bar_colors if bar_colors else colors),
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(color=text_colors if text_colors else "#374151", size=12),
    ))
    
    fig.update_layout(
        title=dict(text=title, font_size=16, x=0.05),
        height=height,
        margin=dict(l=40, r=20, t=40, b=80),
        paper_bgcolor="white",
        plot_bgcolor="#F9FAFB",
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)


def gauge_chart(value: float, title: str, max_val: float = 100,
                threshold_yellow: float = 70, threshold_red: float = 40):
    """Render a gauge/indicator chart for overall score."""
    # Determine color based on thresholds
    if value >= threshold_yellow:
        color = "#10B981"
    elif value >= threshold_red:
        color = "#F59E0B"
    else:
        color = "#EF4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0, threshold_red], "color": "#FEE2E2"},
                {"range": [threshold_red, threshold_yellow], "color": "#FEF3C7"},
                {"range": [threshold_yellow, max_val], "color": "#D1FAE5"},
            ],
            "threshold": {
                "line": {"color": "#6B7280", "width": 2},
                "thickness": 0.75,
                "value": threshold_yellow,
            },
        },
    ))
    
    fig.update_layout(height=280, margin=dict(l=30, r=30, t=40, b=30))
    st.plotly_chart(fig, use_container_width=True)


def donut_chart(values: list[int], labels: list[str], title: str = ""):
    """Render a donut/pie chart for summary distribution."""
    colors = [RYG_CHART_COLORS.get(l.lower(), "#6B7280") for l in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker_colors=colors,
        textinfo="label+percent",
        textfont_size=13,
        pull=[0.03 if l.lower() == "red" else 0 for l in labels],
    )])
    
    fig.update_layout(
        title=dict(text=title, font_size=14) if title else None,
        height=300,
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        showlegend=False,
    )
    
    st.plotly_chart(fig, use_container_width=True)
