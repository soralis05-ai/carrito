from flask import render_template, redirect, url_for, flash
from . import auth_bp

@auth_bp.route('/login')
def login():
    return 'login page placeholder'

@auth_bp.route('/register')
def register():
    return 'register page placeholder'
