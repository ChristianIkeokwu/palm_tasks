import uuid
import datetime
from src.common.database import Database
import src.models.users.users2 as user
import src.common.CONSTANTS as constants

class Meeting(object):
    def __init__(self, name, location, caller, members=[], _id=None, date_time=None,date=None, done=False, objectives=[],
                 comments=[]):
        self.name = name
        self._id = uuid.uuid4().hex if _id is None else _id
        self.location = location
        self.date_time = date_time
        self.date = date_time if date is None else date
        self.caller = user.User(**caller) if type(caller) == dict else caller
        self.members = [user.User(**member) if type(member) == dict else member for member in members ] if members else []
        self.done = done
        self.objectives = objectives
        self.comments = comments  # TODO comments on meetings would notify all members

    def url(self):
        return constants.url + r'meetings/' + self._id

    def __lt__(self, other):
        return   self.date < other.date

    def __eq__(self, other):
        return self._id == other._id

    def save_to_db(self):
        # TODO fix meetings saving to everyone in the database
        Database.initialize()
        Database.update('meetings', {"_id": self._id}, self.json())
        for member in self.members:
            member.add_meeting(self._id)
        self.caller.add_meeting(self._id)

    def json(self):
        return {
            "name": self.name,
            "date_time": self.date_time,
            "date": self.date,
            "_id": self._id,
            "location": self.location,
            "caller": self.caller.json(),
            "members": [member.json() for member in self.members],
            "done": self.done,
            "comments" : self.comments,
            "objectives": self.objectives
        }

    @staticmethod
    def get_by_caller(caller_email):
        return Meeting(**Database.find("meetings", {"email": caller_email}))

    @staticmethod
    def get_by_id(_id):
            return Meeting(**Database.find_one("meetings", {"_id": _id}))

    @staticmethod
    def get_by_date(date):
        return Meeting(**Database.find("meetings", {"date": date}))

    @classmethod
    def meetings_tommorow(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        now = datetime.datetime.utcnow()
        return [cls(**elem) for elem in Database.find('meetings',
                                                      {"date":
                                                           {"$gte": now,
                                                            "$lte" : day_upper},
                                                       "done": False
                                                       })]

    @classmethod
    def next_week(cls):
        day_upper = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
        now = datetime.datetime.utcnow()
        return sorted([cls(**elem) for elem in Database.find('meetings',
                                                             {"date":
                                                                  {"$gte": now,
                                                                   "$lte": day_upper},
                                                              "done": False
                                                              })])
    def end_meeting(self):
        self.done = True
        self.save_to_db()


if __name__ == "__main__":
    test_meeting = Meeting("YouRhapsody Planning",
                           "online",
                           user.User.get_by_email("test@test.com"),
                           members=[user.User.get_by_email("test2@test.com"),
                                    user.User.get_by_email("chris_ikeokwu@gmail.com"),
                                    user.User.get_by_email("mybabeisthebest@yahoo.com")
                                    ],
                           _id="6ffc2a7ede12446181024e49f17fbc78",
                           date_time=datetime.datetime.utcnow(),
                           comments=['this is the test comment for this meeting rah']
                           )
    test_meeting.save_to_db()
