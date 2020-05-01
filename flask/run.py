from flask import Flask, Blueprint, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, \
    current_app

from droptarget import admin

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():

    return render_template('home.html', title="Home")


app.register_blueprint(admin.admin)

if __name__ == "__main__":
    app.run(debug=True)