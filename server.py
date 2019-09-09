from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
from dashapp.util.show_docs import docs
from dashapp.api.yahoo.routes import yahoo
from dashapp.api.sel.banks.util.get_env import get_env
server = Flask(__name__,template_folder='./templates')

# Hide Selenium API for heroku
if get_env() not in ["production"]:
    from dashapp.api.sel.chrome_headless import sel
    server.register_blueprint(sel)

server.register_blueprint(docs)
server.register_blueprint(yahoo)

# Add auth eventually https://dash.plot.ly/authentication
from os import environ
# Only used for CI
if environ.get('DASH_SUPPRESS') is not None:
    app = Dash(server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
else:
    app = Dash(server=server,  external_stylesheets=[dbc.themes.BOOTSTRAP])