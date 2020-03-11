from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UrlForm(FlaskForm):
    giturl = StringField('Git URL', validators=[DataRequired()])
<<<<<<< HEAD
    threshold = StringField('Classifier Threshold', validators=[DataRequired()])
=======
    threshold = StringField('Classifier Threshold', validators=[DataRequired()], render_kw={"placeholder": "Default value: .80"})
>>>>>>> 0b143d4f77549d41efed5f89b20c97d7df70480d
    submit = SubmitField('Classify')
