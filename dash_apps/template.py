import sys as _sys
import os as _os

_head, _sep, _tail = _os.path.abspath(__file__).partition('govhack2019')
_sys.path.insert(0, _os.path.join(_head, _sep))

import pandas as _pd

import plotly_express as _px
import plotly.graph_objs as _go
import dash as _dash
import dash_html_components as _html
import dash_core_components as _dcc
import dash_bootstrap_components as _dbc
from dash.dependencies import Input as _Input, Output as _Output, State as _State

from server import app as _app
from app_util.logging import log_callback_exception as _log_callback_exception


def _generate_page():
    layout_ = _html.Div(
        _html.Div([
            _html.Div([
                _html.Div([
                    'Test 1'
                ], style={'display': 'table-cell', 'width': '40%'}),
                _html.Div([
                    'Test 2'
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    'Test 1'
                ], style={'display': 'table-cell', 'width': '40%'}),
                _html.Div([
                    'Test 2'
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    'Test 1'
                ], style={'display': 'table-cell', 'width': '40%'}),
                _html.Div([
                    'Test 2'
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
        ], style={'display': 'table', 'width': '100%'}),
        id='template_div',
        style={'width': '1200px', 'margin': '0 auto'}
    )
    return layout_


def _init_callbacks():
    pass


category = 'Job Description Generator'
description = 'Job Description Generator'
layout = _generate_page
init_callbacks = _init_callbacks
