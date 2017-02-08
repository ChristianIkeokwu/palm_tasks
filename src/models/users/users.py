from src.common import CONSTANTS
from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils
from src.models.projects.projects import Project
import src.models.meetings.meetings as meetings
from src.models.department.department import Department
import uuid


class User(object):

    def __init__(self,email, password, title, first_name, last_name,department, _id=None,meetings=[], projects=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.title = title
        try:
            department = Department.get_by_name(department)
        except TypeError:
            department = department
        self.department = department
        self.meetings = meetings
        self.projects = projects

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one("users", {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password,title, first_name, last_name,department):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password),title, first_name, last_name, department).save_to_db()

        return True

    @staticmethod
    def get_by_email(email):
         Database.initialize()
         return User(**Database.find_one("users", {"email": email}))

    @staticmethod
    def get_by_id(_id):
        Database.initialize()
        return User(**Database.find_one("users", {"_id": _id}))


    def save_to_db(self):
        Database.update('users', {"_id": self._id}, self.json())

    def url(self):
        return CONSTANTS.url + r'users/' + self._id

    def __eq__(self, other):
        return self._id == other._id

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "department": self.department if type(self.department) == str else self.department.name,
            "meetings": list(set(self.meetings)), #remove duplicates and then sort
            "projects": list(set(self.projects)) # last line
        }
    def progress(self):
        total = 0
        number = 1
        for project in self.projects:
            project = Project.get_by_id(project)
            total += project.progress()
            number += 1
        return int(total/number)

    def get_projects(self):
        projects = []
        for project in self.projects:
            projects.append(Project.get_by_id(project))
        return sorted(projects)

    def get_meetings(self):
        meetings_list = []
        for meeting in self.meetings:
            meetings_list.append(meetings.Meeting.get_by_id(meeting))
        return sorted(meetings_list)

    def add_meeting(self, meeting_id):
        self.meetings.append(meeting_id)
        self.save_to_db()

    def __repr__(self):
        return "{}. {} {}".format(self.title, self.first_name.capitalize(), self.last_name.capitalize())

if __name__ == "__main__":
    Database.initialize()
    for user in Database.find('users',{}):
        user = User(**user)
        for meeting in user.meetings:
            if Database.find_one('meetings', {"_id": meeting}) is None:
                user.meetings.remove(meeting)
        user.save_to_db()





