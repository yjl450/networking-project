# Launch

    $ python backend/server.py

This will launch the server and hosting the pre-built frontend files. The server requires dependencies: Flask, Flask-Socketio, which can be installed by running

    $ pip install flask flask-socketio

Frontend pages have been built already in `frontend/dist/`. However, you can build the frontend Vue project by running the following command:

    cd frontend/
    yarn # install dependencies
    yarn build

This requires Node.js and a package manager, yarn of npm.