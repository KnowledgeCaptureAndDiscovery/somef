from flask_wtf import FlaskForm
from wtforms import SubmitField

class DownloadButton(FlaskForm):
    submit_download = SubmitField('Download JSON file')
