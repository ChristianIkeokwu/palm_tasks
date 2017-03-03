import src.models.projects.projects as project
import src.models.meetings.meetings as meeting
import src.models.tasks.tasks as tasks
from src.common.database import Database

Database.initialize()
project_reminders = project.Project.due_tommorow()
meetings_tommorow = meeting.Meeting.meetings_tommorow()
task_reminders = tasks.Task.due_tommorow()


for proj in project_reminders:
    print('project', proj.name, proj.date)

for meet in meetings_tommorow:
    print('meeting', meet.name, meet.date)

for meet in meeting.Meeting.next_week():
    print('meeting next week', meet.name, meet.date)


for task in task_reminders:
    print('task', task.name, task.date)