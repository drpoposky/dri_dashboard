import pandas as pd
# import plotly.graph_objects as go
from dash import Dash, dcc, Input, Output,no_update, html  # pip install dash (version 2.0.0 or higher)
import json
# import numpy as np
import dash_bootstrap_components as dbc
from app import app
from apps.utils.general_layout import Header, StyleNaDashApp
import plotly.express as px
server = app.server

def replace_region_name(region_name):
    region_name = region_name.replace("Valle d'Aosta/Vallée d'Aoste","Valle d'Aosta")
    region_name = region_name.replace("Trentino-Alto Adige/Südtirol", "Trentino Alto Adige")
    return region_name

italy_regions = json.load(open("limits_IT_regions.geojson", "r"))
# print(italy_regions)
state_id_map = {}
for feature in italy_regions["features"]:
    feature["id"] = feature["properties"]["reg_istat_code_num"]
    state_id_map[replace_region_name(feature["properties"]["reg_name"])] = feature["id"]
df = pd.read_csv("italy_data.csv", sep=";", encoding = "ISO-8859-1")

df["id"] = df["region"].apply(lambda x: state_id_map[x])
df['Density'] = df['Density'].apply(lambda x: str(x))
# df['color'] = df['Density'].apply(lambda x: 'cf82ba' if x==1 else 0)
fig_italy = px.choropleth(
    df,
    locations="id",
    geojson=italy_regions,
    color="Density",
    # hover_name="nome_drag",
    hover_data={'Density':None,'id':None},
    color_discrete_map={'1': '#db2a87',
                        '0': '#edd172'},
    # title="Drag Queen location distribution",
    scope='europe',
    # color_continuous_scale=px.colors.diverging.Tealrose,
    # template='plotly_dark'
    basemap_visible=False,
    projection="natural earth",
    custom_data=['id'],


)
fig_italy.update_geos(
                      fitbounds="locations", visible=False,


                )
fig_italy.update_layout(showlegend=False)


# ------------------------------------------------------------------------------
# App layout


md_presentation_text = '''

'''
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = StyleNaDashApp('index').sidebar

header = Header('Drag Race Italia - Analysis', '', 'favicon.png').header

card_list = []
for key, value in {'Puntate':6, 'Concorrenti':8, 'Età media':33.6}.items():
    card_list.append(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(key.capitalize().replace('-', ' '), className="card-title"),
                        html.P(
                            id="number-" + key,
                            children=value,
                            className="card-value",
                        ),

                    ]
                ),
            ]
        )
    )
row = html.Div(
    [
        dcc.Loading(children=[dbc.CardDeck(card_list)], color="#119DFF", type="dot",
                    fullscreen=False)
    ], style={'padding': '25px'}
)

content = html.Div( [row,

    # html.H1('Network Analysis dashboards lab'),
    html.H1('Drag Queen spatial distribution'),
    dcc.Graph(id='my_bee_map', figure=fig_italy,clear_on_unhover=True,style={'width': '90vh', 'height': '90vh'},
              config={'displayModeBar': False},
),
dcc.Tooltip(id="graph-tooltip-5", direction='bottom'),
])

layout_index = [sidebar, header, html.Div(content, style=CONTENT_STYLE)]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
@app.callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("my_bee_map", "hoverData"),
)
def display_hover(hoverData):
    # print(1)
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    # print(hoverData)
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["location"]


    df_row = df[df['id']==num]
    if str(df_row.nome_drag.values[0])=='nan':
        return False, no_update, no_update
    img_src = df_row['image_url'].values[0]
    name_drag = df_row['nome_drag'].values[0]
    age = str(int(df_row['age_partecipazione_programma'].values[0]))
    actual_name = df_row['nome_reale'].values[0]
    # if len(desc) > 300: desc = desc[:100] + '...'

    children = [
        html.Div(children=[
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(name_drag, style={"color": "darkblue"}),
            html.H3([html.Strong("Età"),f": {age}"]),
            html.H3([html.Strong('Nome OOD'),f": {actual_name}"]),
        ],
        style={'width': '300px', 'white-space': 'normal'})
    ]

    return True, bbox, children

@app.callback(
    Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/general':
        print('comembership')
        return None

    else:
        return layout_index




# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)