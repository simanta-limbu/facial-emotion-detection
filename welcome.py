# -*- coding: utf-8 -*-
"""
Created on Mon May  1 23:06:37 2023

@author: Simanta Limbu
"""

from flask_login import current_user

class welcomeMessage:
    @staticmethod
    def welcome2():
        if current_user.is_authenticated:
            return f"<h1>Hello, {current_user.username}! You are logged in.</h1>"
        else:
            return "<h1>Hello, you are not logged in.</h1>"