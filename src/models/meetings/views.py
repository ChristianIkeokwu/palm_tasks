import datetime
from flask import Blueprint, render_template, request, url_for, redirect, session
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.meetings.meetings import Meeting
from src.models.users.users import User
from src.models.reminder.notification import Event

meetings_blueprint = Blueprint('meetings', __name__)


@meetings_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))

@meetings_blueprint.route('/<string:meeting_id>')
def home(meeting_id):
    return render_template('meetings/home.html', meeting=Meeting.get_by_id(meeting_id))

@meetings_blueprint.route('/new', methods=['GET','POST'])
def new_meeting():
    if request.method == 'POST':
        name = request.form['name']
        date = ''.join(request.form['date'].split('/'))
        date += (request.form['hour'] + request.form['min'])
        date_time = datetime.datetime.strptime(date, '%d%m%Y%H%M')
        location = request.form['location']
        members = request.form['members'].split(',')
        members = [ User.get_by_email(member) for member in members ]
        objectives = request.form['objectives'].split('.')
        meeting = Meeting(name=name,date_time=date_time,caller=User.get_by_email(session['email']),members=members,location=location,objectives=objectives)
        meeting_notif = Event(event={'Meeting': meeting._id},
                        notify=[ member.email for member in members] + [meeting.caller.email],_id=meeting._id)
        meeting_notif.save_to_db()
        meeting.save_to_db()
        meeting_notif.meeting_created(meeting.caller.email)
        return redirect(url_for('.home', meeting_id=meeting._id))
    return render_template("meetings/new_meeting.html")



@meetings_blueprint.route('/<string:meeting_id>/new-objective', methods=['GET', "POST"])
def new_objective(meeting_id):
    if request.method == "POST":
        objective = request.form['objective']
        meeting = Meeting.get_by_id(meeting_id)
        meeting_notif = Event.get_by_id(meeting_id)
        meeting.objectives.append(objective)
        meeting.save_to_db()
        meeting_notif.meeting_added_objective(session['email'],objective)
        return redirect(url_for('.home',meeting_id=meeting_id))
    return render_template('meetings/new_objective.html', meeting=Meeting.get_by_id(meeting_id))


@meetings_blueprint.route('/<string:meeting_id>/new-member', methods=['GET', "POST"])
def new_member(meeting_id):
    if request.method == "POST":
        members = request.form['members'].split(',')
        meeting = Meeting.get_by_id(meeting_id)
        meeting_notif = Event.get_by_id(meeting_id)
        members = [ User.get_by_email(member) for member in members]
        meeting.members += members
        meeting_notif.meeting_added_member(session['email'], members)
        meeting.save_to_db()
        return redirect(url_for('.home',meeting_id=meeting_id))
    return render_template('meetings/new_member.html', meeting=Meeting.get_by_id(meeting_id))

@meetings_blueprint.route('/<string:meeting_id>/new-note', methods=['GET', "POST"])
def new_note(meeting_id):
    if request.method == "POST":
        meeting_note = request.form['meeting-note']
        meeting = Meeting.get_by_id(meeting_id)
        meeting.comments.append(meeting_note)
        Event.get_by_id(meeting_id).meeting_added_note(session['email'],meeting_note)
        meeting.save_to_db()
        return redirect(url_for('.home',meeting_id=meeting_id))
    return render_template('meetings/new_note.html', meeting=Meeting.get_by_id(meeting_id))