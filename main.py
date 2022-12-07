import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

df_average_house_and_salary = pd.read_csv("house_salary_cleaned.csv")

df_gender_pay_2015 = pd.read_csv("gender_2015.csv")
df_gender_pay_2016 = pd.read_csv("gender_2016.csv")
df_gender_pay_2017 = pd.read_csv("gender_2017.csv")
df_gender_pay_2018 = pd.read_csv("gender_2018.csv")
df_gender_pay_2019 = pd.read_csv("gender_2019.csv")
df_gender_pay_2020 = pd.read_csv("gender_2020.csv")
df_gender_pay_2021 = pd.read_csv("gender_2021.csv")
df_gender_pay_2022 = pd.read_csv("gender_2022.csv")

gender_pay_dfs = {
    "2015": df_gender_pay_2015,
    "2016": df_gender_pay_2016,
    "2017": df_gender_pay_2017, 
    "2018": df_gender_pay_2018,
    "2019": df_gender_pay_2019,
    "2020": df_gender_pay_2020,
    "2021": df_gender_pay_2021,
    "2022": df_gender_pay_2022,
}

df_average_house_uk = pd.read_csv("average_uk_house_cleaned.csv")

df_second_homes = pd.read_csv("second_homes.csv")
df_second_homes= df_second_homes.replace(',','', regex=True)
df_second_homes = df_second_homes.apply(pd.to_numeric)

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", id="card-title"),
            html.H2("100", id="card-value"),
            html.P("Description", id="card-description")
        ]
    )
)

house_salary_fig = make_subplots(specs=[[{"secondary_y": True}]])

house_salary_fig.add_trace(go.Scatter(x=df_average_house_and_salary["Year"], y=df_average_house_and_salary["Average house price adj. by inflation (pounds)"], name="average house price"), secondary_y=False,)
house_salary_fig.add_trace(go.Scatter(x=df_average_house_and_salary["Year"], y=df_average_house_and_salary["Median Salary adj. by inflation (pounds)"],name="average wage"), secondary_y=True,)

uk_house_fig = px.line(df_average_house_uk, x=df_average_house_uk["Year"], y=df_average_house_uk.columns)
uk_house_fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

second_homes_fig = px.bar(df_second_homes, x="year", y="Scotland")
second_homes_fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

second_homes_prices_fig = make_subplots(specs=[[{"secondary_y": True}]])
second_homes_prices_fig.add_trace(go.Scatter(x=df_second_homes["year"], y=df_second_homes["Scotland"], name="second homes"), secondary_y=False,)
second_homes_prices_fig.add_trace(go.Scatter(x=df_average_house_uk["Year"], y=df_average_house_uk["Scotland "],name="average house price"), secondary_y=True,)

app.layout = html.Div([
    dbc.Row([
       html.H1('UK housing statistics', style={'text-align':'center'}),

       
                    
    ]
    ),
    dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('Gender Pay Pie Chart'),
                        dcc.Graph(
                            id="gender_pie",
                            figure = {}
                        )
                    ],
                    className='bg-white'
                    ),
                dbc.Col(
                    [
                        html.H2('Gender Pay Settings'), 
                        dcc.Dropdown(id="year",
                            options=[
                                {"label": "2015", "value": "2015"},
                                {"label": "2016", "value": "2016"},
                                {"label": "2017", "value": "2017"},
                                {"label": "2018", "value": "2018"},
                                {"label": "2019", "value": "2019"},
                                {"label": "2020", "value": "2020"},
                                {"label": "2021", "value": "2021"},
                                {"label": "2022", "value": "2022"},
                            ],
                            multi=False,
                            value="2015",
                            style={'color':'black'}
                        ),
                        dcc.Dropdown(id="age",
                            options=[
                                {"label": "18-21", "value": "18-21"},
                                {"label": "22-29", "value": "22-29"},
                                {"label": "30-39", "value": "30-39"},
                                {"label": "40-49", "value": "40-49"},
                                {"label": "50-59", "value": "50-59"},
                                {"label": "60+", "value": "60+"},
                            ],
                            multi=False,
                            value="18-21",
                            style={'color':'black'}
                        )
                    ],
                    className='bg-dark text-white'
                    ),
                dbc.Col(
                    [
                        html.H2('Gender Pay Bar Chart'),
                        dcc.Graph(
                            id="gender_bar",
                            figure = {}
                        )
                    ],
                    className='bg-white'
                    )
            ],
            style={"height": "60vh"}),
            dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('UK average house prices vs average annual salary'),
                        dcc.Graph(
                            figure = house_salary_fig
                        )
                        ],
                    className='bg-white'
                    ),
                dbc.Col(
                    [
                        html.H2('All UK countries average house prices'),
                        dcc.Graph(
                            figure = uk_house_fig
                        )
                    ],
                    className='bg-dark text-white'
                    )
            ],
            style={"height": "60vh"}),
            dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('Empty Homes and Second Homes in Scotland'),
                        dcc.Graph(
                            figure = second_homes_fig
                        ),
                        ],
                        className='bg-dark text-white'
                    ),
                dbc.Col(
                    [
                        html.H2('Empty Homes and Second Homes Vs House Prices in Scotland'),
                        dcc.Graph(
                            figure = second_homes_prices_fig
                        )
                    ],
                    className='bg-white'
                    )
            ],
            style={"height": "60vh"})
        
        
        
])

@app.callback(
    [Output(component_id="gender_pie", component_property="figure"),
     Output(component_id="gender_bar", component_property="figure")],
    [Input(component_id="year", component_property="value"), 
     Input(component_id="age", component_property="value")]
)
def update_graphs(year_input, age_input):
    # print(year_input)
    # print(age_input)
    df = gender_pay_dfs[year_input].copy()
    df_age = df.loc[df["age"].str.contains(age_input)]
    fig1 = px.pie(df_age, names="gender", values="mean")
    fig2 = px.bar(df, x="age", color="gender", y = "mean", barmode='group',)

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)

