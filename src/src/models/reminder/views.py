from src.models.reminder.notification import Notification
from flask import Blueprint,jsonify


notification_blueprint = Blueprint('notification', __name__)


@notification_blueprint.route("/read/<string:_id>")
def read(_id):
    notif = Notification.get_by_id(_id)
    notif.check()
    done = { "message": "{} has been checked".format(notif._id)}
    return jsonify(done)

