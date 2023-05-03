# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 23:05:21 2023

@author: Simanta Limbu
"""

# In ImageModel.py
from User import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
