from flask import Flask as _Flask
from dash import Dash as _Dash
import dash_bootstrap_components as _dbc


DASH_BASE_PATHNAME = '/jinder/'


flask_server = _Flask(__name__)
flask_server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app = _Dash(name=__name__,
            server=flask_server,
            url_base_pathname=DASH_BASE_PATHNAME,
            suppress_callback_exceptions=True,
            external_stylesheets=[_dbc.themes.BOOTSTRAP])
app.title = 'Jinder'
