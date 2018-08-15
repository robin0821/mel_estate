from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Launch the dash app!
app = dash.Dash()
app.title = 'Melbourne Residential Property Market Dashboard...'
server = app.server

# External CSS
external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

for css in external_css:
    app.css.append_css({'external_url': css})

external_js = ["http://code.jquery.com/jquery-3.3.1.min.js",
               "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"]

# External js
for js in external_js:
    app.scripts.append_script({"external_url": js})

# Read in the initial dataset for visualisation...
df = pd.read_csv('./mel_estate.csv')

# Design the layout of app!
app.layout = html.Div([
                html.Div([
                    html.Br([]),
                    html.Div([
                        html.H5('Interactive Dashboard Demo: Melbourne Resendential Property Market Snapshot...'),
                    ], style={'color': 'rgb(255, 153, 0)', 'font': 'Verdana'}),
                    html.Div([
                        html.Br([]),
                    ], className='gs-header'),
                    html.Div([
                        html.Div([
                            html.Label(id='agency-label', children='Agencies', style={'color':'white'}),
                            dcc.Dropdown(id='agencies',
                                        options=[{'label': i, 'value': i} for i in df['Agency'].unique()],
                                        multi=True,
                                        value=['Barry Plant', 'Ray White', 'Harcourts'],
                                        placeholder='Filter by agencies...'),
                                ], className='col-lg-4 col-md-4 col-sm-6 col-xs-12'),
                        html.Div([
                            html.Label(id='locality-label', children='Localities', style={'color':'white'}),
                            dcc.Dropdown(id='localities',
                                        options=[{'label': i, 'value': i} for i in df['Locality'].unique()],
                                        multi=True,
                                        value=['Pakenham', 'Mornington', 'Berwick'],
                                        placeholder='Filter by localities...')
                                ], className='col-lg-4 col-md-4 col-sm-6 col-xs-12'),
                        html.Div([
                            html.Label(id='property-type-label', children='Property Types', style={'color':'white'}),
                            dcc.Dropdown(id='property-types',
                                        options=[{'label': i, 'value': i} for i in df['PropertyType'].unique()],
                                        multi=True,
                                        value=['house', 'unit', 'townhouse'],
                                        placeholder='Filter by property types...')
                                ], className='col-lg-4 col-md-4 col-sm-6 col-xs-12'),
                            ], className='row padded'),
                    html.Br([]),

                    html.Div([
                        html.Label(id='date-range', children='Date Range', className='col-lg-6 col-md-6 col-sm-12 col-xs-12', style={'color':'white'}),
                        html.Label(id='price-from', children='Price From:', className='col-lg-3 col-md-3 col-sm-6', style={'color':'white'}),
                        html.Label(id='price-to', children='Price To:', className='col-lg-3 col-md-3 col-sm-6', style={'color':'white'})
                    ], className='row'),

                    html.Div([
                        html.Div([
                            dcc.DatePickerRange(
                                id='sold-date-range',
                                min_date_allowed=dt(2010, 1, 1),
                                max_date_allowed=dt.now().date(),
                                initial_visible_month=dt(2016,1,1),
                                start_date=dt(2010,1,1),
                                end_date=dt.now().date(),
                            )
                        ], className='col-lg-6 col-md-6 col-sm-12 col-xs-12'),
                        html.Div([
                            dcc.Dropdown(
                                id='select-price-from',
                                options=[{'label':'>10k', 'value':10000 },
                                        {'label':'>100k', 'value':100000},
                                        {'label':'>250k', 'value':250000},
                                        {'label':'>500k', 'value':500000},
                                        {'label':'>1m', 'value':1000000},
                                        {'label':'>5m', 'value':5000000},],
                                value=10000
                            )
                        ], className='col-lg-3 col-md-3 col-sm-6 col-xs-6'),

                        html.Div([
                            dcc.Dropdown(
                                id='select-price-to',
                                options=[{'label':'<=100k', 'value':100000},
                                        {'label':'<=250k', 'value':250000},
                                        {'label':'<=500k', 'value':500000},
                                        {'label':'<=1m', 'value':1000000},
                                        {'label':'<=5m', 'value':5000000},
                                        {'label':'>5m', 'value':10000000}],
                                value=1000000
                            )
                        ], className='col-lg-3 col-md-3 col-sm-6 col-xs-6')
                    ], className='row'),

                    html.Br([]),
                    # Insert Scatter and Box plot...
                    html.Div([
                        html.Div( #Insert Scatter plot...
                            dcc.Graph(id='scatter-plot'),
                            className='col-lg-12 col-md-12 col-sm-12 col-xs-12'),
                        html.Br([]),
                        html.Div( #Insert Box plot...
                            dcc.Graph(id='box-plot'),
                            className='col-lg-12 col-md-12 col-sm-12 col-xs-12'),


                    ]),
                    html.Br([]),
                    #Insert map plot...
                    html.Div([
                        dcc.Graph(id='map-plot',
                                  animate=True)
                    ]),
                    html.Div([
                        html.H6('About DataRaft'),
                        html.P('DataRaft provides services in Customer Strategy and Data Analytics.  Our unique value comes from our domain expertise from experience working in senior strategy and marketing roles for ASX 200 organisations.'),
                        html.Br([])
                    ], style={'color': 'white'})


    ], className='container',style={'backgroundColor':'rgb(64,64,64)', 'fontSize':12})
], style={'backgroundColor': 'rgb(75,75,75)'})

# Function for updating the Scatter Plot...
@app.callback(Output('scatter-plot', 'figure'),
            [Input('agencies', 'value'),
            Input('localities', 'value'),
            Input('property-types', 'value'),
            Input('sold-date-range', 'start_date'),
            Input('sold-date-range', 'end_date'),
            Input('select-price-from', 'value'),
            Input('select-price-to', 'value')])
def update_scatter_plot(agency_names, locality_names,
                    property_tp_names, start_date,
                    end_date, price_from, price_to):

    if not isinstance(agency_names, list):
        agency_names = [agency_names]
    if not isinstance(locality_names, list):
        locality_names = [locality_names]
    if not isinstance(property_tp_names, list):
        property_tp_names = [property_tp_names]

    df_filtered = df[(df['Agency'].isin(agency_names)) &
                     (df['Locality'].isin(locality_names)) &
                     (df['PropertyType'].isin(property_tp_names)) &
                     (df['DateSold'] > start_date) &
                     (df['DateSold'] < end_date) &
                     (df['Price'] > price_from) &
                     (df['Price'] <= price_to)]


    return {'data':[go.Scatter(x=df_filtered[df_filtered['PropertyType']==house_type]['DateSold'],
                        y=df_filtered[df_filtered['PropertyType']==house_type]['Price'],
                        mode='markers',
                        text=df_filtered[df_filtered['PropertyType']==house_type]['StreetAddress'],
                        marker=dict(size=10,
                            opacity=0.7,
                        ),
                        name=house_type,
                        ) for house_type in df['PropertyType'].unique()],
            'layout':go.Layout(
                title = '<b>Property Price trend over the years</b>',
                titlefont=dict(size=16),
                xaxis = dict(title='Time', color='white', gridwidth=0, gridcolor='rgb(75,75,75)'),
                yaxis = dict(title='Proprety Price (in AUD)',color='white', gridwidth=0, gridcolor='rgb(75,75,75)'),
                font = dict(size=10, color='white'),
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgb(64,64,64)',
                plot_bgcolor='rgb(64,64,64)',
                # grid = dict(rows=1, columns=1),
            ),
            }

# Function to update box plot...
@app.callback(Output('box-plot', 'figure'),
            [Input('agencies', 'value'),
            Input('localities', 'value'),
            Input('property-types', 'value'),
            Input('sold-date-range', 'start_date'),
            Input('sold-date-range', 'end_date'),
            Input('select-price-from', 'value'),
            Input('select-price-to', 'value')])
def update_scatter_plot(agency_names, locality_names,
                    property_tp_names, start_date,
                    end_date, price_from, price_to):

    if not isinstance(agency_names, list):
        agency_names = [agency_names]
    if not isinstance(locality_names, list):
        locality_names = [locality_names]
    if not isinstance(property_tp_names, list):
        property_tp_names = [property_tp_names]

    df_filtered = df[(df['Agency'].isin(agency_names)) &
                     (df['Locality'].isin(locality_names)) &
                     (df['PropertyType'].isin(property_tp_names)) &
                     (df['DateSold'] > start_date) &
                     (df['DateSold'] < end_date) &
                     (df['Price'] > price_from) &
                     (df['Price'] <= price_to)]


    return {'data':[go.Box(y=df_filtered[df_filtered['Locality']==suburb]['Price'],
                            name=suburb, opacity=0.8, line=dict(width=1))
                     for suburb in df_filtered['Locality'].unique()],
            'layout': go.Layout(
                title='<b>Property price statistics</b>',
                titlefont=dict(size=16),
                xaxis = dict(title='Suburbs / Geo-location', color='white', gridwidth=0, gridcolor='rgb(75,75,75)'),
                yaxis = dict(title='Proprety Price (in AUD)',color='white', gridwidth=0, gridcolor='rgb(75,75,75)'),
                font = dict(size=10, color='white'),
                margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor='rgb(64,64,64)',
                plot_bgcolor='rgb(64,64,64)',
            )}

# Function for updating the map plot...
@app.callback(Output('map-plot', 'figure'),
            [Input('agencies', 'value'),
            Input('localities', 'value'),
            Input('property-types', 'value'),
            Input('sold-date-range', 'start_date'),
            Input('sold-date-range', 'end_date'),
            Input('select-price-from', 'value'),
            Input('select-price-to', 'value')])
def update_map_plot(agency_names, locality_names,
                    property_tp_names, start_date,
                    end_date, price_from, price_to):

    if not isinstance(agency_names, list):
        agency_names = [agency_names]
    if not isinstance(locality_names, list):
        locality_names = [locality_names]
    if not isinstance(property_tp_names, list):
        property_tp_names = [property_tp_names]


    df_filtered = df[(df['Agency'].isin(agency_names)) &
                     (df['Locality'].isin(locality_names)) &
                     (df['PropertyType'].isin(property_tp_names)) &
                     (df['DateSold'] > start_date) &
                     (df['DateSold'] < end_date) &
                     (df['Price'] > price_from) &
                     (df['Price'] <= price_to)]

    return {'data':[go.Scattermapbox(
                        lat=df_filtered['Latitude'],
                        lon=df_filtered['Longitude'],
                        mode='markers',
                        marker=dict(size=10,
                                    color='orange',
                                    opacity=0.5),
                        text='Address: ' + df_filtered['StreetAddress'] + '<br>' +
                             'Suburb: ' + df_filtered['Locality'] + '<br>' +
                             'Price Sold: ' + (df_filtered['Price']/1000).astype(str) + 'k AUD' #+ '<br>' +
                             # 'Date Sold: ' + df['DateSold'].astype(str)
                             # 'Distance to CBD: ' + df_filtered['cbdDistance'].astype(str) + '<br>' +
                             # 'Closest Primary School: ' + df['1PrimaryName'] + " (" + df['1PrimarySector'] + ") " + " " + df['1PrimaryScore'].astype(str) + ", "  + '<br>' +
                             # 'Closest Secondary School: ' + df['1SecondaryName'] + " (" + df['1SecondarySector'] + ") " + " " + df['1SecondaryScore'].astype(str)
                    )],

            'layout':go.Layout(
                title='<b>Geolocation distribution of properties</b>',
                titlefont=dict(size=16),
                autosize=True,
                height=768,
                # width=1024,
                hovermode='closest',
                mapbox=dict(
                    accesstoken='pk.eyJ1IjoiZGF0YXJhZnQiLCJhIjoiY2prOGJsMzBzMTgzYzNxcW9rMW5mZXMwayJ9.iaClqwde2Jm55-TCAw_38g',
                    bearing=0,
                    pitch=0,
                    zoom=8,
                    style='mapbox://styles/dataraft/cjk8dxpvs51ax2so27sjoeg1f',
                    center=dict(lat=-37.8, lon=144.96),
                ),
                margin=dict(l=20, r=20, t=40, b=40),
                paper_bgcolor='rgb(64,64,64)',
                plot_bgcolor='rgb(64,64,64)',
                font = dict(size=10, color='white'),
            )}




if __name__ == '__main__':
    app.run_server()
