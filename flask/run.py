from flask import Flask, Blueprint, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, \
    current_app

from droptarget import admin

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)

@app.route("/")
@app.route("/home")
def index():

    return render_template('home.html', title="Home")


app.register_blueprint(admin.admin)

# Debugging.  Turn this off when done!
app.debug = app.config["DEBUG"]

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
