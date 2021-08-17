from flask.templating import render_template
from Screener import app
from Screener.form import SelectForm

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = SelectForm()
    return render_template('select.html', form = form)