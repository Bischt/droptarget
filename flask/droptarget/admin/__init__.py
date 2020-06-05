from flask import Flask, Blueprint, jsonify, request, session, g, redirect, url_for, abort, render_template, flash, \
    current_app
from ..backend import PlayfieldAPI
from ..forms import AddPlayerForm
from ..forms import DelPlayerForm
from ..forms import AddLocationForm
from ..forms import DelLocationForm
from ..forms import AddMachineForm
from ..forms import DelMachineForm

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


@admin.route('/admin/machines', methods=['GET', 'POST'])
def show_admin_machines():
    machineform = AddMachineForm()
    machinedeleteform = DelMachineForm()

    # When a form is submitted, process it
    if request.method == 'POST':
        # Process add/edit machine form

        # TODO: Figure out server side form validation
        # if machineform.validate_on_submit():

        if request.form['operation'] == "edit":
            # Editing existing machine
            results = _update_machine()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Edited machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

        elif request.form['operation'] == "delete":
            # Remove the machine
            results = _delete_machine()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Removed machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")
        else:
            # Adding new machine
            results = _add_machine()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Added new machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

    return render_template('admin-machines.html',
                           title="Admin - Machines",
                           obj_counts=_get_object_counts(),
                           machine_data=_get_all_machines(),
                           machineform=machineform,
                           machinedeleteform=machinedeleteform)


@admin.route('/admin/_admin_machine_info')
# Get all the admin editable details about a player from the database and return as JSON
def _admin_machine_info():
    machine_id = request.args.get('machine_id', 0, type=str)

    # Query API for specific player by id
    data = (machine_id, )
    machine_json = playfield.api_request("get", "machine", "machine_by_id", data)

    # If error querying API flash message to user
    if machine_json is not "Error" and machine_json is not None:
        entries = playfield.parse_json(machine_json)
    else:
        flash("Problem accessing Playfield API")
        entries = {}

    # TODO: Make API call to IFPA to refresh stored player info

    # Parse out results and compile into JSON
    for entry in entries:
        machine_id = entry['machine_id']
        name = entry['name']
        abbr = entry['abbr']
        manufacturer = entry['manufacturer']
        manDate = entry['manDate']
        players = entry['players']
        gameType = entry['gameType']
        theme = entry['theme']
        ipdbURL = entry['ipdbURL']

    return jsonify(machine_id=machine_id,
                   name=name,
                   abbr=abbr,
                   manufacturer=manufacturer,
                   manDate=manDate,
                   players=players,
                   gameType=gameType,
                   theme=theme,
                   ipdbURL=ipdbURL)


@admin.route('/admin/locations', methods=['GET', 'POST'])
def show_admin_locations():
    locationform = AddLocationForm()
    locationdeleteform = DelLocationForm()

    # When a form is submitted, process it
    if request.method == 'POST':
        # Process add/edit machine form

        # TODO: Figure out server side form validation
        # if locationform.validate_on_submit():

        if request.form['operation'] == "edit":
            # Editing existing machine
            results = _update_location()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Edited machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

        elif request.form['operation'] == "delete":
            # Remove the machine
            results = _delete_location()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Removed machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")
        else:
            # Adding new machine
            results = _add_location()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Added new machine - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

    return render_template('admin-locations.html',
                           title="Admin - Locations",
                           obj_counts=_get_object_counts(),
                           location_data=_get_all_locations(),
                           locationform=locationform,
                           locationdeleteform=locationdeleteform)


@admin.route('/admin/_admin_location_info')
# Get all the admin editable details about a location from the database and return as JSON
def _admin_location_info():
    location_id = request.args.get('location_id', 0, type=str)

    # Query API for specific location by id
    data = (location_id, )
    location_json = playfield.api_request("get", "location", "location_by_id", data)

    # If error querying API flash message to user
    if location_json is not "Error" and location_json is not None:
        entries = playfield.parse_json(location_json)
    else:
        flash("Problem accessing Playfield API")
        entries = {}

    # TODO: Make API call to IFPA to refresh stored player info

    # Parse out results and compile into JSON
    for entry in entries:
        location_id = entry['location_id']
        name = entry['name']
        address = entry['address']
        addressPrivate = entry['addressPrivate']
        notes = entry['notes']
        locType = entry['locType']
        active = entry['active']

    return jsonify(location_id=location_id,
                   name=name,
                   address=address,
                   addressPrivate=addressPrivate,
                   notes=notes,
                   locType=locType,
                   active=active)


def _add_location():
    data = dict(name=request.form['name'],
                nick=request.form['address'],
                email=request.form['addressPrivate'],
                phone=request.form['notes'],
                location=request.form['locType'],
                ifpanumber=request.form['active'])

    retval = playfield.api_request("post", "location", "add_location", data)

    return retval


def _update_location():

    data = dict(location_id=request.form['location_id'],
                name=request.form['name'],
                address=request.form['address'],
                addressPrivate=request.form['addressPrivate'],
                notes=request.form['notes'],
                locType=request.form['locType'],
                active=request.form['active'])

    retval = playfield.api_request("post", "location", "update_location", data)

    return retval


def _delete_location():
    data = (request.form['location_id'])
    retval = playfield.api_request("delete", "location", "delete_location", data)

    return retval


@admin.route('/admin/players', methods=['GET', 'POST'])
def show_admin_players():
    playerform = AddPlayerForm()
    playerdeleteform = DelPlayerForm()

    # When a form is submitted, process it
    if request.method == 'POST':
        # Process add/edit player form

        # TODO: Figure out server side form validation
        # if playerform.validate_on_submit():

        if request.form['operation'] == "edit":
            # Editing existing player
            results = _update_player()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Edited player - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

        elif request.form['operation'] == "delete":
            # Remove the player
            results = _delete_player()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Removed player - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")
        else:
            # Adding new player
            results = _add_player()

            if results is not "Error":
                # Succeeded, so lets display a message
                flash("info")
                flash("Added new player - %s" % request.form['name'])
            else:
                flash("error")
                flash("Problem accessing Playfield API")

    return render_template('admin-players.html',
                           title="Admin - Players",
                           obj_counts=_get_object_counts(),
                           player_data=_get_all_players(),
                           playerform=playerform,
                           playerdeleteform=playerdeleteform)


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


def _add_player():
    data = dict(name=request.form['name'],
                nick=request.form['nick'],
                email=request.form['email'],
                phone=request.form['phone'],
                location=request.form['location'],
                ifpanumber=request.form['ifpanumber'],
                pinside=request.form['pinside'],
                notes=request.form['notes'],
                status=request.form['status'],
                active=request.form['active'])

    retval = playfield.api_request("post", "player", "add_player", data)

    return retval


def _update_player():
    data = dict(player_id=request.form['player_id'],
                name=request.form['name'],
                nick=request.form['nick'].upper(),
                email=request.form['email'],
                phone=request.form['phone'],
                location=request.form['location'],
                ifpanumber=request.form['ifpanumber'],
                pinside=request.form['pinside'],
                notes=request.form['notes'],
                status=request.form['status'],
                active=request.form['active'])

    retval = playfield.api_request("post", "player", "update_player", data)

    return retval


def _delete_player():
    data = (request.form['player_id'])
    retval = playfield.api_request("delete", "player", "delete_player", data)

    return retval


def _add_machine():
    data = dict(name=request.form['name'],
                abbr=request.form['abbr'],
                manufacturer=request.form['manufacturer'],
                manDate=request.form['manDate'],
                players=request.form['players'],
                gameType=request.form['gameType'],
                theme=request.form['theme'],
                ipdbURL=request.form['ipdbURL'])

    retval = playfield.api_request("post", "machine", "add_machine", data)

    return retval


def _update_machine():

    data = dict(machine_id=request.form['machine_id'],
                name=request.form['name'],
                abbr=request.form['abbr'],
                manufacturer=request.form['manufacturer'],
                manDate=request.form['manDate'],
                players=request.form['players'],
                gameType=request.form['gameType'],
                theme=request.form['theme'],
                ipdbURL=request.form['ipdbURL'])

    retval = playfield.api_request("post", "machine", "update_machine", data)

    return retval


def _delete_machine():
    data = (request.form['machine_id'])
    retval = playfield.api_request("delete", "machine", "delete_machine", data)

    return retval


@admin.route('/admin/_update_player_status', methods=['GET'])
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

    return retval


@admin.route('/admin/_update_player_active', methods=['GET'])
# Update the player's active status.
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

    return retval


def _get_all_players():
    player_json = playfield.api_request("get", "player", "all_players", None)

    if player_json is not "Error" and player_json is not None:
        player_entries = playfield.parse_json(player_json)
    else:
        # Fail silently
        player_entries = "api_error"

    return player_entries


@admin.route('/admin/_update_location_private', methods=['GET'])
# Update the location's status.  Status is used to determine if the location address is private.
def _update_location_private():
    location_id = request.args.get('location_id', 0, type=str)
    address_private = request.args.get('addressPrivate', 0, type=int)
    if address_private == 1:
        address_private_value = 1
    elif address_private == 0:
        address_private_value = 0
    else:
        address_private_value = 0

    data = (location_id, str(address_private_value),)
    retval = playfield.api_request("get", "location", "set_private", data)

    return retval


@admin.route('/admin/_update_location_active', methods=['GET'])
# Update the location's active status
def _update_location_active():
    location_id = request.args.get('location_id', 0, type=str)
    active = request.args.get('active', 0, type=str)

    if active == "true":
        active_value = True
    elif active == "false":
        active_value = False
    else:
        active_value = False

    data = (location_id, str(active_value),)
    retval = playfield.api_request("get", "location", "set_active", data)

    return retval

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
