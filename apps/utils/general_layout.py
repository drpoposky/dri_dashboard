from dash import html
from app import app
import dash_bootstrap_components as dbc
from dash import dcc


class Header:
    def __init__(self, title, description, img):
        self.header = html.Div(
            children=[
                html.Div(
                    children=[
                        html.P(children="", className="header-emoji"),
                        html.Img(src=app.get_asset_url('images/' + img),
                                 className="icondash"),
                        html.H1(
                            children=title, className="header-title"
                        ),
                        html.P(
                            children=description,
                            className="header-description",
                        ),
                    ],
                    className="header",
                )
            ],
            className="header-out",
            style={
                "margin-left": "15rem",
                "padding": "1.5rem 2rem",
                "border": "0px"
            }
        )

class StyleNaDashApp:
    def __init__(self, page):
        self.page = page
        self.SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
        }

        # padding for the page content
        content = [
            html.H2("Drag Race Italia", className="display-4"),
            html.Hr(),
            html.P(
                "", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("General", href="/", active="exact"),
                    # dbc.DropdownMenu(
                    #     children=[
                    #         dbc.DropdownMenuItem("Theme", href="/comemberships"),
                            # dbc.DropdownMenuItem("Personas", href="/personas"),
                            # dbc.DropdownMenuItem("Organizations", href="/organizations"),
                    #     ],
                    #     nav=True,
                    #     in_navbar=True,
                    #     label="Co Memberships",
                    #     direction="right"
                    # ),
                    dbc.NavLink("Episode 1", href="/general", active="exact"),
                    # dbc.NavLink("Co Members", href="/comembers", active="exact"),
                    dbc.NavLink("Episode 2", href="/organizations", active="exact"),

                ],
                vertical=True,
                pills=True,
            ),

        ]
        if page != 'index':
            content += [html.H6(
                "Database", className=""),
                dcc.Dropdown(

                    id='database-dropdown',
                    options=[
                        {'label': 'opdm', 'value': 'opdm'},
                        {'label': 'neo4j', 'value': 'neo4j'},
                        {'label': 'opdm.umbria', 'value': 'opdm.umbria'},
                    ],
                    value='opdm.umbria'
                )]

        self.sidebar = html.Div(
            content,
            style=self.SIDEBAR_STYLE,
        )