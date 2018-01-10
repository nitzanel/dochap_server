import conf
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, FileField,SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    gtf_file = FileField(
        'Gtf file',
        render_kw={
            'id':'gtfUpload',
            'onchange':'fileUploadCallback();'
        },
        validators=[DataRequired()]
    )
    specie_selection = SelectField(
        'Specie',
        choices=conf.supported_species,
        validators=[DataRequired()]
    )
    submit = SubmitField(
        'Upload',
        render_kw={'class':'btn btn-primary'}
    )

