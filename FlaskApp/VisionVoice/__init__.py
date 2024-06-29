from flask import Flask, request, jsonify,url_for
from flask_sqlalchemy import SQLAlchemy

import os,sys
import logging

direc=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(direc,"data.sqlite")


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db=SQLAlchemy(app)