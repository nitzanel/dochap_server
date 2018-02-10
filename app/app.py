import utils
import conf
import compare_gen
import os
import flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Text
from flaskext.markdown import Markdown
from forms import UploadForm
from jinja2 import Environment, FileSystemLoader
# dochap tool

def create_app(config_file=None):
    app = flask.Flask('Dochap')
    app.secret_key = os.urandom(32)
    AppConfig(app,config_file)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    Bootstrap(app)
    Markdown(app)
    create_views(app)
    create_api(app)
    create_nav(app)
    return app



def create_views(app):
    """
    Register views for the app
    """
    @app.route('/dochap/')
    def index():
        response = flask.redirect(flask.url_for('upload'))
        return response


    @app.route('/dochap/upload')
    def upload():
        form = UploadForm()
        return flask.render_template('upload.html',form=form)


    @app.route('/dochap/about')
    def about():
        about_text = ""
        with open('./templates/markdown/about.md', 'r') as f:
            about_text = f.read()
        return flask.render_template('about.html', about_text=about_text)


def create_api(app):
    """
    Register api routes for the app
    """
    @app.route('/dochap/api/1.0/gtf_upload',methods=['POST'])
    def api_gtf_upload():
        form = UploadForm()
        save_path = '/tmp/uploaded_gtf'
        form.gtf_file.data.save(save_path)
        user_transcripts = utils.parse_gtf_file(save_path)
        os.remove(save_path)
        specie = form.specie_selection.data
        genes = form.genes_selection.data
        genes = list(set(genes.split(',')))
        flask_response = compare_gen.create_html_pack_better(
                user_transcripts,
                specie,
                genes,
                conf.running_local,
                conf.local_save_dir,
                conf.compare_filename
                )
        return flask_response


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
    app = create_app()
    app.run('0.0.0.0', debug=False, threaded=True, port=5001)
