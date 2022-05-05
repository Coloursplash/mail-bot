# -*- coding: utf-8 -*-
# Import Monkey module from gevent for monkey-patching
from gevent import monkey
# Monkey-patching standart Python library for async working
monkey.patch_all()
# Import WSGI server from Gevent
from gevent.pywsgi import WSGIServer
# Import Compress module from Flask-Compress for compress static
# content (HTML, CSS, JS)
from flask_compress import Compress

# Flask
from flask import Flask
from threading import Thread


app = Flask("Mail bot")
compress = Compress()
compress.init_app(app)


@app.route('/')
def flask_main():
    return "The mail bot is alive!"


def keep_alive():
    server = Thread(target=run)
    server.start()


def run():
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()