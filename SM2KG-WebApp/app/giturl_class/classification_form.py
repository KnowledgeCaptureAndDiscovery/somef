from flask_wtf import FlaskForm
from wtforms import SubmitField

class ClassificationForm(FlaskForm):
    submit_invo = SubmitField("Description")
    submit_inst = SubmitField("Invocation")
    submit_cita = SubmitField("Citation")
    submit_desc = SubmitField("Description")
