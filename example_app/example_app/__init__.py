from flask import Flask
app = Flask(__name__)
app.config.from_envvar('EXAMPLE_APP_CONFIG')

import example_app.views
