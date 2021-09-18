from os import read
from flask import Flask
from flask import render_template, make_response, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
from time import sleep, time
from threading import Thread


class Main:
    def __init__(self):
        # Flask
        app = Flask(__name__)
        @app.route('/')
        def hello():
            if 'ID' in request.headers.keys():
                return self.log_maker(request.headers['id'])
            else:
                return render_template('dashboard.html')

        # Socket IO
        self.socketio = SocketIO(app)
        t = Thread(target=self.log_emitter)
        t.start()
        @self.socketio.on('connect')
        def send_first_log():
            emit("log-set", open("logfile", "r").read())
        self.socketio.run(app)
    
    def log_emitter(self):
        while True:
            log = open("logfile", "r").read()
            self.socketio.emit("log-set", log)
            lastlog = log
            start = time()
            while log == lastlog:
                sleep(0.1)


Main()
