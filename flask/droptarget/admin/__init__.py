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
    return render_template('admin-home.html',
                           title="Admin - Home",
                           obj_counts=_get_object_counts())


@admin.route('/admin/machines')
def show_admin_machines():
    return render_template('admin-machines.html',
                           title="Admin - Machines",
                           obj_counts=_get_object_counts(),
                           machine_data=_get_all_machines())


@admin.route('/admin/locations')
def show_admin_locations():
    return render_template('admin-locations.html',
                           title="Admin - Locations",
                           obj_counts=_get_object_counts(),
                           location_data=_get_all_locations())


@admin.route('/admin/players')
def show_admin_players():
    return render_template('admin-players.html',
                           title="Admin - Players",
                           obj_counts=_get_object_counts(),
                           player_data=_get_all_players())


def _get_all_players():
    player_json = playfield.api_request("get", "player", "all_players", None)

    if player_json is not "Error" and player_json is not None:
        player_entries = playfield.parse_json(player_json)
    else:
        # Fail silently
        player_entries = "api_error"

    return player_entries


def _get_all_locations():
    location_json = playfield.api_request("get", "location", "all_locations", None)

    if location_json is not "Error" and location_json is not None:
        location_entries = playfield.parse_json(location_json)
    else:
        # Fail silently
        location_entries = "api_error"

    return location_entries


def _get_all_machines():
    machine_json = playfield.api_request("get", "machine", "all_machines", None)

    if machine_json is not "Error" and machine_json is not None:
        machine_entries = playfield.parse_json(machine_json)
    else:
        # Fail silently
        machine_entries = "api_error"

    return machine_entries


def _get_object_counts():
    object_count_json = playfield.api_request("get", "general", "get_object_counts", None)

    if object_count_json is not "Error" and object_count_json is not None:
        obj_count_entries = playfield.parse_json(object_count_json)
    else:
        # Fail silently
        obj_count_entries = "api_error"

    return obj_count_entries
