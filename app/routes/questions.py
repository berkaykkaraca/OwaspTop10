from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.forms import QuestionForm, AnswerForm
from app.decorators import login_required

question_bp = Blueprint("question",__name__)

@question_bp.route("/askquestion", methods=["GET", "POST"])
@login_required
def askQuestion():
    form = QuestionForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        question = form.question.data
        author = session["username"]
        sql = "INSERT INTO questions(author,title,question) VALUES (%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(sql, (author, title, question))
        mysql.connection.commit()
        cur.close()
        flash("Yeni soru başarıyla eklendi.", "info")
        return redirect(url_for("question.questions"))
    return render_template("askquestion.html", form=form)

@question_bp.route("/questions")
def questions():
    cursor = mysql.connection.cursor()
    s = "SELECT * FROM questions"
    result = cursor.execute(s)
    if result > 0:
        questions = cursor.fetchall()
        return render_template("questions.html", questions=questions)
    else:
        return render_template("questions.html")

@question_bp.route("/question/<string:id>")
def question(id):
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()

    s = "SELECT * FROM questions WHERE question_id=%s"
    result = cursor.execute(s, (id,))
    s2 = "SELECT * FROM answers WHERE question_id=%s"
    result2 = cursor2.execute(s2, (id,))

    if result > 0:
        answers = cursor2.fetchall()
        question = cursor.fetchone()
        return render_template("question.html", question=question, answers=answers)
    else:
        return render_template("question.html")

@question_bp.route("/answer/<string:id>", methods=["GET", "POST"])
@login_required
def answer(id):
    form = AnswerForm(request.form)
    cur2 = mysql.connection.cursor()
    s = "SELECT * FROM questions WHERE question_id = %s"
    result1 = cur2.execute(s, (id,))
    q = cur2.fetchone()
    if request.method == "POST" and form.validate():
        author = session['username']
        answer = form.answer.data
        question_id = id

        sql = "INSERT INTO answers(author,answer,question_id) VALUES (%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(sql, (author, answer, question_id))
        mysql.connection.commit()
        cur.close()
        flash("Cevabınız başarıyla eklendi.", "info")
        return redirect(url_for("question.questions"))
    return render_template("answer.html", form=form, q=q)

@question_bp.route("/searchquestion", methods=["GET", "POST"])
def searchQuestion():
    if request.method == "GET":
        return redirect(url_for("main.index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sql = "select * from questions where title like '%" + str(keyword) + "%' "
        result = cursor.execute(sql)
        if result == 0:
            flash("Böyle bir makale bulunmuyor.", "danger")
            return redirect(url_for("question.questions"))
        else:
            questions = cursor.fetchall()
            return render_template("questions.html", questions=questions)
