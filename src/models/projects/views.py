import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for,redirect,session
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.projects.projects import Project
from src.models.users.users import User
from src.models.reminder.notification import Event

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))



@projects_blueprint.route('/<string:project_id>')
def home(project_id):
    return render_template('projects/home.html', project=Project.get_by_id(project_id))

@projects_blueprint.route('/new', methods=['GET','POST'])
def new_project():
    if request.method == 'POST':
        name = request.form['name']
        date = ''.join(request.form['due_date'].split('/'))
        due_date = datetime.datetime.strptime(date, '%d%m%Y')
        priority = int(request.form['priority'])
        owner = session['email']
        project = Project(name=name, owner=owner, due_date=due_date, priority=priority)
        project_notif = Event({'Project':project._id},notify=[owner], _id=project._id)
        project.save_to_db()
        project_notif.save_to_db()
        user = User.get_by_email(session['email'])
        user.projects.append(project._id)
        user.save_to_db()

        return redirect(url_for('.home', project_id=project._id))
    return render_template('projects/new_project.html')

@projects_blueprint.route('/<string:project_id>/new-note', methods=['GET', 'POST'])
def new_note(project_id):
    if request.method == 'POST':
        project_note = request.form['project-note']
        Project.get_by_id(project_id).add_comment(project_note)
        Event.get_by_id(project_id).project_note_added(session['email'], project_note)
        return redirect(url_for('.home',project_id=project_id))
    return render_template('projects/new_note.html',project=Project.get_by_id(project_id))

@projects_blueprint.route('/<string:project_id>/new-task', methods=['GET', 'POST'])
def new_task(project_id):
    Event.get_by_id(project_id).project_task_added(session['email'])
    return render_template('projects/project_new_task.html',project=Project.get_by_id(project_id))


@projects_blueprint.route('/edit/<string:project_id>',methods=['GET','POST'])
def edit_project(project_id):
    pass