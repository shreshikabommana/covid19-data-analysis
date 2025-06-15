#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash


# In[2]:


DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

covid = pd.read_csv(f"{DATA_DIR}/covid.csv")
grouped = pd.read_csv(f"{DATA_DIR}/covid_grouped.csv")
deaths = pd.read_csv(f"{DATA_DIR}/coviddeath.csv")


# In[3]:


# Filter for USA and preprocess
usa_grouped = grouped[grouped["Country/Region"] == "US"].copy()
usa_grouped["Date"] = pd.to_datetime(usa_grouped["Date"])
usa_grouped.sort_values("Date", inplace=True)


# In[4]:


# Moving averages (7-day)
usa_grouped["Cases_7d_avg"] = usa_grouped["Confirmed"].diff().rolling(window=7).mean()
usa_grouped["Deaths_7d_avg"] = usa_grouped["Deaths"].diff().rolling(window=7).mean()


# In[5]:


# Total cases & deaths over time
fig1 = px.line(usa_grouped, x="Date", y="Confirmed", title="Total Confirmed Cases in USA")
fig1.write_html(f"{OUTPUT_DIR}/usa_total_cases.html")

fig2 = px.line(usa_grouped, x="Date", y="Deaths", title="Total Deaths in USA")
fig2.write_html(f"{OUTPUT_DIR}/usa_total_deaths.html")


# In[6]:


# Moving average plot
plt.figure(figsize=(12,6))
plt.plot(usa_grouped["Date"], usa_grouped["Cases_7d_avg"], label="7-Day Avg Cases")
plt.plot(usa_grouped["Date"], usa_grouped["Deaths_7d_avg"], label="7-Day Avg Deaths")
plt.title("COVID-19 USA: 7-Day Moving Averages")
plt.xlabel("Date")
plt.ylabel("Cases / Deaths")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/moving_averages.png")
plt.close()


# In[7]:


# Case-to-Death ratio over time
usa_grouped["Death_to_case_ratio"] = (
    usa_grouped["Deaths"] / usa_grouped["Confirmed"]
).replace([float("inf"), -float("inf")], pd.NA).fillna(0)

plt.figure(figsize=(10,5))
sns.lineplot(data=usa_grouped, x="Date", y="Death_to_case_ratio")
plt.title("Death-to-Case Ratio Over Time (USA)")
plt.ylabel("Ratio")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/death_to_case_ratio.png")
plt.close()


# In[8]:


# Interactive Time Slider for Cases & Deaths
usa_grouped["Date"] = pd.to_datetime(usa_grouped["Date"])

usa_monthly = usa_grouped.resample("M", on="Date").sum().reset_index()

fig_slider = px.line(
    usa_monthly,
    x="Date",
    y=["Confirmed", "Deaths"],
    title="COVID-19 Cases & Deaths Over Time (USA)",
    labels={"value": "Count", "variable": "Metric"},
)

fig_slider.update_layout(
    xaxis=dict(title="Date", tickformat="%b %Y"),
    yaxis=dict(title="Count"),
)
fig_slider.write_html(f"{OUTPUT_DIR}/cases_deaths_over_time.html")


# In[9]:


# Dual-Axis Cases vs. Deaths Plot
fig, ax1 = plt.subplots(figsize=(12,6))

# First Y-axis for Cases
ax1.set_xlabel("Date")
ax1.set_ylabel("7-Day Avg Cases", color="blue")
ax1.plot(usa_grouped["Date"], usa_grouped["Cases_7d_avg"], color="blue", label="7-Day Avg Cases")
ax1.tick_params(axis="y", labelcolor="blue")

# Second Y-axis for Deaths
ax2 = ax1.twinx()
ax2.set_ylabel("7-Day Avg Deaths", color="red")
ax2.plot(usa_grouped["Date"], usa_grouped["Deaths_7d_avg"], color="red", linestyle="dashed", label="7-Day Avg Deaths")
ax2.tick_params(axis="y", labelcolor="red")

fig.tight_layout()
plt.title("Comparison of Cases vs. Deaths in USA (7-Day Moving Avg)")
plt.savefig(f"{OUTPUT_DIR}/cases_vs_deaths.png")
plt.close()


# ### Mortality by Comorbidity and Age Range Dashboard: Bar Plot by State

# In[15]:


conditions = ['Influenza and pneumonia', 'Chronic lower respiratory diseases',
              'Adult respiratory distress syndrome', 'Respiratory failure',
              'Respiratory arrest', 'Other diseases of the respiratory system',
              'Hypertensive diseases', 'Ischemic heart disease', 'Cardiac arrest',
              'Cardiac arrhythmia', 'Heart failure', 'Cerebrovascular diseases',
              'Other diseases of the circulatory system', 'Sepsis', 'Malignant neoplasms',
              'Diabetes', 'Obesity', 'Alzheimer disease', 'Vascular and unspecified dementia',
              'Renal failure', 'Intentional and unintentional injury, poisoning, and other adverse events',
              'All other conditions and causes (residual)', 'COVID-19']

condition_groups = ['Respiratory diseases', 'Circulatory diseases', 'Sepsis', 'Malignant neoplasms', 'Diabetes',
                    'Obesity', 'Alzheimer disease', 'Vascular and unspecified dementia', 'Renal failure',
                    'Intentional and unintentional injury, poisoning and other adverse events',
                    'All other conditions and causes (residual)', 'Coronavirus Disease 2019']

app1 = JupyterDash(__name__)

age_range_dropdown = dcc.Dropdown(
    id='age-range-dropdown',
    options=[
        {'label': '0-24', 'value': '0-24'},
        {'label': '25-34', 'value': '25-34'},
        {'label': '35-44', 'value': '35-44'},
        {'label': '45-54', 'value': '45-54'},
        {'label': '55-64', 'value': '55-64'},
        {'label': '65-74', 'value': '65-74'},
        {'label': '75-84', 'value': '75-84'},
        {'label': '85+', 'value': '85+'},
        {'label': 'Not stated', 'value': 'Not stated'},
        {'label': 'All ages', 'value': 'All ages'}
    ],
    value='All ages',
)

condition_dropdown = dcc.Dropdown(
    id='condition-dropdown',
    options=[{'label': condition, 'value': condition} for condition in conditions],
    value=conditions[0],
)

app1.layout = html.Div([
    html.H3("Select Age Range and Condition"),
    age_range_dropdown,
    condition_dropdown,
    html.Div(id='display-output', children="Results will be shown here."),
    dcc.Graph(id='condition-visualization')
])

# Callback to update based on selections
@app1.callback(
    [Output('display-output', 'children'),
     Output('condition-visualization', 'figure')],
    [Input('age-range-dropdown', 'value'),
     Input('condition-dropdown', 'value')]
)
def update_output(age_range, condition):
    filtered_data = deaths[(deaths['Age Group'] == age_range) & (deaths['Condition'] == condition)]
    
    output_text = f"Age Range: {age_range}, Condition: {condition}, " \
                  f"Number of Cases: {len(filtered_data)}"

    fig = px.bar(filtered_data,
                 x='State',
                 y='Number of COVID-19 Deaths',
                 title=f"COVID-19 Deaths by State for {condition} in Age Range: {age_range}",
                 labels={"Number of COVID-19 Deaths": "Deaths", "State": "State"})

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Number of Deaths",
        showlegend=False
    )

    return output_text, fig

# if __name__ == '__main__':
#     app1.run_server(debug=True, port=8050)

app = app1


# ### Dynamic Time Series Dashboard: Tracking State-Specific Trends Over Time

# In[16]:


app2 = JupyterDash(__name__)

# Dropdown for age range
age_range_dropdown = dcc.Dropdown(
    id='age-range-dropdown',
    options=[
        {'label': '0-24', 'value': '0-24'},
        {'label': '25-34', 'value': '25-34'},
        {'label': '35-44', 'value': '35-44'},
        {'label': '45-54', 'value': '45-54'},
        {'label': '55-64', 'value': '55-64'},
        {'label': '65-74', 'value': '65-74'},
        {'label': '75-84', 'value': '75-84'},
        {'label': '85+', 'value': '85+'},
        {'label': 'Not stated', 'value': 'Not stated'},
        {'label': 'All ages', 'value': 'All ages'}
    ],
    value='All ages',
)

app2.layout = html.Div([
    age_range_dropdown,
    dcc.Graph(id='usa-map'),
])

# Callback to update the map based on age range
@app2.callback(
    Output('usa-map', 'figure'),
    [Input('age-range-dropdown', 'value')]
)
def update_usa_map(selected_age_range):
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
        scope="usa",
        range_color=[filtered_data["Number of COVID-19 Deaths"].min(),
                     filtered_data["Number of COVID-19 Deaths"].max() * 0.025],
    )
    return fig_map

if __name__ == '__main__':
    app2.run_server(debug=True, port=8051)


# In[ ]:





# In[ ]:




