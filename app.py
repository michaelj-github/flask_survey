from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import datetime
import surveys
from random import randint
app = Flask(__name__)
app.config['SECRET_KEY'] = "mjm34442"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)
sessionkey = str(datetime.datetime.now())
# print(sessionkey)
responses  = []

surveytype = ''
qnum = 0
storeqnum = 0

@app.route('/')
def index():
    """Home Page"""
    return render_template("home.html")

@app.route('/startpage')
def start():
    """Start Page"""
    global surveytype
    global storeqnum
    responses = []
    session[sessionkey] = []
    qnum = 0
    storeqnum = 0
    surveytype = request.args["survey"] # for future use
    if surveytype == "satisfaction":
        thesurvey = surveys.satisfaction_survey
    # elif surveytype == "personality":
    #     # thesurvey = surveys.personality_quiz
    #     thesurvey = surveys.satisfaction_survey
    # else:
    #     # thesurvey = surveys.anewsurvey
    #     thesurvey = surveys.satisfaction_survey
    # print(thesurvey.questions[0].question)
    # print(surveytype, thesurvey, qnum)
    return render_template("startpage.html", qnum=qnum, thesurvey = thesurvey)


@app.route('/question/<int:qnum>')
def question(qnum):
    """Question Page"""

    global storeqnum
    if qnum != storeqnum:
        flash("Questions must be answered in order.")
        qnum = storeqnum
    return render_template("question.html", qnum=qnum, thequestions = surveys.satisfaction_survey.questions)

@app.route('/answer/<int:qnum>', methods=["POST"])
def answer(qnum):
    """Answer Page"""
    theanswer = request.form['answer']
    responses = session[sessionkey]
    responses.append(theanswer)
    session[sessionkey] = responses
    # print(responses)
    # if qnum > 2:
    #     raise
    global storeqnum
    qnum += 1
    storeqnum += 1
    return render_template("answer.html", theanswer=theanswer, qnum=qnum, thequestions = surveys.satisfaction_survey.questions)
