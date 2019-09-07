from typing import Optional as _Optional

import sys as _sys
import os as _os
import logging as _logging
import functools as _functools
from logging.handlers import RotatingFileHandler as _RotatingFileHandler
from logging.handlers import SMTPHandler as _SMTPHandler

import pandas as _pd

import dash as _dash
from dash.exceptions import PreventUpdate as _PreventUpdate
import dash_html_components as _html

_head, _sep, _tail = _os.path.abspath(__file__).partition('govhack2019')
_sys.path.insert(0, _os.path.join(_head, _sep))


from server import app as _app


# set up logging filter
class _LogFilter(_logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return ('127.0.0.1' not in msg
                and not msg.startswith('localhost'))


# set up decorator for callback exception logging
def log_callback_exception(num_of_output: int=1, err_output: _Optional[int]=None):
    """Return a decorator that wraps the passed in function and logs
    exceptions should one occur, except for PreventUpdate exception.

    Args:
        num_of_output: The number of outputs expected by the wrapped function. By default it is 1.
        err_output: The 0-based index of output that will be used to display error message when an error occurs.
            Or None which indicates all outputs affected should display error message.
            By default it is None.

    Returns:
        Wrapped function.
    """
    def decorator(func):
        @_functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, _PreventUpdate):
                    # log the exception
                    _app.logger.exception('Exception @ ' + func.__name__)
                    if num_of_output == 1:
                        return _html.P('An error has occurred and website admin has been notified.',
                                       style={'color': 'red', 'margin': '10px'})
                    else:
                        if err_output is not None:
                            # ret = [_dash.no_update for _ in range(num_of_output)]
                            ret = [_html.Div() for _ in range(num_of_output)]
                            ret[err_output] = _html.P('An error has occurred and website admin has been notified.',
                                                      style={'color': 'red', 'margin': '10px'})
                            return ret
                        else:
                            return [_html.P('Error. Admin notified.', style={'color': 'red', 'margin': '10px'})
                                    for _ in range(num_of_output)]
                else:
                    # re-raise the PreventUpdate exception
                    raise e
        return wrapper
    return decorator


def setup_logging():
    _EMAIL_LOG_HOST = 'outlook.challenger.com.au'
    _EMAIL_LOG_FROM = 'xiaochen.huang@benthamam.com'
    _EMAIL_LOG_TO = 'xiaochen.huang@benthamam.com'
    _EMAIL_LOG_CREDENTIALS = None
    _EMAIL_LOG_SECURE = None
    try:
        _config_df = _pd.read_csv(_os.path.join(_head, _sep, 'app_util', 'config.csv'), header=0, index_col=0)
        if 'email_log_host' in _config_df.index:
            _EMAIL_LOG_HOST = _config_df.loc['email_log_host', 'value']
        if 'email_log_host_port' in _config_df.index:
            _EMAIL_LOG_HOST = (_EMAIL_LOG_HOST, _config_df.loc['email_log_host_port', 'value'])
        if 'email_log_from' in _config_df.index:
            _EMAIL_LOG_FROM = _config_df.loc['email_log_from', 'value']
        if 'email_log_to' in _config_df.index:
            _EMAIL_LOG_TO = _config_df.loc['email_log_to', 'value']
        if 'email_log_pwd' in _config_df.index:
            _EMAIL_LOG_CREDENTIALS = (_EMAIL_LOG_FROM, _config_df.loc['email_log_pwd', 'value'])
            _EMAIL_LOG_SECURE = ()
    except FileNotFoundError:
        pass
    # set up logging formatter
    _formatter = _logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # set up log file handler
    _file_log_handler = _RotatingFileHandler(_os.path.join(_head, _sep, 'credit_analysis_app.log'),
                                             maxBytes=1024 * 1024 * 100, backupCount=20)
    _file_log_handler.setFormatter(_formatter)
    _file_log_handler.addFilter(_LogFilter())
    _file_log_handler.setLevel(_logging.DEBUG)
    # set up email handler
    _email_handler = _SMTPHandler(mailhost=_EMAIL_LOG_HOST,
                                  fromaddr=_EMAIL_LOG_FROM,
                                  toaddrs=[_EMAIL_LOG_TO],
                                  credentials=_EMAIL_LOG_CREDENTIALS,
                                  secure=_EMAIL_LOG_SECURE,
                                  subject='Credit Analysis App Exception')
    _email_handler.setFormatter(_formatter)
    _email_handler.addFilter(_LogFilter())
    _email_handler.setLevel(_logging.ERROR)
    # set up logging
    _app.logger.addHandler(_file_log_handler)
    _app.logger.addHandler(_email_handler)
    _logging.getLogger('werkzeug').addHandler(_file_log_handler)
    _logging.getLogger('werkzeug').addHandler(_email_handler)
