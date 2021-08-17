from Screener import db


class Sector(db.Model):
    __tablename__ = 'sector'

    id = db.Column(db.Integer, primary_key = True)
    sector = db.Column(db.String(120), nullable = False)

    # one to many relationship with Industry 
    industries = db.relationship('Industry', back_populates = 'sector')

    def __repr__(self) -> str:
        return f'Sector: {self.sector}'



class Industry(db.Model):
    __tablename__ = 'industry'

    id = db.Column(db.Integer, primary_key = True)
    industry = db.Column(db.String(120), nullable = False)

    # many to one relationship to Sector
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable = False)
    sector = db.relationship('Sector', back_populates = 'industries')


    def __repr__(self) -> str:
        return f'Industry: {self.industry}'



class Security(db.Model):
    __tablename__ = 'securities'

    id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.String(5), nullable = False)
    security = db.Column(db.String(120), nullable = False)
    sector = db.Column(db.String(120), nullable = False)
    industry = db.Column(db.String(120), nullable = False)

    def __repr__(self) -> str:
        return f'{self.symbol}: {self.security}'

