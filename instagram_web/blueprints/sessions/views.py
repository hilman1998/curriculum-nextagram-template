from flask import Flask,Blueprint,render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user, logout_user, login_required
from instagram_web.util.google_oauth import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    username=request.form.get('user_name')
    password=request.form.get('password')

    username_object=User.get_or_none(User.name==username)
    if username_object:   
        if check_password_hash(username_object.password_hash,password):
            flash ("yay you signed in")
            login_user(username_object)
            return redirect(url_for('users.show', username=username_object.name))
        else:
            flash("budu la kau")
            return redirect(url_for('sessions.new'))

    else:
        return "no username found"

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    # remove user info from browser session
    # session.pop('user_id', None)
    logout_user()
    flash("Logout success!","primary")
    return redirect(url_for("sessions.new"))    

    # user_list=User.select()
    # for user in user_list:
    #     if user.name == username:
    #         if check_password_hash(user.password_hash, password):
    #             return "nice"
    #         else:
    #             return "pahal ni"

@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

