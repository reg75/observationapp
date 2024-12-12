from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

teacher_choices = [] # Used by new_observation() / usada por new_observation() 

class ObservationForm(FlaskForm):
   Observation_Teacher = SelectField('Teacher Observed', choices=teacher_choices, validators=[
      DataRequired("Please select a teacher")])
   Observation_Class = StringField('Class', validators=[
      DataRequired(),
      Length(max=8, message="Max 8 characters")])
   Observation_Focus = StringField('Focus', validators=[
      DataRequired(),
      Length(max=32, message="Max 32 characters")])
   Observation_Strengths = TextAreaField('Strengths', validators=[Length(max=1000, message="Max 1000 characters")], render_kw={'class': 'custom-textarea'})
   Observation_Weaknesses = TextAreaField('Areas for development', validators=[Length(max=1000, message="Max 1000 characters")], render_kw={'class': 'custom-textarea'})
   Observation_Comments = TextAreaField('Other comments', validators=[Length(max=1000, message="Max 1000 characters")], render_kw={'class': 'custom-textarea'})
   submit = SubmitField('Save')