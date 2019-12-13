# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/aaaaaaaa'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(16), unique=True)

@app.route('/')
def hello_world():
    return 'Hello World!'

db.drop_all()
db.create_all()
db.session.commit()
if __name__ == '__main__':

    app.run()