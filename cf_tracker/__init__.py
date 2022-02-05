from flask import Flask, render_template, url_for


# this is the application factory function
# creates an instance of our flask app
def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    from . import db
    db.init_app(app)

    return app
