from flask import render_template, jsonify, request
from Screener import app 
from Screener.form import SelectForm
from Screener.models import Industry, Sector

# Home routing 
@app.route('/', methods = ['GET', 'POST'])
def home():
    form = SelectForm()

    if request.method == 'POST' and form.validate_on_submit():
        pass

    return render_template('select.html', form = form)


# Helper routing function to provide industry data based off sector selection
@app.route('/<sector>', methods = ['GET'])
def getSectorData(sector: 'str'):

    sector_model = Sector.query.filter_by(sector = sector).first()

    industries = {}
    i = 0
    
    # build dictionary
    for industry in sector_model.industries:
        industries[i] = str(industry)
        i = i + 1

    return jsonify(industries)