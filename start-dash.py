import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from remote import Remote


class Dashboard:
    def __init__(self):
        self.host = json.load(open("config.json", "r"))['server_address']
        self.remote = Remote(self.host)
        self.app = dash.Dash(
            title="Discadminecraft",
            update_title=None,
            external_stylesheets=[{"href": "assets/style.css", "rel": "stylesheet"}]
        )

        self.app.layout = html.Div(
            className="wrapper",
            children=[
                html.Div(
                    className="console",
                    children=[
                        html.Div(className="console-title", children=[html.Span(children="Console")]),
                        html.Div(className="console-text", children=[html.Pre(id="live-console-output")]),
                        html.Span(className="console-input", children=[
                            html.I(children=">"),
                            dcc.Input(id="console-input-field", className="console-input-field")
                        ]),
                        dcc.Interval(id="live-console-interval", interval=1000, n_intervals=0)
                    ]
                ),
                html.Div(
                    className="buttons-div",
                    children=[
                        html.Button(className="start-button", id="start-button", children="⏻ Start server",
                                    style={"display": "none"}),
                        html.Button(className="stop-button", id="stop-button", children="⏻ Stop server",
                                    style={"display": "none"})
                    ]
                ),
                html.P(id='placeholder'),
                html.P(id='placeholder2')
            ]
        )

        self.make_button_functions()
        self.app.run_server(host="0.0.0.0")

    def make_button_functions(self):
        self.logcache = ""

        @self.app.callback(Output('start-button', 'style'),
                           Output('stop-button', 'style'),
                           Output('live-console-output', 'children'),
                           Input('live-console-interval', 'n_intervals'))
        def show_hide_start(n):
            status = ""
            try:
                status = self.remote.status()
            except OSError:
                pass
            if status == 'stopped' or status == "":
                self.logcache = ""
                return {}, {"display": "none"}, "Server stopped"
            else:
                log = ""
                while True:
                    try:
                        log = self.remote.log()
                        break
                    except OSError:
                        continue
                if self.logcache in log:
                    new = log[len(self.logcache):]
                    if new:
                        self.logcache = log
                return {'display': 'none'}, {}, self.logcache

        @self.app.callback(Output('placeholder', 'children'),
                           Input('start-button', 'n_clicks'))
        def start_server(n):
            if n is not None:
                while True:
                    try:
                        self.remote.start()
                        break
                    except OSError:
                        continue
            return ""

        @self.app.callback(Output('placeholder2', 'children'),
                           Input('stop-button', 'n_clicks'))
        def stop_server(n):
            if n is not None:
                while True:
                    try:
                        self.remote.stop()
                        break
                    except OSError:
                        continue
            return ""

        self.submit_count = None

        @self.app.callback(Output('console-input-field', 'value'),
                           Input('console-input-field', 'value'),
                           Input("console-input-field", "n_submit"))
        def read_command(value, n_submit):
            if n_submit != self.submit_count:
                self.submit_count = n_submit
                if n_submit:
                    while True:
                        try:
                            self.remote.run(value)
                            break
                        except OSError:
                            continue
                    return ""
            return value


Dashboard()
