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