import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("formatted_sales.csv")
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)
app.title = "Soul Foods Dashboard"

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div(

    style={
        "backgroundColor": "#eef3f8",
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Segoe UI"
    },

    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#1f3b73",
                "fontSize": "42px",
                "fontWeight": "bold",
                "marginBottom": "8px"
            }
        ),

        html.H3(
            "Sales Analysis Before and After the January 15, 2021 Price Increase",
            style={
                "textAlign": "center",
                "color": "#666666",
                "marginBottom": "35px"
            }
        ),

        html.Div(

            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0px 5px 18px rgba(0,0,0,0.15)",
                "marginBottom": "25px"
            },

            children=[

                html.H3(
                    "Filter by Region",
                    style={
                        "color": "#1f3b73",
                        "marginBottom": "15px"
                    }
                ),

                dcc.RadioItems(

                    id="region",

                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],

                    value="all",

                    inline=True,

                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "30px",
                        "fontSize": "18px",
                        "fontWeight": "600"
                    }

                )

            ]

        ),

        html.Div(

            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginBottom": "25px"
            },

            children=[

                html.Div(
                    id="total_sales_card",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "32%",
                        "textAlign": "center",
                        "boxShadow": "0px 5px 15px rgba(0,0,0,0.15)"
                    }
                ),

                html.Div(
                    id="avg_sales_card",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "32%",
                        "textAlign": "center",
                        "boxShadow": "0px 5px 15px rgba(0,0,0,0.15)"
                    }
                ),

                html.Div(
                    id="region_card",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "32%",
                        "textAlign": "center",
                        "boxShadow": "0px 5px 15px rgba(0,0,0,0.15)"
                    }
                )

            ]

        ),

        html.Div(

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "15px",
                "boxShadow": "0px 5px 18px rgba(0,0,0,0.15)"
            },

            children=[

                dcc.Graph(id="sales_graph")

            ]

        ),

        html.Div(

            style={
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "marginTop": "30px",
                "borderLeft": "6px solid #1f3b73",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
            },

            children=[

                html.H3(
                    "Business Insight",
                    style={"color": "#1f3b73"}
                ),

                html.P(
                    "The dashed green line represents the Pink Morsel price increase on "
                    "15 January 2021. Sales after this date are consistently higher than "
                    "before the increase, indicating that the pricing change did not reduce "
                    "overall revenue."
                )

            ]

        ),

        html.Hr(),

        html.P(
            "Developed by Sasikaran | Dash & Plotly Dashboard",
            style={
                "textAlign": "center",
                "color": "#666666",
                "fontSize": "15px",
                "marginTop": "20px"
            }
        )

    ]

)

# -----------------------------
# Callback
# -----------------------------

@app.callback(

    Output("sales_graph", "figure"),
    Output("total_sales_card", "children"),
    Output("avg_sales_card", "children"),
    Output("region_card", "children"),

    Input("region", "value")

)

def update_dashboard(region):

    if region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == region]

    sales = filtered_df.groupby("date")["Sales"].sum().reset_index()

    total_sales = filtered_df["Sales"].sum()
    average_sales = sales["Sales"].mean()

    fig = px.line(
        sales,
        x="date",
        y="Sales",
        markers=True,
        template="plotly_white"
    )

    fig.update_traces(
        line=dict(color="#1f77b4", width=4),
        marker=dict(size=5)
    )

    fig.update_layout(
        title="Pink Morsel Sales Over Time",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified",
        font=dict(size=15),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=650
    )

    fig.update_xaxes(showgrid=True, gridcolor="#e5e5e5")
    fig.update_yaxes(showgrid=True, gridcolor="#e5e5e5")

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="green",
        line_width=3,
        annotation_text="Price Increase",
        annotation_position="top left"
    )

    total_card = [

        html.H4("Total Sales"),

        html.H2(
            f"${total_sales:,.0f}",
            style={"color": "#1f77b4"}
        )

    ]

    average_card = [

        html.H4("Average Daily Sales"),

        html.H2(
            f"${average_sales:,.0f}",
            style={"color": "#e67e22"}
        )

    ]

    region_card = [

        html.H4("Selected Region"),

        html.H2(
            region.upper(),
            style={"color": "#2ecc71"}
        )

    ]

    return fig, total_card, average_card, region_card


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)