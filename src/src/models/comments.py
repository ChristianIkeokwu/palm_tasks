import uuid
from src.common.database import Database


class Comment(object):
    def __init__(self, content, event, commenter, _id=None):
        self.content = content
        self._id = uuid.uuid4().hex if _id is None else _id
        self.event = event # r'project/project_id'
        self.commenter = commenter

    def save_to_db(self):
        Database.insert('comments', self.json())

    def json(self):
        return {
            "_id": self._id,
            "content": self.content,
            "event": self.event,
            "commenter": self.commenter
        }

    def delete(self):
        Database.remove('comments', {"_id": self._id})

    @classmethod
    def get_by_id(cls, event):
        pass
