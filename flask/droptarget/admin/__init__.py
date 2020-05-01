from flask import Flask, Blueprint, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, \
    current_app
from ..backend import PlayfieldAPI


app = Flask(__name__)

admin = Blueprint('admin',
                  __name__,
                  static_url_path='/admin',
                  static_folder='../static',
                  template_folder='../templates')

playfield = PlayfieldAPI("host.docker.internal", "8080")


@admin.route('/admin')
def show_admin():
    return render_template('admin-home.html',
                           title="Admin")