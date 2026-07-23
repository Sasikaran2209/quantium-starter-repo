import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

df = pd.read_csv("formatted_sales.csv")


df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")


daily_sales = df.groupby("date")["sales"].sum().reset_index()


fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales"
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),

    dcc.Graph(
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=True)