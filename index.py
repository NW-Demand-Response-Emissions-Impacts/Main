"""
index.py

Sets up the two-page dashboard layout. See Dashboard Generator package to edit the pages.
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from emissions_calculator.phase2_dashboard_generator import home, more_info


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[
            html.Img(src=app.get_asset_url('dr_logo.png'),style={'height':'12%',
            'width':'12%','display': 'inline-block','verticalAlign': 'top'}),
            dcc.Link('Home', href='/home', style={'font-size':'20px',
            'display': 'inline-block','verticalAlign': 'top',
            'text-decoration':'underline', "margin-left": "10px"}),
            dcc.Link('More Information', href='/more_info', style={'font-size':'20px',
            'display': 'inline-block','verticalAlign': 'top',"margin-left": "10px",
            'text-decoration':'underline'})
            ]),
    html.H1('Emissions Impacts of Demand Response Programs',style={"textAlign":
            "center","margin-top":"20px"}),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    Displays webpage based on user input.

    Args:
        pathname: user-selected webpage path
    Returns:
        HTML layout based on user input
    """
    if pathname == '/home':
        webpage = home.layout
    elif pathname == '/more_info':
        webpage = more_info.layout
    else:
        webpage = "404 Page Error! Please choose a link"

    return webpage

if __name__ == '__main__':
    app.run_server()
