from wtforms import Form, TextField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(Form):
  search = TextField('', [DataRequired()])
  submit = SubmitField('Buscar', render_kw={'class': 'btn btn-success btn-block'})
