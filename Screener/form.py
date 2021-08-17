from flask_wtf import FlaskForm 
from wtforms import SubmitField
from wtforms.fields.core import SelectField


sector_data = [
    'Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive',
    'Energy', 'Financial Services', 'Healthcare', 'Industrials', 'Real Estate','Technology',
    'Utilities']

basic_materials_industries = ['Chemicals', 'Construction Materials', 'Metals & Mining', 'Paper & Forest Products']
communication_services_industries = ['Telecommunications Services', 'Media & Publishing']
consumer_cyclical_industries = ['Automobiles & Auto Parts', 'Containers & Packaging', 'Diversified Retail', 'Hotels & Entertainment Services',
    'Houshold Goods', 'Leisure Products', 'Speciality Retailers', 'Textiles & Apparel']
consumer_defensive_industries = ['Beverages', 'Food & Drug Retailing', 'Food & Tobacco', 'Personal & Household Products & Services']
energy_industries = ['Coal', 'Oil & Gas', 'Oil & Gas Related Equipment and Services', 'Renewable Energy']
financial_services_industries = ['Banking Services', 'Collective Investments', 'Holding Companies', 'Insurance', 'Investment Banking & Investment Services']

delta = ['1D', '1W', '1M', '3M', '1Y', '3Y', '5Y']

class SelectForm(FlaskForm):
    sector_select = SelectField('Sector: ', choices = sector_data)
    industry_select = SelectField('Industry: ', choices = basic_materials_industries)
    delta_select = SelectField('Duration: ', choices = delta)

    submit = SubmitField('Search')