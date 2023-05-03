# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 22:50:59 2023

@author: Simanta Limbu
"""

from flask import render_template

class StartScreen:
    @staticmethod
    def home():
        return render_template('home.html')
