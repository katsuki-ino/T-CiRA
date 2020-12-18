import plotly.graph_objects as go
import plotly.io as pio

scatter_layout = go.Layout(
    plot_bgcolor='#3B3B3B',
    paper_bgcolor='#222222',
    # bordercolor='#3498DB',
    xaxis={
        'color': '#839496',
        'tickcolor': '#839496'
    },
    yaxis={
        'color': '#839496',
        'tickcolor': '#839496'
    },
    legend=dict(font=dict(size=16, color='#839496'),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                itemsizing='constant'),
    margin=dict(
        l=30,
        r=30,
        t=65,
        b=0
    ),
)

pio.templates['amanogawa'] = go.layout.Template(layout=go.Layout(scatter_layout))