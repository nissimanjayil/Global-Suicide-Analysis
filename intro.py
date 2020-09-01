import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


df = pd.read_csv('master.csv')
sr = df.groupby(by=['year']).agg({'suicides_no': ["sum"]})
sr.columns = ['total_suicide']

sr_gender = df.groupby(by=['sex']).agg({'suicides_no': ["sum"]})
sr_gender.columns = ['total_suicide']
sr_gender.reset_index(inplace=True)


sr_age = df.groupby(by=['age']).agg({'suicides_no': ['sum']})
sr_age.columns = ['total_suicides']

cr_total = df.groupby(by=['country']).agg({'suicides_no': ['sum']})
cr_total.columns = ['total_suicide']
cr_total = cr_total.sort_values(by=['total_suicide'], ascending=False).head(10)

cr_map = df.groupby(by=['country']).agg({"suicides_no": ['sum']})
cr_map.columns = ['total_suicide']
cr_map.reset_index(inplace=True)

cr_gender = df.groupby(by=['country', 'sex']).agg({'suicides_no': ['sum']})
cr_gender.columns = ['total_suicide']
cr_gender.reset_index(inplace=True)
cr_gender = cr_gender.sort_values(
    by=['total_suicide'], ascending=False).head(10)

data_pop = df.groupby(by=['age', 'sex']).agg({'population': ['sum']})
data_pop.columns = ['population']
data_pop.reset_index(inplace=True)

gdp_country = df.groupby(by=['country']).agg(
    {"gdp_per_capita ($)": ['mean'], "suicides_no": ['mean']})

gdp_country = df.groupby(by=['country', 'year', 'sex', 'gdp_per_capita ($)']).agg(
    {"suicides_no": ['sum']})
gdp_country.columns = ["total_suicide"]
gdp_country.reset_index(inplace=True)


gdp_year = df.groupby(by=['year']).agg(
    {"gdp_per_capita ($)": ['mean'], "suicides_no": ['mean']})
gdp_year.columns = ["gdp_per_capita", "total_suicide"]


gdp_gender = df.groupby(by=['country', 'sex', 'gdp_per_capita ($)']).agg(
    {"suicides_no": ['sum']})
gdp_gender.columns = ["total_suicide"]
gdp_gender.reset_index(inplace=True)

app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([


    html.Div([

        html.Br(),
        html.H1('Global suicide analysis 1985 - 2016'),
        html.Div(id='output_data'),
        html.Br(),

        dcc.Dropdown(id='my_dropdown',
                     options=[
                         {'label': 'World wide suicide',
                             'value': 'World wide suicide'},
                         {'label': 'Country wise suicide',
                          'value': 'Country wise suicide'},
                         {'label': 'GDP wise suicide', 'value': 'GDP wise suicide'}
                     ],
                     optionHeight=35,  # height/space between dropdown options
                     # dropdown value selected automatically when page loads
                     value='GDP wise suicide',
                     disabled=False,  # disable dropdown value selection
                     multi=False,  # allow multiple dropdown values to be selected
                     searchable=True,  # allow user-searching of dropdown values
                     search_value='',  # remembers the value searched in dropdown
                     # gray, default text shown when no option is selected
                     placeholder='Please select...',
                     clearable=True,  # allow user to removes the selected value
                     # use dictionary to define CSS styles of your dropdown
                     style={'width': "100%"},
                     # className='select_box',           #activate separate CSS document in assets folder
                     # persistence=True,                 #remembers dropdown value. Used with persistence_type
                     # persistence_type='memory'         #remembers dropdown value selected until...
                     ),  # 'memory': browser tab is refreshed
        # 'session': browser tab is closed
        # 'local': browser cookies are deleted
    ], className='three columns'),

    html.Div(
        id="container",
    ),
    html.Div([
        dcc.Graph(id='our_graph', figure={}),
        dcc.Graph(id="gender"),
        dcc.Graph(id="age")
    ]),



])

# ---------------------------------------------------------------
# Connecting the Dropdown values to the graph


@app.callback(
    [Output(component_id='our_graph', component_property='figure'),
     Output(component_id="gender", component_property='figure'),
     Output(component_id="age", component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value')]
)
def build_graph(column_chosen):
    #global fig, fig2, fig3
    if column_chosen == 'World wide suicide':

        fig = px.bar(sr, title="Worldwide suicide by year")
        fig2 = px.pie(sr_gender, values='total_suicide',
                      names='sex', title="World wide suicide by Gender ")
        fig3 = px.bar(sr_age, title="World wide suicide by age",
                      color_discrete_sequence=['green']*3)
        return fig, fig2, fig3
    elif column_chosen == "Country wise suicide":
        fig = px.bar(cr_total, title="Top 10 Countries with the highest suicide rates",
                     orientation='h')
        fig2 = px.choropleth(cr_map, locations="country", locationmode='country names',
                             color="total_suicide",  # lifeExp is a column of gapminder
                             hover_name="country",  # column to add to hover information
                             color_continuous_scale=px.colors.sequential.Plasma, title="Map with total suicides in Different Countries")
        fig3 = px.pie(data_pop, values='population',
                      names='age', title="Population by age 1985-2015")
        return fig, fig2, fig3
    elif column_chosen == 'GDP wise suicide':
        fig = px.line_3d(gdp_country, y='gdp_per_capita ($)',
                         x='total_suicide', z='year', color='country', title="GDP wise suicide 1985 - 2015")
        fig2 = px.bar(
            gdp_year, title="GDP wise suicide:Correlation between suicide and GDP according to each year")
        fig3 = px.pie(gdp_gender, values='total_suicide', names='country',
                      title="GDP wise suicide by countries 1985 -2016")
        return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
