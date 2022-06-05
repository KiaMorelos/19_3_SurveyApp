from flask import Flask, request, render_template, redirect, flash, session 

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey 

app = Flask(__name__)

app.config['SECRET_KEY'] = "its_a_secret_to_everybody"

debug = DebugToolbarExtension(app)

num_of_qs = len(satisfaction_survey.questions)

@app.route('/')
def root():
    """Root Route, show user the title of the survey, instructions"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("index.html", title=title, instructions=instructions)

@app.route('/start-survey', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:question_num>')
def show_questions(question_num):
    """If requested question exists and hasn't yet been answered how current question"""
    responses = session['responses']
    num_res = len(responses)

    if question_num > num_res:
        flash("the question you tried to access was invalid")
        return redirect(f"/questions/{num_res}")
    if question_num == num_of_qs and num_res:
         flash("you already answered all questions")
         return redirect("/thanks")
    
    question = satisfaction_survey.questions[question_num].question
    choices = satisfaction_survey.questions[question_num].choices
   
    if  num_res != question_num:
        return redirect(f"/questions/{num_res}")
   
    else:
        return render_template("questions.html", question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def next_question():
    """Store answer, and redirect to next unanswerd question"""
    answer = request.form["choice"]
   
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    num_res = len(responses)
    if  num_res == 0:
        return redirect("/questions/0")
    elif  num_res == num_of_qs and len(responses)is not 0:
        return redirect("/thanks")
    else:
        nextq =  num_res
        return redirect(f"/questions/{nextq}")

@app.route('/thanks')
def thankyou():
    """Render html page that thanks users for filling out survey"""
    return render_template("thanks.html")