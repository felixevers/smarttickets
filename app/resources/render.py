from flask import Flask, send_from_directory, redirect
from config import config


def register_render(app: Flask):

    @app.route('/f/<path:path>')
    def render_files(path):
        return send_from_directory(config["FRONTEND"], path)

    @app.route('/f/')
    def render_index():
        return send_from_directory(config["FRONTEND"], 'index.html')

    @app.errorhandler(404)
    def render_all_index(e):
        return send_from_directory(config["FRONTEND"], 'index.html')

    @app.route('/')
    def redirect_index():
        return redirect("/f/", code=302)
