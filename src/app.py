import jinja2
from flask import Flask, session
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.models.projects.projects import Project
from src.models.reminder.notification import Notification
from src.models.users.users import User
from src.models.meetings.meetings import Meeting

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(['templates', 'templates/users', 'templates/meetings', 'templates/projects', 'templates/tasks', 'templates/department'])
)

app = Flask(__name__)
app.secret_key = "123"


from src.models.users.views import user_blueprint
from src.models.projects.views import projects_blueprint
from src.models.meetings.views import meetings_blueprint
from src.models.tasks.views import tasks_blueprint
from src.models.department.views import department_blueprint
app.register_blueprint(department_blueprint, url_prefix="/department")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(projects_blueprint, url_prefix="/projects")
app.register_blueprint(meetings_blueprint, url_prefix="/meetings")
app.register_blueprint(tasks_blueprint, url_prefix="/tasks")


@app.context_processor
def meeting_class():
    return dict(Meeting=Meeting)

@app.context_processor
def project_class():
    return dict(Project=Project)

@app.context_processor
def priority_list():
    return dict(priority_list=['Low','Normal','High','Critical'])

@app.context_processor
def notifications():
    if session.get('email'):
        return dict(notifications=Notification.get_by_email(session['email']))
    else:
        return dict(notifications=[])



@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    if session.get('email'):
        return render_template('home.html', user=User.get_by_email(session['email']) )
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for("users.home"))
        except UserErrors.UserError as e:
            return render_template("login.html", error=e.message)
    return render_template("login.html")  # Send the user an error if their login was invalid


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department =  request.form['department']

        try:
            if User.register_user(email, password,title, first_name,last_name,department):
                session['email'] = email
                return redirect(url_for("users.home"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("register.html")  # Send the user an error if their login was invalid


@app.route('/our_mission')
def our_mission():
    return render_template('our_mission.html')


@app.route('/our_team')
def our_team():
    return render_template('our_team.html')








if __name__ == "__main__":
    app.run(debug=True, port=8000)


