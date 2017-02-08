import uuid
import datetime
from src.common.database import Database
import src.common.CONSTANTS as constants
#from src.models.projects.projects import Project
#from src.models.users.users import User


class Task(object):
    def __init__(self, name, owner, project=None, _id=None, due_date=None, date=None, done=False,priority=1, comments=[],rating=0):
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id
        self.due_date = due_date # parsing the string to generate a datetime object
        self.date = due_date if date is None else date
        self.owner = owner
        self.project = project
        self.done = done
        self.priority = priority
        self.comments = comments
        self.rating = rating
        self.save_to_db()

    def save_to_db(self):
        Database.update('tasks', {"_id": self._id}, self.json())

    def url(self):
        return constants.url + r'tasks/' + self._id

    def __lt__(self, other):
        return other.date < self.date

    def __eq__(self, other):
        return self._id == other._id

    @classmethod
    def due_tommorow(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        now = datetime.datetime.utcnow()
        return sorted([cls(**elem) for elem in Database.find('tasks',
                                                      {"date":
                                                           {"$gte": now,
                                                            "$lte": day_upper},
                                                       "done": False
                                                       })])

    @classmethod
    def next_week(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
        now = datetime.datetime.utcnow()
        return sorted([cls(**elem) for elem in Database.find('tasks',
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
            "project": self.project,
            "done": self.done,
            "priority": self.priority,
            "comments": self.comments,
            "rating" : self.rating
        }

    @staticmethod
    def get_by_owner(owner_email):
        return Task(**Database.find("tasks", {"email": owner_email}))

    @staticmethod
    def get_by_id(_id):
        return Task(**Database.find_one("tasks", {"_id": _id}))

    @staticmethod
    def get_by_date(date):
        return Task(**Database.find("tasks", {"due_date": date}))

    @staticmethod
    def get_by_project():
        pass

    def end_task(self):
        self.done = True
        self.save_to_db()

    def add_comment(self, comment):
        self.comments.append(comment)
        self.save_to_db()


# if __name__ == "__main__":
#     Database.initialize()
#     user = User.get_by_email('test@test.com')
#     for project in user.projects:
#         projects = Project.get_by_id(project)
#         projects.tasks = []
#         for num in range(5):
#             task = Task(
#                 name= 'Test Task {}'.format(num),
#                 owner= "test@test.com",
#                 project=projects._id,
#                 due_date=datetime.datetime.utcnow() + datetime.timedelta(days=1),
#                 priority= num%3 + 1,
#                 comments=['this is a test comment for test task{}'.format(num)]
#             )
#             projects.add_task(task._id)
#
#     user.save_to_db()
