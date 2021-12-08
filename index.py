import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from emissions_calculator.phase2_dashboard_generator import home, more_info
from app import app
from app import server
from dash.dependencies import Input, Output


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home Page', href='/home')],className='row'),
    html.Div([
        dcc.Link('More Information', href='/more_info')],className='row'),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    if pathname == '/more_info':
        return more_info.layout
    else:
        return "404 Page Error! Please choose a link"

if __name__ == '__main__':
    app.run_server()
