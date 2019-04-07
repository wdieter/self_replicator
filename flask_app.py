from flask import Flask, redirect, request, url_for, render_template
from rauth import OAuth2Service
import os

application = Flask(__name__)

client_id = os.getenv("GITHUB_CLIENT_ID")
client_secret = os.getenv("GITHUB_CLIENT_SECRET")
app_secret_key = os.getenv("APP_SECRET_KEY", "super_secret")

application.secret_key = app_secret_key
base_api_url = "https://api.github.com/"

service = OAuth2Service(
    name='github_replicator',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    base_url=base_api_url)


@application.route('/')
def hello():
    return render_template('index.html')


@application.route('/auth')
def get_github_user_code():
    """Step 1 of OAuth2 authentication flow
    Requests made to this page are redirected to the github oauth authorization url
    """
    authorization_params = dict(client_id=client_id,
                                redirect_uri=get_full_url(request, code_for_session),
                                scope='public_repo')
    url = service.get_authorize_url(**authorization_params)
    return redirect(url)


@application.route('/callback')
def code_for_session():
    """Step 2 of OAuth2 authentication flow
    Once user grants the app permission to access their github account, github will redirect here.
    service.get_auth_session exchanges the code given in the url parameters for an access token
    The session variable stores the access token used to call github api
    Finally, create_repo is called"""
    session = service.get_auth_session(data=dict(code=request.args.get("code"),
                                                 redirect_uri=get_full_url(request, code_for_session))
                                       )
    create_repo(session)
    user_url = get_user_profile(session)
    return render_template('post_fork.html', user_url=user_url)


# Flask utility function #

def get_full_url(flask_request, endpoint):
    """Creates callback url based on context of the request.
    making callback url dynamic allows for easier migration to production"""
    url_root = flask_request.url_root[:-1]  # removing trailing '/'
    callback_endpoint = url_for(endpoint.__name__)
    return ''.join([url_root, callback_endpoint])


# Github api functions #

def get_user_profile(session):
    """returns the profile url for the authenticated user"""
    response_json = session.get(base_api_url + "user").json()
    user_url = response_json['html_url']
    return user_url


def create_repo(session):
    """forks the repository to the user's github using the authenticated session"""
    repo_name = 'self_replicator'
    repo_owner = 'wdieter'
    api_base_minus_slash = base_api_url[:-1]
    post_fork_url = '/'.join((api_base_minus_slash, 'repos', repo_owner, repo_name, 'forks'))
    # post_fork_url should look like "https://api.github.com/repos/wdieter/self_replicator/forks"
    response = session.post(post_fork_url)
    return response.text


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)
