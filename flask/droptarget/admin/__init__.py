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
@admin.route('/admin/home')
def show_admin_home():
    return render_template('admin-home.html', title="Admin - Home")


@admin.route('/admin/machines')
def show_admin_machines():
    return render_template('admin-machines.html', title="Admin - Machines")


@admin.route('/admin/locations')
def show_admin_locations():
    return render_template('admin-locations.html', title="Admin - Locations")


@admin.route('/admin/players')
def show_admin_players():
    return render_template('admin-players.html', title="Admin - Players")
