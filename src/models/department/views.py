from flask import  Blueprint,session, render_template
from src.models.department import department
from src.models.users.users import User

department_blueprint = Blueprint('department', __name__ )

@department_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))

@department_blueprint.route("/<string:department_id>")
def home(department_id):
    return render_template("department/home.html", department=department.Department.get_by_id(department_id))