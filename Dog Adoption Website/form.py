from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class AddForm(FlaskForm):
    name=StringField('The name of the dog is: ')
    submit=SubmitField('Add dog')

class DelForm(FlaskForm):
    id=IntegerField('The id to delete: ')
    submit=SubmitField('Remove Dog')

class AddOwner(FlaskForm):
    item_name=StringField('The name of the owner is: ')
    puppy_id=IntegerField('The id of the dog you want: ')
    submit=SubmitField('Add Owner')
