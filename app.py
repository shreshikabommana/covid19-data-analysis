import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load your data
DATA_DIR = "data"
deaths = pd.read_csv(f"{DATA_DIR}/coviddeath.csv")

# Define condition list (same as your notebook)
conditions = [
    'Influenza and pneumonia', 'Chronic lower respiratory diseases',
    'Adult respiratory distress syndrome', 'Respiratory failure',
    'Respiratory arrest', 'Other diseases of the respiratory system',
    'Hypertensive diseases', 'Ischemic heart disease', 'Cardiac arrest',
    'Cardiac arrhythmia', 'Heart failure', 'Cerebrovascular diseases',
    'Other diseases of the circulatory system', 'Sepsis', 'Malignant neoplasms',
    'Diabetes', 'Obesity', 'Alzheimer disease', 'Vascular and unspecified dementia',
    'Renal failure', 'Intentional and unintentional injury, poisoning, and other adverse events',
    'All other conditions and causes (residual)', 'COVID-19'
]

# Initialize Dash app
app = Dash(__name__)
server = app.server  # for WSGI deployment

# Layout with tabs for your two dashboards
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Mortality by Comorbidity', value='tab-1'),
        dcc.Tab(label='Dynamic Time Series', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

# Layout for Tab 1 (Mortality by Comorbidity)
def layout_tab1():
    return html.Div([
        html.H3("Select Age Range and Condition"),
        dcc.Dropdown(
            id='age-range-dropdown-1',
            options=[{'label': a, 'value': a} for a in [
                '0-24', '25-34', '35-44', '45-54',
                '55-64', '65-74', '75-84', '85+',
                'Not stated', 'All ages'
            ]],
            value='All ages',
            clearable=False,
        ),
        dcc.Dropdown(
            id='condition-dropdown',
            options=[{'label': c, 'value': c} for c in conditions],
            value=conditions[0],
            clearable=False,
        ),
        html.Div(id='display-output'),
        dcc.Graph(id='condition-visualization')
    ])

# Layout for Tab 2 (Dynamic Time Series)
def layout_tab2():
    return html.Div([
        html.H3("Dynamic Time Series Dashboard"),
        dcc.Dropdown(
            id='age-range-dropdown-2',
            options=[{'label': a, 'value': a} for a in [
                '0-24', '25-34', '35-44', '45-54',
                '55-64', '65-74', '75-84', '85+',
                'Not stated', 'All ages'
            ]],
            value='All ages',
            clearable=False,
        ),
        dcc.Graph(id='usa-map')
    ])

# Callback to switch tabs
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'tab-1':
        return layout_tab1()
    elif tab == 'tab-2':
        return layout_tab2()

# Callback for Tab 1 interactivity
@app.callback(
    [Output('display-output', 'children'),
     Output('condition-visualization', 'figure')],
    [Input('age-range-dropdown-1', 'value'),
     Input('condition-dropdown', 'value')]
)
def update_mortality_dashboard(age_range, condition):
    filtered_data = deaths[
        ((deaths['Age Group'] == age_range) | (age_range == 'All ages')) &
        (deaths['Condition'] == condition)
    ]
    output_text = f"Age Range: {age_range}, Condition: {condition}, Number of Cases: {len(filtered_data)}"
    fig = px.bar(
        filtered_data,
        x='State',
        y='Number of COVID-19 Deaths',
        title=f"COVID-19 Deaths by State for {condition} in Age Range: {age_range}",
        labels={"Number of COVID-19 Deaths": "Deaths", "State": "State"}
    )
    fig.update_layout(xaxis_title="State", yaxis_title="Number of Deaths", showlegend=False)
    return output_text, fig

# Callback for Tab 2 interactivity
@app.callback(
    Output('usa-map', 'figure'),
    Input('age-range-dropdown-2', 'value')
)
def update_time_series_dashboard(selected_age_range):
    if selected_age_range == 'All ages':
        filtered_data = deaths.groupby("State")["Number of COVID-19 Deaths"].sum().reset_index()
    else:
        filtered_data = deaths[deaths['Age Group'] == selected_age_range].groupby("State")["Number of COVID-19 Deaths"].sum().reset_index()
    fig_map = px.choropleth(
        filtered_data,
        locations="State",
        locationmode="USA-states",
        color="Number of COVID-19 Deaths",
        color_continuous_scale="Greys",
        title=f"Total COVID-19 Deaths per State - Age Group: {selected_age_range}",
        scope="usa"
    )
    return fig_map

if __name__ == '__main__':
    app.run_server(debug=True)
