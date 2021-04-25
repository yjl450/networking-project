from logging import debug
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from time import time
from flask_socketio import join_room, leave_room

app = Flask(__name__,
            static_folder="../frontend/dist/",
            static_url_path="",
            template_folder="../frontend/dist")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
# , async_mode="threading")

user = {}  # mapping from userid (socketid) to username
rooms = {}  # mapping from room name (room_id) to dict of
"""
user = {userid: {userid: username}}
rooms = {room1: {user1: username, user2: username, ...}, 
         room2: {user3: username, user4: username, ...}}
"""

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
    variable_start_string='%%',
    variable_end_string='%%',
))

# Maintain a length of 10
def unique_room(sender_id):
    room_name = str(hash(str(time())+sender_id))[:10]
    if room_name in rooms.keys():
        return unique_room(sender_id)
    return room_name


@app.route('/')
def index():
    return render_template("index.html")


def contact_update():
    # print({"person": user, "group": rooms})
    emit("contact", {"person": user, "group": rooms}, broadcast=True)


def dup_check(name):
    for v in user.values():
        if name in v.values():
            return True
    return False


@socketio.on('login')
def login(message):
    result = ""
    # print("RECV:", request.sid, message)
    # print("SEND:", {'username': message['username'], "userid": request.sid})
    # validation
    if dup_check(message["username"]):
        result = "duplicate"
        emit('login-response',
             {'username': message['username'], "result": result, "userid": request.sid})
    else:
        result = "success"
        user[request.sid] = {request.sid: message["username"]}
        emit('login-response',
             {'username': message['username'], "result": result, "userid": request.sid})
        contact_update()


@socketio.on('message')
def send_message(message):
    """
     {"sender": *userid*, 
      "receiver": *groupid*, 
      "message": *content*}
    """
    # print({"sender": message["sender"],
    #        "receiver": message["receiver"], "message": message["message"]})
    emit("message",
         {"sender": message["sender"], "receiver": message["receiver"],
             "message": message["message"]},
         skip_sid=message["sender"],
         to=message["receiver"])


@socketio.on("create_group")
def create_group(message):
    """
    {"sender": *userid*, 
     "member":{*userid*: *username*}}
    """
    group_id = unique_room(message["sender"])
    rooms[group_id] = message["member"]
    for other in message["member"].keys():
        join_room(group_id, sid=other)
    emit('update_group',
         {"groupid": group_id, "member": message["member"]},
         to=group_id)
    contact_update()
    # print(rooms)


@socketio.on("join_group")
def join_group(message):
    """
    {"groupid": *groupid*, 
     "sender": *userid*}
    """
    groupid, userid = message["groupid"], message["sender"]
    username = user[userid][userid]
    rooms[groupid][userid] = username
    join_room(groupid, sid=userid)
    # print()
    emit('update_group',
         {"groupid": groupid, "member": rooms[groupid]},
         to=groupid)
    contact_update()
    # print(rooms)


@socketio.on("leave_group")
def leave_group(message):
    """
    {"groupid": *groupid*, 
     "sender": *userid*}
    """
    group_id = message["groupid"]
    del rooms[group_id][message["sender"]]
    if len(rooms[group_id]) <= 2:
        del rooms[group_id]
        emit('delete_group', {"groupid": group_id}, to=group_id)
        leave_room(group_id)
    else:
        leave_room(group_id)
        emit('update_group',
             {"groupid": group_id, "member": rooms[group_id]},
             to=group_id)
    contact_update()


@socketio.on("logout")
def logout(message):
    """
    {"sender": *userid*}
    """
    # print("LOGOUT:", message)
    uid = request.sid
    if (uid in user.keys()):
        del user[uid]
    for k in list(rooms.keys()):
        v = rooms[k]
        if uid in v.keys():
            del v[uid]
            if len(v) <= 2:
                emit('delete_group', {"groupid": k}, to=k)
                del rooms[k]
                try:
                    leave_room(k, sid=uid)
                except:
                    pass
            else:
                try:
                    leave_room(k, sid=uid)
                except:
                    pass
                emit('update_group',
                     {"groupid": k, "member": v},
                     to=k)
    contact_update()

@socketio.on("disconnect")
def after_disconnect(reason=""):
    """
    {"sender": *userid*}
    """
    # print("Disconnect:", reason)
    uid = request.sid
    if (uid in user.keys()):
        del user[uid]
    for k in list(rooms.keys()):
        v = rooms[k]
        if uid in v.keys():
            del v[uid]
            if len(v) <= 2:
                emit('delete_group', {"groupid": k}, to=k)
                del rooms[k]
            else:
                emit('update_group',
                     {"groupid": k, "member": v},
                     to=k)
    contact_update()


if __name__ == '__main__':
    socketio.run(app)
