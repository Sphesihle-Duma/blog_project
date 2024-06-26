#!/usr/bin/env python3
from flask import render_template
from mainapp import app, db


@app.errorhandler(404)
def not_found_error(error):
    '''
       Customized 404 error page
    '''
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
