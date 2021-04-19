from logging import debug
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from time import time

app = Flask(__name__,
            static_folder="../frontend/dist/",
            static_url_path="",
            template_folder="../frontend/dist")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')
# , async_mode="threading")

user = {}  # mapping from userid (socketid) to username
rooms = {}  # mapping from room name (room_id) to dict of

jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
    variable_start_string='%%',
    variable_end_string='%%',
))

# Maintain a length of 10
def unique_room(sender_id):
    room_name = str(hash(str(time()+sender_id)))[:10]
    if room_name in rooms.keys():
        return unique_room(sender_id)
    return room_name


@app.route('/')
def index():
    return render_template("index.html")


def contact_update():
    emit("contact", {"person": user, "group": rooms}, broadcast=True)


@socketio.on('login')
def login(message):
    result = ""
    print("RECV:", request.sid, message)
    print("SEND:", {'username': message['username'], "userid": request.sid})
    # validation
    if message["username"] in user.values():
        result = "duplicate"
        emit('login-response',
            {'username': message['username'], "result": result, "userid": request.sid})
    else:
        result = "success"
        user[request.sid] = {request.sid:message["username"]}
        emit('login-response',
            {'username': message['username'], "result": result, "userid": request.sid})
        contact_update()

if __name__ == '__main__':
    socketio.run(app)
