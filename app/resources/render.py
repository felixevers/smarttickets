from flask import Flask, send_from_directory, redirect
from config import config


def register_render(app: Flask):

    @app.route('/f/<path:path>')
    def render_files(path):
        return send_from_directory(config["FRONTEND"], path)

    @app.route('/f/', defaults={'path': ''})
    @app.route('/f/<path:path>')
    def render_index(path):
        return send_from_directory(config["FRONTEND"], 'index.html')

    @app.route('/')
    def redirect_index():
        return redirect("/f/", code=302)
