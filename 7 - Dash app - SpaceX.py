# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:/Users/Wooc Do/Desktop/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                value = "All",
                                style={'textAlign': 'center', 'color': '#503D36','font-size':20, "padding":5 },
                                options=[
                                        {'label': 'All Site', 'value': 'All'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                                placeholder='Select launch site here',
                                searchable = True,                              
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id="success-pie-chart")),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id="payload-slider",
                                min=0, max = 10000, step = 1000,
                                marks={ 0:"0",2500:"2500",5000:"5000",7500:"7500",10000:"10000"},
                                value=[min_payload,max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value"))
def get_pie_chart(entered_site):
    filter_data1  = spacex_df[["Launch Site", "class"]]
    filter_data11 = filter_data1[filter_data1["class"] == 1]
    data_pie = filter_data11.groupby("Launch Site")["class"].sum().reset_index()    
    if entered_site == "All":
        fig = px.pie(  data_pie, values = "class", names ="Launch Site", title="Successful launch by site")
        return fig
    else:
        data_filter12 = filter_data1[filter_data1["Launch Site"] == entered_site]
        data_pie_filter = data_filter12.value_counts().reset_index()
        fig = px.pie(data_pie_filter, names = {0: "Fail", 1:"Success"}, values = "count", title= f"The Percentage of Successful Launch of Site {entered_site}")
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"),
             ([Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]))

def get_scatter_chart(selected_site,selected_value):
    data2 = spacex_df[["Launch Site", "Payload Mass (kg)","Booster Version Category", "class"]]
    data21 = data2[data2["Payload Mass (kg)"] > selected_value[0]]
    data22 = data21[data21["Payload Mass (kg)"] < selected_value[1]]
    if selected_site == "All":
        fig = px.scatter(data22, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        data23 = data22[data22["Launch Site"] == selected_site]
        fig = px.scatter(data23, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig












# Run the app
if __name__ == '__main__':
    app.run_server()
