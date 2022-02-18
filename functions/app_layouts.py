#---------------------------------------------------------------------------------
# Import Libraries
#---------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.io as pio

# Define Layout Functions
#---------------------------------------------------------------------------------
# Layout 1
#---------------------------------------------------------------------------------
def pe_8_grid_3cols_layout(module_title, df, dropdown_filter_property, dropdown_filter_property2,
                           range_filter_property, checkbox_filter_property,
                          stylesheet = [dbc.themes.SUPERHERO] , plotly_template = 'plotly_dark', plot_bg_color = 'rgba(0,0,0,0.3)',
                          div_bg_color = 'rgba(0,0,0,0)',
                          background_image = None
                          ):
    '''
    Function which takes module name as an input and generates an 8 grid layout of dash web app
    spread across three columns. The 1st column has two rows, the 2nd and 3rd each have 3 rows.

    INPUTS:
    module_title = name of the module

    df = dataframe datatable to be used

    dropdown_filter_property = property to be used as drop down filter (categorical)

    dropdown_filter_property2 = 2nd drop down property to be used as drop down filter (categorical)

    range_filter_property = property to be used as range filter (integer)

    checkbox_filter_property = property to be used as checkbox filter (categorical)

    stylesheet = CSS stylesheet to be used for dash app. Could be local file or from the list of availalble
    Bootswatch themes which could be accessed through dash_bootstrap_components.themes module. The following list
    contains the available themes
    [ CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA,
      MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI]

    plotly_template = plotly template to use for plots (default  = plotly_dark). Available templates:
    ['ggplot2', 'seaborn', 'simple_white', 'plotly','plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
    'ygridoff', 'gridon', 'none']

    plot_bg_color = customized color for background and page of plots (default = 'rgba(0,0,0,0.6)')

    div_bg_color = customized color for each div on the page (default = 'rgba(0,0,0,0)')

    background_image = Image path to be used in the background if provided, ensure the path is provided
    in the following format 'url("REPLACE THIS PART WITH ACTUAL IMAGE PATH")'
    '''

    #---------------------------------------------------------------------------------
    # Set default plotly theme for plotting
    #---------------------------------------------------------------------------------
    pio.templates["custom"] = pio.templates[plotly_template]

    #--------------------------------------------------------------------------------------------------------
    # Further Customize plotly theme for plotting by adjusting grid line colors, background and paper color
    #--------------------------------------------------------------------------------------------------------
    # Adjust the grid line and zero grid line colors
    pio.templates["custom"]['layout']['xaxis']['gridcolor'] = '#666666'
    pio.templates["custom"]['layout']['yaxis']['gridcolor'] = '#666666'
    pio.templates["custom"]['layout']['xaxis']['zerolinecolor'] = '#666666'
    pio.templates["custom"]['layout']['yaxis']['zerolinecolor'] = '#666666'

    # Set background of the plot and paper
    pio.templates["custom"]['layout']['paper_bgcolor'] = plot_bg_color
    pio.templates["custom"]['layout']['plot_bgcolor'] = plot_bg_color

    #---------------------------------------------------------------------------------
    # Initialize dash app
    #---------------------------------------------------------------------------------
    app = dash.Dash(external_stylesheets=stylesheet, title=module_title)

    #---------------------------------------------------------------------------------
    # Customize navigation bar
    #---------------------------------------------------------------------------------
    # INPUT: links in href, and specify Module names
    ##################################################################################
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(module_title, href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More Modules", header=True),
                    dbc.DropdownMenuItem("Module 2", href="#"),
                    dbc.DropdownMenuItem("Module 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Webscraping Project : Waqas A. Khan",
        brand_href="https://github.com/Waqas-K",
        color='teal',
        dark=True,
        fluid=True,
        brand_style={'fontSize': '40px'},
        style={'fontSize': '20px'}
    )

    #---------------------------------------------------------------------------------
    # Customize controls panel
    #---------------------------------------------------------------------------------
    dropdown_filter = df[dropdown_filter_property].unique()
    dropdown_filter2 = df[dropdown_filter_property2].unique()
    range_filter = df[range_filter_property].unique()
    checkbox_filter = df[checkbox_filter_property].unique()

    controls = dbc.FormGroup(
        [
            html.P(dropdown_filter_property, style={'textAlign': 'center', 'color':'cyan'}),
            dcc.Dropdown(
                id='dropdown_id',
                options=[{'label': i, 'value': i} for i in dropdown_filter],
                value=dropdown_filter,  # default value
                multi=True,
                style = {'color' : 'black'}),
            html.Br(),
            html.P(range_filter_property, style={'textAlign': 'center', 'color':'cyan'}),
            dcc.RangeSlider(
                id = 'range_id',
                min = range_filter.min(),
                max = range_filter.max(),
                value = [range_filter.min(),range_filter.max()],
                marks = {str(i):str(i) for i in np.arange(0, 10000000, 2000000)},
                step=100000),
            html.Br(),
            html.P(checkbox_filter_property, style={'textAlign': 'center', 'color':'cyan'}),
            dbc.Card([dbc.Checklist(
                id='checkbox_id',
                options=[{'label': i, 'value': i} for i in checkbox_filter],
                value=checkbox_filter,
                inline=True)
                     ]),
            html.Br(),
            html.P(dropdown_filter_property2, style={'textAlign': 'center', 'color':'cyan'}),
            dcc.Dropdown(
                id='dropdown_id2',
                options=[{'label': i, 'value': i} for i in dropdown_filter2],
                value=dropdown_filter2,  # default value
                multi=True,
                style = {'color' : 'black'}),
            html.Br(),
        ])

    #---------------------------------------------------------------------------------
    # Initialize plot windows
    #---------------------------------------------------------------------------------
    # Specify number of plots to be used, initialize them with unique 'id', set their
    # style such as height based on the grid layout of the app. The hoverData property
    # is also initialized for plots through which interactions and cross-filtering could
    # be performed if needed through @app.callbacks, Therefore set the customdata property
    # to be used for cross-filtering through {'points': [{'customdata': '###'}]}
    ####################################################################################
    plot1 = dcc.Graph(id='fig1', hoverData={'points': [{'customdata': dropdown_filter}]} ,style={'height': '68vh'})
    plot2 = dcc.Graph(id='fig2',style={'height': '33vh'})
    plot3 = dcc.Graph(id='fig3',style={'height': '33vh'})
    plot4 = dcc.Graph(id='fig4',style={'height': '33vh'})
    plot5 = dcc.Graph(id='fig5',style={'height': '33vh'})
    plot6 = dcc.Graph(id='fig6',style={'height': '33vh'})
    plot7 = dcc.Graph(id='fig7',style={'height': '33vh'})


    #---------------------------------------------------------------------------------
    # Customize Overall page layout and window sizes
    #---------------------------------------------------------------------------------
    # Create the overall grid layout of the page using Col/Row Containers
    # and specify the size and style for each Col/Row asn well as the entire Container.
    # Then merge all the containers and navbar etc. to create an overall layout of the page
    ####################################################################################
    col1 = dbc.Col(html.Div([
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot1), style={'margin-left': '2%','height': '68vh'}, className= div_bg_color), width=12)]),
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(controls), style={'margin-left': '2%','height': '33vh'}, className=div_bg_color), width=12)]),
                      html.Br()
                      ]),width=4)
    col2 = dbc.Col(html.Div([
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot2), style={'height': '33vh'}, className=div_bg_color), width=12)]),
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot3), style={'height': '33vh'}, className= div_bg_color), width=12)]),
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot4), style={'height': '33vh'}, className=div_bg_color), width=12)]),
                      html.Br()
                      ]),width=4)
    col3 = dbc.Col(html.Div([
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot5), style={'margin-right': '2%','height': '33vh'}, className=div_bg_color), width=12)]),
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot6), style={'margin-right': '2%','height': '33vh'}, className= div_bg_color), width=12)]),
                      html.Br(),
                      dbc.Row([dbc.Col(html.Div(html.B(plot7), style={'margin-right': '2%','height': '33vh'}, className=div_bg_color), width=12)]),
                     html.Br()
                      ]),width=4)


    page_layout = dbc.Row([col1,col2,col3])

    #---------------------------------------------------------------------------------
    # Create the overall app layout
    #---------------------------------------------------------------------------------
    if background_image:
        app.layout =  html.Div(style={'background-image' : background_image,
                              'background-size' : 'cover'},
                               children = [html.Div([navbar]),html.Div([page_layout])])
    else:
        app.layout = html.Div([html.Div([navbar]),html.Div([page_layout])])


    return  app
