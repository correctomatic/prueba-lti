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


###############################################################
# LTI-related routes
###############################################################
@app.route('/login/', methods=['GET', 'POST'])
def login():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    launch_data_storage = get_launch_data_storage()
    flask_request = FlaskRequest()

    target_link_uri = flask_request.get_param('target_link_uri')
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        flask_request,
        tool_conf,
        launch_data_storage=launch_data_storage
    )

    return oidc_login\
        .enable_check_cookies()\
        .redirect(target_link_uri)

@app.route('/launch/', methods=['POST'])
def launch():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch(
        request,
        tool_conf,
        launch_data_storage=launch_data_storage
    )
    message_launch_data = message_launch.get_launch_data()
    #pprint.pprint(message_launch_data)

    tpl_kwargs = {
        'page_title': 'LTI 1.3 Flask App',
        'is_deep_link_launch': message_launch.is_deep_link_launch(),
        'launch_data': message_launch.get_launch_data(),
        'launch_id': message_launch.get_launch_id(),
        'curr_user_name': message_launch_data.get('name', ''),
    }
    return render_template('index.html', **tpl_kwargs)

if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run()
