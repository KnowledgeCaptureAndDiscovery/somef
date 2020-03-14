from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UrlForm(FlaskForm):
    giturl = StringField('Git URL', validators=[DataRequired()])
    threshold = StringField('Classifier Threshold', validators=[DataRequired()], render_kw={"placeholder": "Default value: .80"})

    submit = SubmitField('Classify')
