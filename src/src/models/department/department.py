import src.common.database as db
from src.models.users.users2 import User


class Department(object):

    def __init__(self,name,_id,head,superd=None,subs=[]):
        self.name = name
        self.head = User(**head) if type(head) == dict else head
        self._id = _id
        self.superd = Department.get_by_id(superd) if superd is not None else superd
        self.subs = [Department.get_by_id(sub) for sub in subs] if subs else subs
        self.members = self.add_members()


    def save_to_db(self):
        db.Database.update('departments', {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "head": self.head.json(),
            "_id": self._id,
            "superd": self.superd._id if self.superd else None,
            "subs": [ sub._id for sub in self.subs ] if self.subs else []
        }

    def add_members(self):
        db.Database.initialize()
        members = []
        for member in db.Database.find('users', {'department': self.name}):
            staff = User(**member)
            members.append(staff)
        return members

    @staticmethod
    def get_by_id(_id):
        data = db.Database.find_one('departments', {"_id": _id})
        return Department(**data)

    @staticmethod
    def get_by_name(name):
        data = db.Database.find_one('departments', {"name": name})
        return Department(**data)

    def get_heads(self):
        if not self.superd:
            return [self.head]
        else:
            return [self.head] + self.superd.get_heads()

    def get_members(self):
        if not self.subs:
            return self.members
        else:
            members = []
            for sub in self.subs:
                members += sub.get_members()
            return self.members + members



if __name__ == "__main__":
    lwpm = Department("Loveworld Publishing Ministry","lwpm",User.get_by_email("test@test.com"))
    lwpm.save_to_db()
    lwpmonline = Department("LWPM Online","lwpmonline",User.get_by_email("test2@test.com"),superd="lwpm")
    lwpmonline.save_to_db()

    print(lwpm.head == User.get_by_id("b8f7fbd91e5e43f58a7c53cade1fdff1"))



