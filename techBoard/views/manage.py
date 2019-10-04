# views/manage.py

# This view contains all of the resources for managing views


import sys
sys.path.append("..")
from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, BooleanField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional, Length
from techBoard.models.Issue import Issue

from techBoard.models.DBase import connection


# set blueprint
manage = Blueprint('manage', __name__)

# routes
# ========================================


@manage.route('/manage')
@login_required
def manageIssues():
    try:
        c, conn = connection()
        c.execute("SELECT * FROM techBoard.issue WHERE active = 1 OR CURRENT_DATE - modified_date <= 7 ORDER BY created_date DESC;")
        result_set = c.fetchall()
        conn.close()

        return render_template('manage/manageIssues.html', issues=result_set)

    except Exception as e:
        return str(e)

@manage.route('/manage/<int:issueID>', methods=['GET','POST'])
@login_required
def editIssue(issueID):
    # Initialize the form 
    form = issueForm()
    # Attempt to fetch the record
    issue = Issue()
    issue.issueID = issueID
    result = issue.fetch()

    if form.validate_on_submit():
        issue.title = form.title.data
        issue.description = form.description.data
        issue.status = form.status.data
        issue.instructionBox = int(form.instructionBox.data)
        issue.instructions = form.instructions.data
        issue.active = int(form.active.data)
        # Attempt to store the issue
        result = issue.update()
        if result == True:
            return redirect(url_for("manage.manageIssues"))
        else:
            return "<h1>OOPS</h1><p>Something has gone utterley and terribly wrong. {}</p>".format(str(result))


    if result:
        form.title.data = issue.title 
        form.description.data = issue.description
        form.status.data = issue.status 
        form.instructionBox.data = issue.instructionBox
        form.instructions.data = issue.instructions
        form.active.data = issue.active

        return render_template('manage/issue.html', form=form)

    return "Error: Could not find the record"


@manage.route('/manage/create', methods=['GET','POST'])
@login_required
def createIssue():
    form = issueForm()

    if form.is_submitted():
        if form.validate():
            # Process the data 
            issue = Issue()
            issue.title = form.title.data
            issue.description = form.description.data
            issue.status = form.status.data
            issue.instructionBox = int(form.instructionBox.data)
            issue.instructions = form.instructions.data
            issue.active = int(form.active.data)
            # Attempt to store the issue
            result = issue.store()
            if result == True:
                return redirect(url_for("manage.manageIssues"))
            else:
                return "<h1>OOPS</h1><p>Something has gone utterley and terribly wrong. {}</p>".format(str(result))
        else:
            return "Did not validate"


    return render_template('manage/issue.html', form=form)

    


class issueForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired()])
    status = SelectField("Status: ",choices=[('Still Effecting','Still Effecting'),('Workaround','Workaround'),('Resolved','Resolved')], validators=[DataRequired()])
    instructionBox = BooleanField("Include Instructions: ")
    instructions = TextAreaField("Instructions: ")
    active = BooleanField("Active: ")
    submit = SubmitField("Submit")