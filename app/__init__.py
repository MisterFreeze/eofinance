import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

def create_app(test_config=None):
    # create and configure the app
    kwargs = {}
    if test_config and 'instance_path' in test_config.keys():
      kwargs['instance_path'] = test_config['instance_path']
    app = Flask(__name__, instance_relative_config=True, **kwargs)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import main
    app.register_blueprint(main.bp)

    from . import budget
    app.register_blueprint(budget.bp, BUDGET_STORAGE_DIR = '{}/budgets'.format(app.instance_path))

    return app

def get_db(app):
  return SQLAlchemy(app)

def init_db():
  pass

app = create_app()
db = get_db(app)
