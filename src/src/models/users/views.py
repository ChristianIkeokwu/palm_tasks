from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for,session
from src.models.reminder.notification import Notification
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.users.users import User
from src.models.reminder.notification import Event

user_blueprint = Blueprint('users', __name__)

@user_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))

@user_blueprint.context_processor
def notifications():
    return dict(notifications=Notification.get_by_email(session['email']))

@user_blueprint.route('/<string:user_id>')
def view(user_id):
    return render_template('users/profile.html', staff=User.get_by_id(user_id))



@user_blueprint.route('/')
@user_decorators.requires_login
def home():
    #user = User.get_by_email(session['email'])
    return render_template('users/dashboard.html',)


@user_blueprint.route('/profile')
@user_decorators.requires_login
def view_profile():
    return render_template('users/account.html', user=User.get_by_email(session['email']))


@user_blueprint.route('/profile/edit',methods=['GET','POST'])
@user_decorators.requires_login
def edit_profile():
    pass

@user_blueprint.route('view/<string:user_id>')
#@user_decorators.requires_department_head TODO fix department head permissions
def view_user():
    pass # TODO requires_department_head should work for events also



@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('login'))