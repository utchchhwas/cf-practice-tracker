from flask import Flask, render_template

import cx_Oracle

# Establish the database connection
connection = cx_Oracle.connect(user="c##cf", password="cf",
                               dsn="localhost/orcl")

print('Successfully connected to the database')



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")




@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/welcome")
def afterlogin():
    return render_template("afterlogin.html")


def main():
    app.run(debug=True)  # Run with debug mode turned on


if __name__ == "__main__":
    main()