from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, HiddenField, TextField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Required, Optional, AnyOf


class AddPlayerForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    player_id = HiddenField('player_id', validators=[Optional()])

    nick = StringField('Initials', validators=[Optional()])

    name = StringField('Name', validators=[Required(message="Must enter player name")])

    email = StringField('Email', validators=[Optional()])

    phone = StringField('Phone', validators=[Optional()])

    location = StringField('Location', validators=[Optional()])

    ifpanumber = IntegerField('IFPA Number', validators=[Optional()])

    pinside = StringField('Pinside', validators=[Optional()])

    notes = TextField('Notes', validators=[Optional()])

    status = SelectField(
        'Dues Paid?',
        choices=[('0', 'Not Paid'), ('1', 'Paid')],
        validators=[AnyOf(values=['0', '1'], message="Must select whether or not dues have been paid")]
    )

    active = SelectField(
        'Active?',
        choices=[('true', 'Yes'), ('false', 'No')],
        validators=[AnyOf(values=['false', 'true'], message="Must select whether or not player is active")]
    )


class DelPlayerForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    player_id = HiddenField('player_id', validators=[Optional()])

    name = HiddenField('name', validators=[Optional()])


class AddLocationForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    location_id = HiddenField('location_id', validators=[Optional()])

    name = StringField('Name', validators=[Required(message="Must enter location name")])

    address = StringField('Address', validators=[Optional()])

    locType = SelectField(
        'Location Type?',
        choices=[('0', 'Commercial'), ('1', 'Residence'), ('2', 'Other')],
        validators=[AnyOf(values=['0', '1', '2'], message="Must select location type")]
    )

    addressPrivate = SelectField(
        'Private?',
        choices=[('true', 'Private'), ('false', 'Open')],
        validators=[AnyOf(values=['false', 'true'], message="Must select whether or not location is private")]
    )

    active = SelectField(
        'Active?',
        choices=[('true', 'Yes'), ('false', 'No')],
        validators=[AnyOf(values=['false', 'true'], message="Must select whether or not location is active")]
    )

    notes = TextField('Notes', validators=[Optional()])


class DelLocationForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    location_id = HiddenField('location_id', validators=[Optional()])

    name = HiddenField('name', validators=[Optional()])


class AddMachineForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    machine_id = HiddenField('player_id', validators=[Optional()])

    name = StringField('Name', validators=[Required(message="Must enter machine name")])

    abbr = StringField('Abbreviation', validators=[Optional()])

    manufacturer = StringField('Manufacturer', validators=[Optional()])

    manDate = StringField('Manufacturer Date', validators=[Optional()])

    players = IntegerField('Num Players', validators=[Optional()])

    gameType = StringField('Type', validators=[Optional()])

    theme = TextField('Theme', validators=[Optional()])

    ipdbURL = TextField('IPDB URL', validators=[Optional()])


class DelMachineForm(FlaskForm):

    operation = HiddenField('operation', validators=[Optional()])

    machine_id = HiddenField('machine_id', validators=[Optional()])

    name = HiddenField('name', validators=[Optional()])