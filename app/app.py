import os
import flask
import conf
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Text
from forms import UploadForm


def create_app(config_file=None):
    app = flask.Flask('Dochap')
    app.secret_key = os.urandom(32)
    AppConfig(app,config_file)
    Bootstrap(app)
    create_views(app)
    create_api(app)
    create_nav(app)
    return app


def create_views(app):
    """
    Register views for the app
    """
    @app.route('/')
    def index():
        return flask.render_template('index.html')


    @app.route('/upload')
    def upload():
        form = UploadForm()
        return flask.render_template('upload.html',form=form)


    @app.route('/about')
    def about():
        return flask.render_template('about.html')


def create_api(app):
    """
    Register api routes for the app
    """
    @app.route('/api/1.0/gtf_upload')
    def api_gtf_upload():
        form = UploadForm()
        return 'success'

def create_nav(app):
    """
    Register navbar data, for calling in the html templates
    """
    nav = Nav(app)

    @nav.navigation()
    def basic_navbar():
        return Navbar(
            View('Dochap', 'index'),
            View('Upload', 'upload'),
            View('About', 'about'),
        )
    return nav

if __name__ == '__main__':
    print(conf.supported_species)
    app = create_app()
    app.run('0.0.0.0',debug=True,port=5555)
