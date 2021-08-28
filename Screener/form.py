from flask_wtf import FlaskForm 
from wtforms import SubmitField, validators
from wtforms.fields.core import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from Screener.models import Industry, Sector, Industry



delta = ['1D', '1W', '1M', '3M', '1Y', '3Y', '5Y']



def sectorQueryFactory():
    return Sector.query

def industryQueryFactory():
    sector = Sector.query.first()
    return Industry.query.filter_by(sector = sector)

class SelectForm(FlaskForm):
    sector_select = QuerySelectField('Sector: ', query_factory=sectorQueryFactory, 
                                    allow_blank=False, render_kw={'onchange': 'sectorSelection()'})
    #industry_select = QuerySelectField('Industry: ',  query_factory= industryQueryFactory)
    industry_select = SelectField('Industry: ', coerce=str, validators=[validators.InputRequired()])
    delta_select = SelectField('Duration: ', choices = delta, validators=[validators.InputRequired()])

    submit = SubmitField('Search')