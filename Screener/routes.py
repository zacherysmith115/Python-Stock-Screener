from flask import render_template, jsonify, request
import pandas as pd

from Screener import app 
from Screener.form import SelectForm
from Screener.models import Industry, Sector

# Home routing 
@app.route('/', methods = ['GET', 'POST'])
def home():
    form = SelectForm()
    sector = Sector.query.filter_by(sector = 'Industrials').first()
    form.industry_select.choices = sector.industries
    

    if request.method == 'POST' and form.validate_on_submit():
        securities = form.industry_select.data.securities

        data = {}
        for security in securities:
            data[security.symbol] = [security.one_day_delta, security.one_week_delta, security.one_month_delta,
                    security.three_month_delta, security.one_year_delta, security.three_year_delta,
                    security.five_year_delta]

        df = pd.DataFrame.from_dict(data, orient='index')

        print(df)
        
        if form.delta_select.data == '1D':
            df = df.sort_values(by=[0])
        elif form.delta_select.data == '1W':
            df = df.sort_values(by=[1])
        elif form.delta_select.data == '1M':
            df = df.sort_values(by=[2])
        elif form.delta_select.data == '3M':
            df = df.sort_values(by=[3])
        elif form.delta_select.data == '1Y':
            df = df.sort_values(by=[4])
        elif form.delta_select.data == '3Y':
            df = df.sort_values(by=[5])
        elif form.delta_select == '5Y':
            df = df.sort_values(by=[6])

        print(df)


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