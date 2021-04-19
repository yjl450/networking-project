from logging import debug
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__,
            static_folder = "../frontend/dist/",
            static_url_path="",
            template_folder = "../frontend/dist")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
variable_end_string='%%',
    ))


@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('login')
def test_message(message):
    print(request.sid, message)
    emit('login-response', {'username': message['username'], "userid": 1001})

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)