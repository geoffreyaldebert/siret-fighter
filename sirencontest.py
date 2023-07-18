import dash
import dash_auth
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import random
import json
import numpy as np
import requests

import plotly.express as px

from secretsAuth import *

from os import listdir

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'],suppress_callback_exceptions=True)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

orgas = pd.read_csv("orgas.csv", dtype=str)

output_orgas = pd.read_csv("output_orgas.csv", dtype=str)


actual_id = None
fighter = None
actual_siret = None
list_ids_processed = output_orgas["id"].to_list()
orgas = orgas[~orgas["id"].isin(list_ids_processed)]

@app.callback(
    dash.dependencies.Output('test', 'children'),
    dash.dependencies.Input('input-fighter', 'value'),
)
def update_fighter(input_fighter):
    global fighter
    fighter = input_fighter
    return html.P("")


@app.callback(
    dash.dependencies.Output('test2', 'children'),
    dash.dependencies.Input('input-candidats', 'value'),
)
def update_siret(input_siret):
    global actual_siret
    actual_siret = input_siret
    return html.P("")


@app.callback(
    dash.dependencies.Output('test3', 'children'),
    dash.dependencies.Input('input_text', 'value'),
)
def update_siret2(input_siret):
    global actual_siret
    actual_siret = input_siret
    return html.P("")


@app.callback(
    [
        dash.dependencies.Output('alert-1', 'children', allow_duplicate=True),
        dash.dependencies.Output('refresh-button', 'n_clicks', allow_duplicate=True)
    ],
    dash.dependencies.Input('validate-button-sure', 'n_clicks'),
    prevent_initial_call=True,
)
def validate_siret_1(btn1):
    if btn1:
        global actual_siret
        global actual_id
        global fighter
        global list_ids_processed
        global orgas
        test = save_result(True)
        alert = ""
        res = btn1
        if not test:
            if not actual_siret:
                alert_text = "Sélectionnez une proposition avant de valider"
            if not fighter:
                alert_text = "Sélectionnez un combattant pour sauver votre score"
            alert = dbc.Alert(
                alert_text,
                id="alert-fade",
                dismissable=True,
                is_open=True,
            ),
            res = None
        else:
            list_ids_processed.append(actual_id)
            orgas = orgas[~orgas["id"].isin(list_ids_processed)]
            file1 = open("output_orgas.csv", "a")
            file1.write(f"\n{actual_id},{actual_siret},{fighter},True")
            file1.close()
        return html.P(alert), res
    else:
        raise dash.exceptions.PreventUpdate


@app.callback(
    [
        dash.dependencies.Output('alert-1', 'children', allow_duplicate=True),
        dash.dependencies.Output('refresh-button', 'n_clicks', allow_duplicate=True),
    ],
    dash.dependencies.Input('validate-button-not-sure', 'n_clicks'),
    prevent_initial_call=True,
)
def validate_siret_2(btn1):
    if btn1:
        global actual_siret
        global actual_id
        global fighter
        global orgas
        test = save_result(False)
        alert = ""
        res = btn1
        if not test:
            if not actual_siret:
                alert_text = "Sélectionnez une proposition avant de valider"
            if not fighter:
                alert_text = "Sélectionnez un combattant pour sauver votre score"
            alert = dbc.Alert(
                alert_text,
                id="alert-fade",
                dismissable=True,
                is_open=True,
            ),
            res = None
        else:
            list_ids_processed.append(actual_id)
            orgas = orgas[~orgas["id"].isin(list_ids_processed)]
            file1 = open("output_orgas.csv", "a")
            file1.write(f"\n{actual_id},{actual_siret},{fighter},False")
            file1.close()
        return html.P(alert), res
    else:
        raise dash.exceptions.PreventUpdate


@app.callback(
    [
        dash.dependencies.Output('alert-1', 'children', allow_duplicate=True),
        dash.dependencies.Output('refresh-button', 'n_clicks', allow_duplicate=True),
    ],
    dash.dependencies.Input('validate_input-button', 'n_clicks'),
    prevent_initial_call=True,
)
def validate_siret_3(btn1):
    if btn1:
        global actual_siret
        global actual_id
        global fighter
        global orgas
        test = save_result(True)
        alert = ""
        res = btn1
        if not test:
            if not actual_siret:
                alert_text = "Entrez un siret dans le champs texte avant de valider"
            if not fighter:
                alert_text = "Sélectionnez un combattant pour sauver votre score"
            alert = dbc.Alert(
                alert_text,
                id="alert-fade",
                dismissable=True,
                is_open=True,
            ),
            res = None
        else:
            list_ids_processed.append(actual_id)
            orgas = orgas[~orgas["id"].isin(list_ids_processed)]
            file1 = open("output_orgas.csv", "a")
            file1.write(f"\n{actual_id},{actual_siret},{fighter},True")
            file1.close()
        return html.P(alert), res
    else:
        raise dash.exceptions.PreventUpdate


@app.callback(
    [
        dash.dependencies.Output('alert-1', 'children', allow_duplicate=True),
        dash.dependencies.Output('refresh-button', 'n_clicks', allow_duplicate=True),
    ],
    dash.dependencies.Input('validate-button-no-siret', 'n_clicks'),
    prevent_initial_call=True,
)
def validate_siret_4(btn1):
    if btn1:
        global actual_siret
        global actual_id
        global fighter
        global orgas
        res = btn1
        alert = ""
        if not fighter:
            alert_text = "Sélectionnez un combattant pour sauver votre score"
            alert = dbc.Alert(
                alert_text,
                id="alert-fade",
                dismissable=True,
                is_open=True,
            ),
            res = None
        else:
            list_ids_processed.append(actual_id)
            orgas = orgas[~orgas["id"].isin(list_ids_processed)]
            file1 = open("output_orgas.csv", "a")
            file1.write(f"\n{actual_id},None,{fighter},True")
            file1.close()
        return html.P(alert), res
    else:
        raise dash.exceptions.PreventUpdate


def save_result(sure):
    if actual_id and actual_siret and fighter:
        return True
    else:
        return False
        


@app.callback(
    [
        dash.dependencies.Output("nom-orga", "children"),
        dash.dependencies.Output("candidats-orgas", "children"),
        dash.dependencies.Output('Torgnax-points', 'children'),
        dash.dependencies.Output('Turbofist-points', 'children'),
        dash.dependencies.Output('Kikaboum-points', 'children'),
        dash.dependencies.Output('Foudrielle-points', 'children'),
        dash.dependencies.Output('Blitzo-points', 'children'),
        dash.dependencies.Output('Zippy-points', 'children'),
        dash.dependencies.Output('Pichenet-points', 'children'),
        dash.dependencies.Output('Dualia-points', 'children'),
    ],
    [dash.dependencies.Input("refresh-button",'n_clicks')],
    prevent_initial_call=True
)
def button_pushed(btn1):
    if btn1:
        global actual_id
        global actual_siret
        global orgas
        global output_orgas
        global list_ids_processed
        output_orgas = pd.read_csv("output_orgas.csv", dtype=str)
        list_ids_processed = output_orgas["id"].to_list()
        orgas = orgas[~orgas["id"].isin(list_ids_processed)]

        fighter_points_span = []
        fighter_names = ["Torgnax", "Turbofist", "Kikaboum", "Foudrielle", "Blitzo", "Zippy", "Pichenet", "Dualia"]
        for fighter in fighter_names:
            fighter_points_span.append(
                html.Span(" (" + str(output_orgas[output_orgas["fighter"] == fighter].shape[0]) + " pts)")
            )

        actual_siret = None
        actual_id = None
        df = orgas.sample(n=1)
        actual_id = df.iloc[0]["id"]
        orga_name = df.iloc[0]["name"]
        orga_desc = df.iloc[0]["description"]
        orga_url = f"https://www.data.gouv.fr/fr/organizations/{actual_id}"
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?q={orga_name}")
        if "results" in r.json():
            data = r.json()["results"][:3]
        else:
            data = []

        candidats = []
        for d in data:
            candidats.append({
                "label":
                    [
                        html.A(
                            d["nom_complet"],
                            href=f"https://annuaire-entreprises.data.gouv.fr/etablissement/{d['siege']['siret']}",
                            target="_blank",
                            style={"margin-left": "10px"}
                        ),
                    ],
                "value": d["siege"]["siret"],
            })
        if data:
            list_candidats = dcc.RadioItems(candidats, id="input-candidats")
        else:
            list_candidats = html.P("Aucun candidat trouvé")

        output_candidat = html.Div([
            list_candidats,        
            html.Br(),
            html.Button('Je suis sûr', id='validate-button-sure'),
            html.Button('Je suis moyennement sûr', id='validate-button-not-sure'),
            html.Br(),
            html.Br(),
            html.P("Si non présent dans la liste ci-dessus : "),
            dcc.Input(
                id="input_text",
                type="text",
                placeholder='Entrez SIRET',
                value="",
            ),
            html.Button('Valider', id='validate_input-button'),
            html.Br(),
            html.Br(),
            html.Button('Pas de SIRET pour cette organisaton', id='validate-button-no-siret'),
            html.Br(),
            html.Br(),

        ])

        return (
            html.Div([
                html.A(orga_name, href=orga_url, target="_blank"),
                html.Br(),
                html.Br(),
                html.P("Description :"),
                html.P(orga_desc)
            ]),
            output_candidat,
            fighter_points_span[0],
            fighter_points_span[1],
            fighter_points_span[2],
            fighter_points_span[3],
            fighter_points_span[4],
            fighter_points_span[5],
            fighter_points_span[6],
            fighter_points_span[7],
        )
    else:
        raise dash.exceptions.PreventUpdate

def serve_layout():
    return html.Div([
        html.Div([
            html.H1("Siret Fighter")
        ]),
        html.Div([
            html.H3("Chose your fighter !")
        ]),
        html.Div([
            dcc.RadioItems(
                [
                    {
                        "label":
                            [
                                html.Img(src="assets/perso1.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Torgnax", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Torgnax"].shape[0]) + " pts)"),
                                    id="Torgnax-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Torgnax",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso2.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Turbofist", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Turbofist"].shape[0]) + " pts)"),
                                    id="Turbofist-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ], 
                        "value": "Turbofist",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso3.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Kikaboum", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Kikaboum"].shape[0]) + " pts)"),
                                    id="Kikaboum-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Kikaboum",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso4.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Foudrielle", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Foudrielle"].shape[0]) + " pts)"),
                                    id="Foudrielle-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Foudrielle",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso5.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Blitzo", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Blitzo"].shape[0]) + " pts)"),
                                    id="Blitzo-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Blitzo",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso6.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Zippy", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Zippy"].shape[0]) + " pts)"),
                                    id="Zippy-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Zippy",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso7.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Pichenet", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Pichenet"].shape[0]) + " pts)"),
                                    id="Pichenet-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Pichenet",
                    },
                    {
                        "label":
                            [
                                html.Img(src="assets/perso8.png", height=100, style={"margin-left": "20px"}),
                                html.Span("Dualia", style={'font-size': 13, 'padding-left': 10}),
                                html.Span(
                                    children=html.Span(" (" + str(output_orgas[output_orgas["fighter"] == "Dualia"].shape[0]) + " pts)"),
                                    id="Dualia-points",
                                    style={'font-size': 12, 'margin-right': '20px'}
                                ),
                            ],
                        "value": "Dualia",
                    },
                ],
                labelStyle={"float": "left", "width": "270px", "margin-right": "30px", "margin-bottom": "20px", "border": "1px solid black"},
                id="input-fighter"
            )
        ]),

        html.Button('Next fight', id='refresh-button',n_clicks=0),
        html.Br(),
        html.Br(),
        html.Div(id="alert-1", children=[]),
        html.Div([
            html.Div([
                html.P("Nom orga"),
                html.Div(id="nom-orga",children=[]),
            ], style={'width':'500px', 'border': '1px solid black', 'padding': '10px', }),
            html.Div([
                html.P("Candidats"),
                html.Div(id="candidats-orgas",children=[]),
            ], style={'width':'500px', 'border': '1px solid black', 'padding': '10px', 'margin-left': '20px'}),
        ], style={'display': 'flex'}),
        html.Div(id="test", children=[]),
        html.Div(id="test2", children=[]),
        html.Div(id="test3", children=[]),
        html.Div(id="test4", children=[]),
        html.Div(id="test5", children=[]),
        html.Div(id="test6", children=[])
    ],style={'width':'1200px','margin':'auto'})

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True,port=7676)