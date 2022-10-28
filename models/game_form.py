from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class GameForm(FlaskForm):
    name = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    save = SubmitField('Salvar')
