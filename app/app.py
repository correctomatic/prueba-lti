import os, pprint, datetime
from tempfile import mkdtemp

# from questions import questions
# from dbmethods import drop_db_table, create_db_table, get_questions, get_question_by_id, insert_quiz_question, update_question, delete_question

from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from flask_caching import Cache

from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskMessageLaunch, FlaskRequest, FlaskCacheDataStorage
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.registration import Registration

class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app = Flask(__name__,
            static_url_path='',
            static_folder='./frontend/static',
            template_folder='./frontend/templates')

CORS(app, resources={r"/*": {"origins": "*"}})

app.wsgi_app = ReverseProxied(app.wsgi_app)

config = {
    "DEBUG": True,
    "ENV": "development",
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 600,
    "SECRET_KEY": "3dj90jdwi0d320edj9d",
    "SESSION_TYPE": "filesystem",
    "SESSION_FILE_DIR": mkdtemp(),
    "SESSION_COOKIE_NAME": "pylti1p3-flask-app-sessionid",
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SECURE": False,   # should be True in case of HTTPS usage (production)
    "SESSION_COOKIE_SAMESITE": None,  # should be 'None' in case of HTTPS usage (production)
    "DEBUG_TB_INTERCEPT_REDIRECTS": False
}
app.config.from_mapping(config)
cache = Cache(app)


def get_lti_config_path():
    return os.path.join(app.root_path, 'configs', 'reactquiz.json')

def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)

def get_jwk_from_public_key(key_name):
    key_path = os.path.join(app.root_path, '..', 'configs', key_name)
    f = open(key_path, 'r')
    key_content = f.read()
    jwk = Registration.get_jwk(key_content)
    f.close()
    return jwk

if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run()
