# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 22:49:27 2023

@author: Simanta Limbu
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    images = db.relationship('Image', backref='user', lazy=True)