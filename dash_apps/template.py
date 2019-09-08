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


_purpose_of_the_role = (
    'Working alongside and supporting a highly experienced project manager '
    + 'who enjoys mentoring and developing those around him. '
    + 'Ensure optimum outcomes regarding safety, quality, reliability and capacity meet '
    + 'the delivery program schedules, relative to program costs.',
)

_duties = {
    'Review specifications':
        'Review and Amend existing Internal Specifications as required from various stakeholders' + ' ' * 150,
    'Technical maintenance':
        'Ongoing specification technical maintenance' + ' ' * 150,
    'Specifications delivery':
        'Delivery customer specifications on time for samples through to final approved specifications' + ' ' * 150,
}

_skills = {
    'Communication':
        'Excellent interpersonal and communication skills' + ' ' * 150,
    'Reporting': 'Strong reporting experience' + ' ' * 150,
    'Excavation': 'Sound knowledge of construction from excavation' + ' ' * 150,
    'Subcontractors': 'Excellent knowledge of subcontractors' + ' ' * 150,
}

_qualifications = {
    'Carpenter': 'Trade qualified as Carpenter' + ' ' * 150,
    '1st/2nd Tier': 'Tier 1 and 2 head contractor experience' + ' ' * 150,
    'High Rise': 'Experience in high rise residential construction projects' + ' ' * 150,
}


def _generate_page():
    layout_ = _html.Div(
        _html.Div([
            _html.Div([
                _html.Div([
                    _html.H4('Job Title'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Input(
                        placeholder='Job Title...',
                        type='text',
                        value='Structures Foreman',
                        style={'display': 'inline-block', 'width': '100%'},
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Purpose of the role')
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Textarea(
                        placeholder='Enter a value...',
                        value=_purpose_of_the_role,
                        style={'width': '100%', 'height': '100px'}
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Main Duties / Responsibilities'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div(style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    _dcc.Dropdown(
                        options=[
                            {'label': duty, 'value': duty}
                            for duty in _duties.keys()
                        ],
                        value=list(_duties.keys()),
                        multi=True,
                        style={'margin-right': '10px'}
                    )
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Textarea(
                        placeholder='Enter a value...',
                        value=''.join(_duties.values()),
                        style={'width': '100%', 'height': '120px'}
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Skills'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div(style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    _dcc.Dropdown(
                        id='skill_selector',
                        options=[
                            {'label': skill, 'value': skill}
                            for skill in _skills.keys()
                        ],
                        value=list(_skills.keys())[:2],
                        multi=True,
                        style={'margin-right': '10px'}
                    )
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Textarea(
                        id='skills',
                        placeholder='Enter a value...',
                        value=''.join(list(_skills.values())[:2]),
                        style={'width': '100%', 'height': '120px'}
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Qualifications & Experience'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div(style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    _dcc.Dropdown(
                        options=[
                            {'label': qual, 'value': qual}
                            for qual in _qualifications.keys()
                        ],
                        value=list(_qualifications.keys()),
                        multi=True,
                        style={'margin-right': '10px'}
                    )
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Textarea(
                        placeholder='Enter a value...',
                        value=''.join(_qualifications.values()),
                        style={'width': '100%', 'height': '120px'}
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Salary Range'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div(style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div([
                _html.Div([
                    _html.Div(
                        _dcc.Dropdown(
                            id='state_selector',
                            options=[
                                {'label': 'NSW', 'value': 'NSW'},
                                {'label': 'ACT', 'value': 'ACT'},
                                {'label': 'VIC', 'value': 'VIC'},
                                {'label': 'QLD', 'value': 'QLD'},
                                {'label': 'WA', 'value': 'WA'},
                                {'label': 'NT', 'value': 'NT'},
                                {'label': 'TAS', 'value': 'TAS'},
                            ],
                            value='NSW',
                            multi=False,
                            clearable=False,
                            style={'width': '100px'}
                        ), style={'margin-right': '10px', 'display': 'inline-block'}
                    ),
                    _html.Div(
                        _dcc.Dropdown(
                            id='area_selector',
                            options=[
                                {'label': 'All Sydney', 'value': 'Sydney'},
                                {'label': 'All ACT', 'value': 'ACT'},
                            ],
                            value='Sydney',
                            multi=False,
                            clearable=False,
                            style={'width': '250px'}
                        ), style={'display': 'inline-block'}
                    )
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _html.Div(
                        _dcc.Dropdown(
                            id='salary_low',
                            options=[
                                {'label': '$100,000', 'value': 100000},
                                {'label': '$110,000', 'value': 110000},
                                {'label': '$120,000', 'value': 120000},
                                {'label': '$130,000', 'value': 130000},
                                {'label': '$140,000', 'value': 140000},
                                {'label': '$150,000', 'value': 150000},
                            ],
                            value=100000,
                            style={'width': '200px'}
                        ), style={'display': 'inline-block', 'margin-right': '10px'}
                    ),
                    _html.Plaintext('-', style={'display': 'inline-block', 'margin-right': '10px',
                                                'vertical-align': 'top'}),
                    _html.Div(
                        _dcc.Dropdown(
                            id='salary_high',
                            options=[
                                {'label': '$100,000', 'value': 100000},
                                {'label': '$110,000', 'value': 110000},
                                {'label': '$120,000', 'value': 120000},
                                {'label': '$130,000', 'value': 130000},
                                {'label': '$140,000', 'value': 140000},
                                {'label': '$150,000', 'value': 150000},
                            ],
                            value=130000,
                            style={'width': '200px'}
                        ), style={'display': 'inline-block', 'margin-right': '10px'}
                    ),
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div([
                    _html.H4('Other'),
                ], style={'display': 'table-cell', 'width': '40%', 'vertical-align': 'top'}),
                _html.Div([
                    _dcc.Textarea(
                        placeholder='Enter a value...',
                        value='',
                        style={'width': '100%', 'height': '120px'}
                    )
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
            _html.Div(style={'display': 'table-row', 'width': '100%', 'height': '20px'}),
            _html.Div([
                _html.Div(style={'display': 'table-cell', 'width': '40%'}),
                _html.Div([
                    _html.Button('Preview', id='preview_button')
                ], style={'display': 'table-cell', 'width': '60%'}),
            ], style={'display': 'table-row', 'width': '100%'}),
        ], style={'display': 'table', 'width': '100%'}),
        id='template_div',
        style={'width': '1200px', 'margin': '0 auto'}
    )
    return layout_


def _init_callbacks():
    @_app.callback(_Output('template_div', 'children'),
                   [_Input('preview_button', 'n_clicks')])
    @_log_callback_exception()
    def _preview(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return _dash.no_update
        jd = [
            _html.H2('Structures Foreman'),
            _html.H6('The Company:'),
            _html.P('Our company is a boutique multi award winning building contractor '
                    + 'with a fantastic history of success and a very low turnover of staff.'),
            _html.H6('Purpose of the role:'),
            _html.P(_purpose_of_the_role),
            _html.H6('Main Duties / Responsibilities:'),
            _html.Ul(
                [_html.Li(duty) for duty in _duties.values()]
            ),
            _html.H6('Skills:'),
            _html.Ul(
                [_html.Li(skill) for skill in list(_skills.values())[:-1]]
            ),
            _html.H6('Qualifications & Experience:'),
            _html.Ul(
                [_html.Li(qual) for qual in _qualifications.values()]
            ),
            _html.H6('Salary Range: $120,000 - $150,000'),
            _html.P('If you have the relevant skill set and experience as set out above '
                    + 'and are interested in discussing this opportunity further, '
                    + 'please send across your CV to XXX XXX or call 02 XXXX XXXX.')
        ]
        children = [
            _html.Div(jd),
            _html.Div(
                _html.Button('Publish', id='publish_button'),
                id='publish_status_div',
                style={'display': 'inline-block', 'margin-right': '20px'}
            ),
            _html.Div(style={'margin': '20px'}),
        ]
        return children

    @_app.callback(_Output('publish_status_div', 'children'),
                   [_Input('publish_button', 'n_clicks')])
    @_log_callback_exception()
    def _publish(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return _dash.no_update
        return [
            _html.Div(
                _html.P('Posted on jobsearch.gov.au', style={'color': 'green'}),
                style={'background-color': 'lightgreen', 'padding': '5px', 'display': 'inline-block'}
            ),
            _html.Div(style={'width': '10px', 'display': 'inline-block'}),
            _html.Div(
                _html.P('Failed to post on seek.com.au', style={'color': 'red'}),
                style={'background-color': 'salmon', 'padding': '5px', 'display': 'inline-block'}
            ),
            _html.Div(style={'width': '10px', 'display': 'inline-block'}),
            _html.Div(
                _html.P('Alerted job advisers.', style={'color': 'green'}),
                style={'background-color': 'lightgreen', 'padding': '5px', 'display': 'inline-block'}
            ),
        ]

    @_app.callback(_Output('area_selector', 'value'),
                   [_Input('state_selector', 'value')])
    @_log_callback_exception()
    def _change_area(state):
        if state == 'ACT':
            return 'ACT'
        else:
            return 'Sydney'

    @_app.callback([_Output('salary_low', 'value'),
                    _Output('salary_high', 'value')],
                   [_Input('area_selector', 'value')])
    @_log_callback_exception(2)
    def _change_area(area):
        if area == 'ACT':
            return 120000, 150000
        else:
            return 100000, 130000

    @_app.callback(_Output('skills', 'value'),
                   [_Input('skill_selector', 'value')])
    @_log_callback_exception()
    def _change_area(skills):
        if skills is None:
            return _dash.no_update
        else:
            return ''.join(_skills[skill] for skill in skills)


category = 'Job Description Generator'
description = 'Job Description Generator'
layout = _generate_page
init_callbacks = _init_callbacks
