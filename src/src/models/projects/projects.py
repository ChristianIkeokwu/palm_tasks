import uuid
import datetime
from src.common.database import Database
from src.models.tasks.tasks import Task
import src.common.CONSTANTS as constants


class Project(object):
    def __init__(self, name, owner, tasks=[], _id=None, due_date=None, date=None, done=False, comments=[],priority=1):
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id
        self.due_date = due_date
        self.date = due_date if date is None else date
        self.owner = owner
        self.tasks = tasks
        self.done = done
        self.priority = priority
        self.comments = comments

    def url(self):
        return constants.url + r'projects/' + self._id
    def save_to_db(self):
        Database.update('projects', {"_id": self._id}, self.json())

    def __lt__(self, other):
        return other.date < self.date

    def __eq__(self, other):
        return self._id == other._id

    @classmethod
    def due_tommorow(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        now = datetime.datetime.utcnow()
        return sorted([cls(**elem) for elem in Database.find('projects',
                                                      {"date":
                                                           {"$gte": now,
                                                            "$lte": day_upper},
                                                       "done": False
                                                       })])

    @classmethod
    def next_week(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
        now = datetime.datetime.utcnow()
        return sorted([cls(**elem) for elem in Database.find('projects',
                                                             {"date":
                                                                  {"$gte": now,
                                                                   "$lte": day_upper},
                                                              "done": False
                                                              })])
    def json(self):
        return {
            "name": self.name,
            "_id": self._id,
            "owner": self.owner,
            "due_date": self.due_date,
            "date": self.date,
            "tasks": self.tasks,
            "done": self.done,
            "priority": self.priority,
            "comments": self.comments
        }
    def all_tasks(self):
        all_tasks = []
        for _id in self.tasks:
            all_tasks.append(Task.get_by_id(_id))
        return all_tasks

    def all_active_tasks(self):
        all_tasks = []
        for _id in self.tasks:
            if not Task.get_by_id(_id).done:
                all_tasks.append(Task.get_by_id(_id))
        return all_tasks

    def progress(self):
        all_tasks = self.all_tasks()
        finished = 0
        for task in all_tasks:
            if task.done:
                finished += 1
        try:
            progress = (finished / len(all_tasks)) * 100
            return int(progress)
        except ZeroDivisionError:
            progress = 0
            return int(progress)

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('projects',{})]

    @staticmethod
    def get_by_owner(owner_email):
        return Project(**Database.find("projects", {"email": owner_email}))

    @staticmethod
    def get_by_id(_id):
        return Project(**Database.find_one("projects", {"_id": _id}))

    @staticmethod
    def get_by_date(date):
        return Project(**Database.find("projects", {"due_date": date}))

    def end_project(self):
        self.done = True
        self.save_to_db()

    def set_priority(self, priority):
        self.priority = priority
        self.save_to_db()

    def add_task(self, task_id):
        self.tasks.append(task_id)
        self.save_to_db()

    def add_comment(self, comment):
        self.comments.append(comment)
        self.save_to_db()

if __name__ == "__main__":
    project = Project("Run Marketing Campaign at 10 schools","test@test.com",tasks=[],due_date=datetime.datetime.utcnow(),
                        comments=["this is a test projects for testing sake"],  priority=3)
    Database.initialize()
    project.save_to_db()