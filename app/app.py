import os, pprint, datetime
from jwcrypto import jwk
from tempfile import mkdtemp


# from questions import questions
# from dbmethods import drop_db_table, create_db_table, get_questions, get_question_by_id, insert_quiz_question, update_question, delete_question

from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from flask_caching import Cache

from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect
from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.registration import Registration


class ReverseProxied:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get("HTTP_X_FORWARDED_PROTO")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


app = Flask(
    __name__,
    static_url_path="",
    static_folder="./static",
    template_folder="./templates",
)

CORS(app, resources={r"/*": {"origins": "*"}})

# app.wsgi_app = ReverseProxied(app.wsgi_app)

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
    "SESSION_COOKIE_SECURE": False,  # should be True in case of HTTPS usage (production)
    "SESSION_COOKIE_SAMESITE": None,  # should be 'None' in case of HTTPS usage (production)
    "DEBUG_TB_INTERCEPT_REDIRECTS": False,
}
app.config.from_mapping(config)
cache = Cache(app)


def get_lti_config_path():
    return os.path.join(app.root_path, "configs", "reactquiz.json")


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


def get_jwk_from_public_key(key_name):
    key_path = os.path.join(app.root_path, "..", "configs", key_name)
    f = open(key_path, "r")
    key_content = f.read()
    jwk = Registration.get_jwk(key_content)
    f.close()
    return jwk


###############################################################
# LTI-related routes
###############################################################
@app.route("/login/", methods=["GET", "POST"])
def login():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    launch_data_storage = get_launch_data_storage()
    flask_request = FlaskRequest()

    target_link_uri = flask_request.get_param("target_link_uri")
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(
        flask_request, tool_conf, launch_data_storage=launch_data_storage
    )

    return oidc_login.enable_check_cookies().redirect(target_link_uri)


@app.route("/launch_old", methods=["POST"])
def launch_old():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = FlaskMessageLaunch(
        request, tool_conf, launch_data_storage=launch_data_storage
    )

    message_launch_data = message_launch.get_launch_data()
    # pprint.pprint(message_launch_data)

    tpl_kwargs = {
        "page_title": "LTI 1.3 Flask App",
        "is_deep_link_launch": message_launch.is_deep_link_launch(),
        "launch_data": message_launch.get_launch_data(),
        "launch_id": message_launch.get_launch_id(),
        "curr_user_name": message_launch_data.get("name", ""),
    }
    return render_template("index.html", **tpl_kwargs)


class ExtendedFlaskMessageLaunch(FlaskMessageLaunch):

    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce validation.

        """
        iss = self.get_iss()
        deep_link_launch = self.is_deep_link_launch()
        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super().validate_nonce()

def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


def get_jwk_from_public_key(key_name):
    key_path = os.path.join(app.root_path, '..', 'configs', key_name)
    f = open(key_path, 'r')
    key_content = f.read()
    jwk = Registration.get_jwk(key_content)
    f.close()
    return jwk

PAGE_TITLE = 'Game Example'

@app.route('/launch', methods=['POST'])
def launch():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch(flask_request, tool_conf, launch_data_storage=launch_data_storage)
    message_launch_data = message_launch.get_launch_data()
    pprint.pprint(message_launch_data)

    difficulty = message_launch_data.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}) \
        .get('difficulty', None)
    if not difficulty:
        difficulty = request.args.get('difficulty', 'normal')

    tpl_kwargs = {
        'page_title': PAGE_TITLE,
        'is_deep_link_launch': message_launch.is_deep_link_launch(),
        'launch_data': message_launch.get_launch_data(),
        'launch_id': message_launch.get_launch_id(),
        'curr_user_name': message_launch_data.get('name', ''),
        'curr_diff': difficulty
    }
    return render_template('game.html', **tpl_kwargs)


@app.route('/configure/<launch_id>/<difficulty>/', methods=['GET', 'POST'])
def configure(launch_id, difficulty):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                           launch_data_storage=launch_data_storage)

    if not message_launch.is_deep_link_launch():
        raise Forbidden('Must be a deep link!')

    launch_url = url_for('launch', _external=True)

    resource = DeepLinkResource()
    resource.set_url(launch_url + '?difficulty=' + difficulty) \
        .set_custom_params({'difficulty': difficulty}) \
        .set_title('Breakout ' + difficulty + ' mode!')

    html = message_launch.get_deep_link().output_response_form([resource])
    return html

@app.route('/api/score/<launch_id>/<earned_score>/<time_spent>/', methods=['POST'])
def score(launch_id, earned_score, time_spent):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                           launch_data_storage=launch_data_storage)

    resource_link_id = message_launch.get_launch_data() \
        .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')

    if not message_launch.has_ags():
        raise Forbidden("Don't have grades!")

    sub = message_launch.get_launch_data().get('sub')
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    earned_score = int(earned_score)
    time_spent = int(time_spent)

    grades = message_launch.get_ags()
    sc = Grade()
    sc.set_score_given(earned_score) \
        .set_score_maximum(100) \
        .set_timestamp(timestamp) \
        .set_activity_progress('Completed') \
        .set_grading_progress('FullyGraded') \
        .set_user_id(sub)

    sc_line_item = LineItem()
    sc_line_item.set_tag('score') \
        .set_score_maximum(100) \
        .set_label('Score')
    if resource_link_id:
        sc_line_item.set_resource_id(resource_link_id)

    grades.put_grade(sc, sc_line_item)

    tm = Grade()
    tm.set_score_given(time_spent) \
        .set_score_maximum(999) \
        .set_timestamp(timestamp) \
        .set_activity_progress('Completed') \
        .set_grading_progress('FullyGraded') \
        .set_user_id(sub)

    tm_line_item = LineItem()
    tm_line_item.set_tag('time') \
        .set_score_maximum(999) \
        .set_label('Time Taken')
    if resource_link_id:
        tm_line_item.set_resource_id(resource_link_id)

    result = grades.put_grade(tm, tm_line_item)

    return jsonify({'success': True, 'result': result.get('body')})


@app.route('/api/scoreboard/<launch_id>/', methods=['GET', 'POST'])
def scoreboard(launch_id):
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch.from_cache(launch_id, flask_request, tool_conf,
                                                           launch_data_storage=launch_data_storage)

    resource_link_id = message_launch.get_launch_data() \
        .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')

    if not message_launch.has_nrps():
        raise Forbidden("Don't have names and roles!")

    if not message_launch.has_ags():
        raise Forbidden("Don't have grades!")

    ags = message_launch.get_ags()

    if ags.can_create_lineitem():
        score_line_item = LineItem()
        score_line_item.set_tag('score') \
            .set_score_maximum(100) \
            .set_label('Score')
        if resource_link_id:
            score_line_item.set_resource_id(resource_link_id)

        score_line_item = ags.find_or_create_lineitem(score_line_item)
        scores = ags.get_grades(score_line_item)

        time_line_item = LineItem()
        time_line_item.set_tag('time') \
            .set_score_maximum(999) \
            .set_label('Time Taken')
        if resource_link_id:
            time_line_item.set_resource_id(resource_link_id)

        time_line_item = ags.find_or_create_lineitem(time_line_item)
        times = ags.get_grades(time_line_item)
    else:
        scores = ags.get_grades()
        times = None

    members = message_launch.get_nrps().get_members()
    scoreboard_result = []

    for sc in scores:
        result = {'score': sc['resultScore']}
        for tm in times:
            if tm['userId'] == sc['userId']:
                result['time'] = tm['resultScore']
                break
        for member in members:
            if member['user_id'] == sc['userId']:
                result['name'] = member.get('name', 'Unknown')
                break
        scoreboard_result.append(result)

    return jsonify(scoreboard_result)


"""
In the context of LTI (Learning Tools Interoperability) 1.3,
the scopes section in the /config endpoint results defines the permissions that the tool is requesting from the platform
(such as Moodle). These scopes specify the access rights the tool needs to perform various operations.

(En principio esto no lo uso)
"""


@app.route("/config", methods=["GET"])
def config():
    tool_configuration = {
        "title": "Flask LTI 1.3 Tool",
        "scopes": [
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",  # This scope allows the tool to create and manage line items, which represent columns in the gradebook.
            "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",  # This scope grants the tool permission to read the results (grades or scores) associated with a line item. The tool cannot modify the results with this scope.
            "https://purl.imsglobal.org/spec/lti-ags/scope/score",  # This scope allows the tool to submit scores to the platform. This is often used to update student grades based on their performance in the tool.
        ],
        "extensions": [
            {
                "platform": "moodle",
                "settings": {
                    "placements": ["course_navigation", "resource_selection"],
                    "icon_url": "https://example.com/icon.png",
                    "secure_icon_url": "https://example.com/icon.png",
                },
            }
        ],
        "public_jwk_url": "https://your-domain.com/jwks",
        "redirect_uris": ["https://your-domain.com/lti/launch"],
        "custom_fields": {"field1": "$Context.id", "field2": "$ResourceLink.id"},
    }
    return jsonify(tool_configuration)


@app.route("/jwks", methods=["GET"])
def jwks():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    public_key_path = os.path.join(__location__, "configs", "public.key")

    with open(public_key_path, "rb") as public_key_file:
        public_key = public_key_file.read()

    key = jwk.JWK.from_pem(public_key)
    jwk_data = key.export(as_dict=True)
    jwks = {"keys": [jwk_data]}
    return jsonify(jwks)


if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # Remote debugging with VS Code
    # -------------------------------------------------------------------------
    import debugpy

    debugger_attached_env_var = "DEBUGGER_ATTACHED"
    # Check if the debugger is not already attached
    if os.getenv(debugger_attached_env_var) != "1":
        debugpy.listen(("0.0.0.0", 5678))
        # No need to wait for the debugger to attach if you don't need to
        # debug until the first request
        # print("Waiting for debugger attach...")
        # debugpy.wait_for_client()

        # Set the environment variable to indicate debugger attachment
        os.environ[debugger_attached_env_var] = "1"
    # -------------------------------------------------------------------------

    try:
        print(app.template_folder)
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
    # The exception is for avoiding pausing the debugger when the app reloads
    except SystemExit as e:
        pass
