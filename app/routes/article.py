from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app import app, mysql
from app.forms import ArticleForm
from app.decorators import login_required
from datetime import datetime
import os
from playwright.sync_api import sync_playwright
article_bp = Blueprint("article",__name__)


@article_bp.route("/addarticle", methods=["GET", "POST"])
@login_required
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        url = form.url.data
        content = form.content.data
        author = session['username']
        sql = "INSERT INTO articles(title,url,author,content) VALUES (%s,%s,%s,%s)"
        cur = mysql.connection.cursor()
        cur.execute(sql, (title, url, author, content))
        mysql.connection.commit()
        cur.close()
        flash("Yeni makale başarı ile eklendi..", "info")
        return redirect(url_for("main.dashboard"))
    return render_template("addarticle.html", form=form)

@article_bp.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    s = "SELECT * FROM articles WHERE id=%s"
    result = cursor.execute(s, (id,))
    if result > 0:
        article = cursor.fetchone()
        screenshot_filename = capture_screenshot(article["url"])
        return render_template("article.html", article=article, screenshot_filename=screenshot_filename)
    else:
        return render_template("article.html")

def capture_screenshot(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot_path = os.path.join('static', 'screenshots', filename)
            os.makedirs(os.path.join('static', 'screenshots'), exist_ok=True)
            page.screenshot(path=screenshot_path)
            browser.close()
            return filename
    except Exception as e:
        return f"Hata: {str(e)}"

@article_bp.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    s = "SELECT * FROM articles WHERE author = %s and id = %s"
    result = cursor.execute(s, [session["username"], id])
    if result > 0:
        s2 = "DELETE FROM articles WHERE id = %s"
        cursor.execute(s2, (id,))
        mysql.connection.commit()
        return redirect(url_for("main.dashboard"))
    else:
        flash("Böyle bir makale yok veya yetkiniz yok.", "danger")
        return redirect(url_for("main.index"))

@article_bp.route("/update/<string:id>", methods=["GET", "POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        s1 = "SELECT * FROM articles WHERE id=%s AND author=%s;"
        result = cursor.execute(s1, (id, session["username"]))
        if result == 0:
            flash("Böyle bir makale yok veya yetkiniz yok.", "danger")
            return redirect(url_for("main.index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html", form=form)
    else:
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        s = "UPDATE articles SET title = %s, content = %s WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(s, (newTitle, newContent, id))
        mysql.connection.commit()
        flash("Article Updated Successfully", "success")
        return redirect(url_for("main.dashboard"))

@article_bp.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    s = "SELECT * FROM articles"
    result = cursor.execute(s)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html", articles=articles)
    else:
        return render_template("articles.html")

@article_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("main.index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sql = "select * from articles where title like '%" + str(keyword) + "%' "
        result = cursor.execute(sql)
        if (result == 0):
            flash("Böyle bir makale bulunmuyor.", "danger")
            return redirect(url_for("article.articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html", articles=articles)
