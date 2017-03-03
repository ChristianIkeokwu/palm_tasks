import datetime
import uuid

import src.models.users.users as users
from src.common.database import Database
from src.models.projects.projects import Project
from src.models.tasks.tasks import Task
from src.models.meetings.meetings import Meeting


class Notification(object):
    def __init__(self,creator,action,_event,_id=None,notify=None,time=None,summary=None, read=False):
        self.creator = users.User.get_by_email(creator)
        self.notify = users.User.get_by_email(notify)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.action = action
        self._event = _event
        self.read = read
        self.time = datetime.datetime.utcnow() if time is None else time
        self.summary = summary[0:40] if summary else summary
        self.event = ''
        for elem in _event:
            id = _event[elem]
            statement = "{}.get_by_id('{}')".format(elem, id)
            self.event = eval(statement)

    def check(self):
        self.read = True
        self.save_to_db()


    def json(self):
        return {
            "read" : self.read,
            "creator": self.creator.email,
            "action": self.action,
            "_event": self._event,
            "time" : self.time,
            "summary": self.summary,
            "notify": self.notify.email,
            "_id": self._id
        }
    def __repr__(self):
        return str(self.json())

    def __lt__(self, other):
        return other.time < self.time

    def save_to_db(self):
        Database.update('notifications',{"_id": self._id}, self.json())

    @staticmethod
    def get_by_email(email):
        notifications = []
        for notif in Database.find('notifications', {"notify": email}):
            notifications.append(Notification(**notif))

        notifications.sort()
        return notifications

    @staticmethod
    def get_by_id(_id):
        try:
            notif = Database.find_one('notifications', {"_id": _id})
            return Notification(**notif)
        except Exception:
            return None



    @staticmethod
    def get_read_by_email(email):
        notifications = []
        for notif in Database.find('notifications', {"notify": email}):
            notif = Notification(**notif)
            if not notif.read:
                notifications.append(notif)
        notifications.sort()
        return notifications

# Project Notifications


class Event(object):
    def __init__(self, event,notify,_id):
        self._id = _id
        self.event = event
        self.notify = notify

    def save_to_db(self):
        Database.insert('events', self.json())

    @staticmethod
    def get_by_id(_id):
        return Event(**Database.find_one("events", {"_id": _id}))

    def json(self):
        return {
        "event": self.event,
        "notify": self.notify,
        "_id": self._id
        }



    def project_created(self, creator):
        """
        event: is a dictionary of event cls and _id
        person: person _id
        """
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "created the project", self.event, notify=person)
                notif.save_to_db()



    def project_task_added(self, creator):
        """
        summary: is the name of the task
        """
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "added a task to the project", self.event, notify=person)
                notif.save_to_db()



    def project_note_added(self,creator, summary):  # Alert everyone in list except maker
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "added a note to the project", self.event, summary=summary, notify=person)
                notif.save_to_db()



    def project_completed(self,creator):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "has completed the project", self.event, notify=person)
                notif.save_to_db()


    # Task Notifications

    def task_note_added(self,creator, summary):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "added a note to the task", self.event, summary=summary, notify=person)
                notif.save_to_db()


    def task_completed(self, creator):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "completed the task", self.event, notify=person)
                notif.save_to_db()


    def task_priority_changed(self,creator):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "changed the priority of", self.event, notify=person)
                notif.save_to_db()


    def task_rated(self,creator, summary):
        summary = 'Task now rated at {}'.format(summary)
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "rated the task", self.event, summary=summary, notify=person)
                notif.save_to_db()


    # Meeting Notifications

    def meeting_created(self,creator):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "created the meeting", self.event, notify=person)
                notif.save_to_db()


    def meeting_added_member(self,creator, summary):
        summary = 'added {} to the meeting'.format(summary)
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "added someone to the meeting", self.event, summary=summary, notify=person)
                notif.save_to_db()


    def meeting_added_note(self,creator,summary):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "added a note to the meeting", self.event, summary=summary, notify=person)
                notif.save_to_db()


    def meeting_added_objective(self,creator, summary):
        for person in self.notify:
            if person != creator:
                notif = Notification(creator, "updated the meeting objectives", self.event, summary=summary, notify=person)
                notif.save_to_db()

            #notif.save_to_db()


if __name__ == "__main__":
    creator = 'chris_ikeokwu@gmail.com'

    event = Event({'Project': "95d3c34f4e91422b9f86e225ec1eae3b"},['test@test.com','test2@test.com','chris_ikeokwu@gmail.com'])
    event.project_completed(creator)
    event.project_created(creator)
    event.project_note_added(creator,'this are some damn notes my mehn')
    event.meeting_added_member(creator,users.User.get_by_email(creator))
    event.meeting_added_objective(creator,'do some good stuff')

    print(Notification.get_by_email('test@test.com'))