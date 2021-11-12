from flask import render_template,request,redirect,url_for,abort
from . import main



@main.route('/')
def index():
    return '<h1> its working</h1>'