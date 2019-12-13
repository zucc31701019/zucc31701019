# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/testt'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(16), unique=True)

class Users(db.Model):
    _tablename_='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16))
    email = db.Column(db.String(32))
    password = db.Column(db.String(16))
    role_id = db.Column(db.Integer)


@app.route('/')
def hello_world():
    data = Users.query.all()
    print(data)
    return 'Hello World!'

# db.drop_all()
# db.create_all()
# db.session.commit()

data = Users.query.all()
print(data)


if __name__ == '__main__':
    app.run()