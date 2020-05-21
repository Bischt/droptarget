from flask import Flask, Blueprint, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, \
    current_app
from ..backend import PlayfieldAPI
from ..forms import AddPlayerForm

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
    playerform = AddPlayerForm()

    # When a form is submitted, process it
    if request.method == 'POST':
        # Process new player form
        if playerform.validate_on_submit():
            # Pull submitted data from the form
            data = dict(player_id=request.form['player_id'],
                        name=request.form['name'],
                        nick=request.form['nick'],
                        email=request.form['email'],
                        phone=request.form['phone'],
                        location=request.form['location'],
                        ifpanumber=request.form['ifpanumber'],
                        pinside=request.form['pinside'],
                        notes=request.form['notes'],
                        status=request.form['status'],
                        active=request.form['active'])

            results = playfield.api_request("post", "player", "add_player", data)

    return render_template('admin-players.html',
                           title="Admin - Players",
                           obj_counts=_get_object_counts(),
                           player_data=_get_all_players(),
                           playerform=playerform)


@admin.route('/admin/_admin_player_info')
# Get all the admin editable details about a player from the database and return as JSON
def _admin_player_info():
    player_id = request.args.get('player_id', 0, type=str)

    # Query API for specific player by id
    data = (player_id, )
    player_json = playfield.api_request("get", "player", "player_by_id", data)

    # If error querying API flash message to user
    if player_json is not "Error" and player_json is not None:
        entries = playfield.parse_json(player_json)
    else:
        flash("Problem accessing Playfield API")
        entries = {}

    # TODO: Make API call to IFPA to refresh stored player info

    # Parse out results and compile into JSON
    for entry in entries:
        player_id = entry['player_id']
        nick = entry['nick']
        name = entry['name']
        phone = entry['phone']
        email = entry['email']
        location = entry['location']
        ifpanumber = entry['ifpanumber']
        pinside = entry['pinside']
        notes = entry['notes']
        status = entry['status']
        active = entry['active']

    return jsonify(player_id=player_id,
                   nick=nick,
                   name=name,
                   phone=phone,
                   email=email,
                   location=location,
                   ifpanumber=ifpanumber,
                   pinside=pinside,
                   notes=notes,
                   status=status,
                   active=active)


@admin.route('/admin/_update_player_status')
# Update the player's status.  Status is used to determine if the user is paid up.
def _update_player_status():
    player_id = request.args.get('player_id', 0, type=str)
    status = request.args.get('status', 0, type=int)
    if status == 1:
        statusvalue = 1
    elif status == 0:
        statusvalue = 0
    else:
        statusvalue = 0

    data = (player_id, str(statusvalue),)
    retval = playfield.api_request("get", "player", "set_status", data)

    return jsonify(ret=0)


@admin.route('/admin/_update_player_active')
# Update the player's status.  Status is used to determine if the user is paid up.
def _update_player_active():
    player_id = request.args.get('player_id', 0, type=str)
    active = request.args.get('active', 0, type=str)

    if active == "true":
        activevalue = True
    elif active == "false":
        activevalue = False
    else:
        activevalue = False

    data = (player_id, str(activevalue),)
    retval = playfield.api_request("get", "player", "set_active", data)

    return jsonify(ret=0)


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
