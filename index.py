import base64 as _base64

import sys as _sys
import os as _os
from importlib import import_module as _import_module
from importlib import reload as _reload

_head, _sep, _tail = _os.path.abspath(__file__).partition('govhack2019')
_sys.path.insert(0, _os.path.join(_head, _sep))

from flask import request as _request
import dash_html_components as _html
import dash_core_components as _dcc
import dash_bootstrap_components as _dbc
from dash.dependencies import Input as _Input, Output as _Output

from app_util.file_sys_reader import list_files as _list_files
import server as _server
from server import app as _app


def _load_app_module(app: str, is_dash: bool=True):
    """Load underlying module of a Dash app.

    Args:
        app: App's corresponding file name.

    Returns:
        Module loaded.
    """
    mod = _import_module(('dash_apps.' if is_dash else 'apps.') + app)
    if app[:4] == 'dev_':
        mod = _reload(mod)
    return mod


def _get_apps(is_dash: bool=True, include_dev: bool=False):
    """Get a list of available Dash apps.

    Args:
        include_dev: Include apps in development or not.

    Returns:
        List of available apps.
    """
    apps = _list_files(folder=_os.path.join(_head, _sep, 'dash_apps' if is_dash else 'apps'), suffix='py')
    if include_dev:
        apps = [app[:-3] for app in apps]
    else:
        apps = [app[:-3] for app in apps if app[:4] != 'dev_']
    return apps


def _get_app_info(app, is_dash: bool=True):
    """Get Dash app information.

    Args:
        app: App's corresponding file name.

    Returns:
        category: App category.
        description: App description.
    """
    mod = _load_app_module(app, is_dash=is_dash)
    return getattr(mod, 'category'), getattr(mod, 'description')


def _get_dash_app_content(app):
    """Get Dash app content.

    Args:
        app: App's corresponding file name.

    Returns:
        App content.
    """
    mod = _load_app_module(app, is_dash=True)
    return getattr(mod, 'layout')()


def _init_app(app, is_dash=True):
    """Initialise Dash app callbacks.

    Args:
        app: App's corresponding file name.
    """
    mod = _load_app_module(app, is_dash=is_dash)
    if is_dash:
        if hasattr(mod, 'init_callbacks'):
            getattr(mod, 'init_callbacks')()
    else:
        if hasattr(mod, 'init_routes'):
            getattr(mod, 'init_routes')()


def _generate_nav():
    jinder_logo = open(_os.path.join(_head, _sep, 'static', 'white logo.png'), 'rb').read()
    jinder_logo = _base64.b64encode(jinder_logo).decode('utf-8')
    navigation_bar = [
        _html.Div(
            _dcc.Link(
                _html.Img(
                    src='data:image/jpeg;base64,{}'.format(jinder_logo),
                    height='50px',

                ),
                href=_server.DASH_BASE_PATHNAME + 'index'
            ),
            style={'margin': '5px', 'display': 'inline-block'}
        )
    ]
    nav_items = []
    app_info_list = []
    dash_apps = _get_apps(is_dash=True)
    if dash_apps:
        for app in dash_apps:
            category, description = _get_app_info(app, is_dash=True)
            link = _server.DASH_BASE_PATHNAME + app
            app_info_list.append(dict(category=category, description=description, link=link, is_dash=True))
    flask_apps = _get_apps(is_dash=False)
    if flask_apps:
        for app in flask_apps:
            category, description = _get_app_info(app, is_dash=False)
            link = '/' + app + '/'
            app_info_list.append(dict(category=category, description=description, link=link, is_dash=False))
    if app_info_list:
        app_info_list.sort(key=lambda x: [x['category'], x['description']])
        # group apps based on category
        current_category = app_info_list[0]['category']
        menu_items = []
        for i, app in enumerate(app_info_list):
            if app['category'] != current_category:
                nav_items.append(_dbc.DropdownMenu(menu_items, label=current_category, nav=True))
                current_category = app['category']
                menu_items = []
            menu_items.append(_dbc.DropdownMenuItem(app['description'],
                                                    href=app['link'],
                                                    # external_link=not app['is_dash']))
                                                    external_link=True))
        nav_items.append(_dbc.DropdownMenu(menu_items, label=current_category, nav=True, style={'a.color': 'black'}))
        # construct navigation bar
        navigation_bar.append(_html.Div(
            _dbc.Nav(nav_items),
            id='jinder-nav',
            style={'vertical-align': 'middle', 'display': 'inline-block'}
        ))
    return _html.Div(navigation_bar, style={'height': '60px', 'background-color': 'rgb(255,255,255)'})


def _generate_dash_index_page():
    """Set up index page.

    Returns:
        Index page.
    """
    _app.title = 'Jinder'
    app_info_list = []
    dash_apps = _get_apps(is_dash=True, include_dev=False)
    if dash_apps:
        for app in dash_apps:
            category, description = _get_app_info(app, is_dash=True)
            link = _server.DASH_BASE_PATHNAME + app
            app_info_list.append(dict(category=category, description=description, link=link))
    flask_apps = _get_apps(is_dash=False, include_dev=False)
    if dash_apps:
        for app in flask_apps:
            category, description = _get_app_info(app, is_dash=False)
            link = '/' + app + '/'
            app_info_list.append(dict(category=category, description=description, link=link))
    if app_info_list:
        app_info_list.sort(key=lambda x: [x['category'], x['description']])
        # group links based on category
        divs = []
        current_category = app_info_list[0]['category']
        divs.append(_html.H2(current_category))
        for i, app in enumerate(app_info_list):
            if app['category'] == current_category:
                if i != 0:
                    divs.append(_html.Br())
            else:
                current_category = app['category']
                divs.append(_html.H2(current_category))
            divs.append(_dcc.Link(app['description'], href=app['link'], refresh=True))
        index_page = _html.Div(divs,
                               style={'margin': '10px'})
    else:
        index_page = _html.Div([_html.Plaintext('Website under maintenance. Please come back later.')],
                               style={'margin': '10px'})
    return index_page


def _shutdown_server():
    """Shutdown server.
    """
    func = _request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# set up page layout
_app.layout = _html.Div([
    _dcc.Location(id='url', refresh=False),
    _generate_nav(),
    _html.Div(
        # TODO: switch default value to 0 when demo mode is ready
        _dcc.Slider(id='website_mode', min=0, max=2, step=1,
                    marks={0: 'Full View', 1: 'Demo View', 2: 'Dev View'}),
        id='website_mode_div',
        style={'display': 'none'}
    ),
    _html.Div(id='no_output_callback_placeholder'),
    _html.Div(id='page-content')
])


@_app.callback(_Output('page-content', 'children'),
               [_Input('url', 'pathname')])
def _display_page(pathname):
    if pathname is not None and pathname.startswith(_server.DASH_BASE_PATHNAME):
        pathname = pathname[len(_server.DASH_BASE_PATHNAME):]
    if pathname is None or pathname == '' or pathname == 'index':
        children = _generate_dash_index_page()
    elif pathname == 'shutdown':
        _shutdown_server()
        children = 'Server shutting down...'
    elif pathname in _get_apps(include_dev=True):
        children = _get_dash_app_content(pathname)
    else:
        # TODO: return a 404 "URL not found" page here
        children = _html.Div([_html.Plaintext('404: {} not found'.format(pathname))])
    return children


@_server.flask_server.route('/jinder/<path>')
def _load_dash_path(path):
    if path is None or path == '' or path == 'index':
        title = 'Jinder'
    elif path == 'shutdown':
        title = 'Server Shutdown'
    elif path in _get_apps(include_dev=True):
        title = _get_app_info(path)[1]
    else:
        title = '404 ' + path
    _app.title = title
    # _app.title = path
    return _app.index()


# TODO: change behaviour
@_server.flask_server.route('/')
def _homepage():
    import flask
    return flask.redirect('/jinder/')


def start_webservice(local_only=False):
    dash_apps = _get_apps(is_dash=True, include_dev=True)
    if dash_apps:
        for app in dash_apps:
            _init_app(app, is_dash=True)
    flask_apps = _get_apps(is_dash=False, include_dev=True)
    if flask_apps:
        for app in flask_apps:
            _init_app(app, is_dash=False)
    if local_only:
        _app.run_server(port=8050, debug=False)
    else:
        from app_util.logging import setup_logging
        setup_logging()
        _app.run_server(host='0.0.0.0', port=8050, debug=False)


if __name__ == '__main__':
    start_webservice()
