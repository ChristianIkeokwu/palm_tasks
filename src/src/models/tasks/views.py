import datetime
from flask import Blueprint, render_template, request, url_for, redirect, session
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.tasks.tasks import Task
from src.models.users.users import User
from src.models.projects.projects import Project
from src.models.reminder.notification import Event

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))


@tasks_blueprint.route('/<string:task_id>')
def home(task_id):
    return render_template('tasks/home.html', task=Task.get_by_id(task_id))


@tasks_blueprint.route('/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        name = request.form['name']
        date = ''.join(request.form['due_date'].split('/'))
        due_date = datetime.datetime.strptime(date, '%d%m%Y')
        project = request.form['project']
        priority = int(request.form['priority'])
        owner = session['email']
        task = Task(name=name, owner=owner, project=project, due_date=due_date, priority=priority)
        task_notif = Event({'Task': task._id},notify=[session['email']],_id=task._id)
        task_notif.save_to_db()
        project = Project.get_by_id(project)
        project.add_task(task._id)
        Event.get_by_id(project._id).project_task_added(session['email'])
        return redirect(url_for('.home', task_id=task._id))
    return render_template('/tasks/new_task.html')


@tasks_blueprint.route('/edit/<string:task_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_task(task_id):
    pass


@tasks_blueprint.route('/<string:task_id>/new-note' ,methods=['GET', 'POST'])
def new_note(task_id):
    if request.method == 'POST':
        task_note = request.form['task-note']
        Task.get_by_id(task_id).add_comment(task_note)
        Event.get_by_id(task_id).task_note_added(session['email'],task_note)
        return redirect(url_for('.home', task_id=task_id))
    return render_template('tasks/task_new_note.html', task=Task.get_by_id(task_id))


@tasks_blueprint.route('<string:task_id>/complete')
def complete_task(task_id):
    task = Task.get_by_id(task_id)
    task.end_task()
    Event.get_by_id(task_id).task_completed(session['email'])
    task.save_to_db()
    return redirect(url_for('projects.home', project_id=task.project))
