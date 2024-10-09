from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,
TimeField, DateField, TextAreaField, BooleanField)
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime



class NewAppointment(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  start_date = DateField("Start", validators=[DataRequired()])
  start_time = TimeField("Start", validators=[DataRequired()])
  end_date = DateField("End", validators=[DataRequired()])
  end_time = TimeField("End", validators=[DataRequired()])
  description = TextAreaField("Description")
  private = BooleanField("Private")
  submit = SubmitField("Create an appointment")

  def validate_end_date(form, field):
    start = datetime.combine(form.start_date.data, form.start_time.data).strftime("%Y-%m-%d %H:%M:%S")
    end = datetime.combine(form.end_date.data, form.end_time.data).strftime("%Y-%m-%d %H:%M:%S")
    if start >= end:
      raise ValidationError("End date/time must come after start date/time")
