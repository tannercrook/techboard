# views/public.py

# This view contains all of the resources for public facing views


import sys
sys.path.append("..")
from flask import Blueprint, render_template, session, request, jsonify
from flask_login import login_required

from techBoard.models.DBase import connection


# set blueprint
public = Blueprint('public', __name__)

# routes
# ========================================

# Homepage with search and featured
@public.route('/')
def home():
    return render_template('public/homepage.html')

@public.route('/issues')
def showIssues():
    try:
        c, conn = connection()
        c.execute("SELECT * FROM techBoard.issue WHERE active = 1;")
        result_set = c.fetchall()
        conn.close()

        return render_template('public/issues.html', issues=result_set)

    except Exception as e:
        return str(e)

    
