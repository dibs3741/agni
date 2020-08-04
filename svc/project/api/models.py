from sqlalchemy.sql import func
from project import db


class User(db.Model):
    __tablename__ = 'test1'

    col1 = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class cInvestmentModel(db.Model): 
    __tablename__ = 'agni_portfolio_model'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50))
    category = db.Column(db.String(50))
    allocation = db.Column(db.Numeric(20,2))

class cPosition(db.Model): 
    __tablename__ = 'agni_etl_stage_ff1'
    id = db.Column(db.Integer, primary_key=True)
    asofdate = db.Column(db.Date)
    accname = db.Column(db.String(50))
    symbol = db.Column(db.String(50))
    costbasis = db.Column(db.Numeric(20,2))
    currentvalue = db.Column(db.Numeric(20,2))
