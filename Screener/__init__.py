from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# app config and db initialization #
app = Flask(__name__)
app.config['SECRET_KEY'] = '653d72d9f6ed01acf0d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
db = SQLAlchemy(app)

