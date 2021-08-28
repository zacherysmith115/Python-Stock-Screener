from flask import render_template, jsonify, request
import pandas as pd
import matplotlib.pyplot as plt

from Screener import app, db
from Screener.form import SelectForm
from Screener.models import Industry, Sector

# Home routing 
@app.route('/', methods = ['GET', 'POST'])
def home():
    form = SelectForm()
    sector = Sector.query.filter_by(sector = 'Industrials').first()
    form.industry_select.choices = sector.industries


    # Form submitted
    if request.method == 'POST':

        # Get securities in the selected industry
        industry = Industry.query.filter_by(industry = form.industry_select.data).first()
        securities = industry.securities

        # Build a dataframe with all the delta values for the securities 
        data = {}
        for security in securities:
            data[security.symbol] = [security.one_day_delta, security.one_week_delta, security.one_month_delta,
                    security.three_month_delta, security.one_year_delta, security.three_year_delta,
                    security.five_year_delta]

        columns = ['1D', '1W', '1M', '3M', '1Y', '3Y', '5Y']
        df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
        
        # Sort based on selected delta
        df.sort_values(by=[form.delta_select.data], inplace=True, ascending=False)
      
        # Get the best performers
        df = df.head()
        series = df[form.delta_select.data]
      
        return render_template('result.html', industry = industry, delta = form.delta_select.data, series = series)

    return render_template('select.html', form = form)


# Helper routing function to provide industry data based off sector selection
@app.route('/<sector>', methods = ['GET'])
def getSectorData(sector: 'str'):

    sector_model = Sector.query.filter_by(sector = sector).first()

    # Handle initial GET request for the page
    if not sector_model:
        return jsonify(None)

    industries = {}
    i = 0
    
    # build dictionary
    for industry in sector_model.industries:
        industries[i] = str(industry)
        i = i + 1

    return jsonify(industries)