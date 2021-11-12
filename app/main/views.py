from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..request import get_quotes



@main.route('/')
def index():
    Quote = get_quotes()
    return render_template('cover.html', Quote=Quote)