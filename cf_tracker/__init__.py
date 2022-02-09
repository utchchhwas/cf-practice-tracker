import imp
from flask import Flask, render_template, url_for, redirect


# this is the application factory function
# creates an instance of our flask app
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp) 

    from . import account
    app.register_blueprint(account.bp)

    from . import contests
    app.register_blueprint(contests.bp)

    from . import update_db

    @app.route('/update_contests')
    def update_contests():
        update_db.update_contests()
        return redirect(url_for('index'))
    
    @app.route('/update_problems')
    def update_problems():
        update_db.update_problems()
        return redirect(url_for('index'))

    return app
