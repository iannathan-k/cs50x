import os
import time
import google.generativeai as genai

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from markdown import markdown


# Configure application
app = Flask(__name__)

genai.configure(api_key=os.environ["API_KEY"])
#model = genai.GenerativeModel('gemini-1.5-flash')
model = genai.GenerativeModel(model_name="gemini-1.5-pro")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

TRIVIA_COUNT = 3
HIGH_SCORE_COUNT =10
MOST_RECENT_QUESTIONS = 8
EPOCH = 40246871

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show landing page"""
    return render_template("index.html")


@app.route("/trivia", methods=["GET", "POST"])
@login_required
def trivia():
    """Show trivia page"""

    # prompt for GenAI to generate trivia questions
    str = "Provide random %d as-level chemistry questions, followed by the answer. Prefix \
        each question with **QQ** and each answer with **AA**." % TRIVIA_COUNT

    response = model.generate_content(str)
    text = response.text
    qqaas = parseQuestionAnswer(text)

    # Insert stats entry for the given batchid, all unanswered initially
    user_id = session["user_id"]
    batchid = int(time.time())
    db.execute("INSERT INTO stats(user_id, timestamp, batchid, unanswered) VALUES (?, ?, ?, ?)",
               user_id, time.time(), batchid, TRIVIA_COUNT)

    return render_template("trivia.html", qqaas=qqaas, batchid=batchid)


@app.route("/ama", methods=["GET", "POST"])
@login_required
def ama():
    """Show Ask Me Anything page"""

    user_id = session["user_id"]
    if request.method == "POST":
        question = request.form.get("question").strip()
        if (question is None or len(question) == 0):
            return apology("Missing question!")

        response = fetch_ama_response(question)
        return render_template("ama_done.html", question=question, answer=markdown(response))

    else:
        questionid = request.args.get("questionid")
        if not questionid:
            type = request.args.get("type")
            orderby = "timestamp"
            if type == "frequent":
                orderby = "counter"
            rows = db.execute("SELECT id, question FROM history WHERE user_id=? ORDER BY %s DESC \
                              LIMIT ?" % orderby, user_id, MOST_RECENT_QUESTIONS)
            questions = []
            for row in rows:
                questions.append((row["id"], row["question"]))
            return render_template("ama.html", questions=questions)

        else:
            rows = db.execute("SELECT question FROM history WHERE id=?", questionid)
            if len(rows) == 0:
                return apology("Question not found", 500)
            question = rows[0]["question"]
            response = fetch_ama_response(question)
            return render_template("ama_done.html", question=question, answer=markdown(response))


def fetch_ama_response(question):
    response = model.generate_content(question)
    text = response.text

    user_id = session["user_id"]
    rows = db.execute("SELECT id, counter FROM history WHERE user_id=? AND question=?", user_id, question)
    if len(rows) == 0:
        db.execute("INSERT INTO history(user_id, question, timestamp) VALUES (?, ?, ?)",
                   user_id, question, time.time())
    else:
        id = rows[0]["id"]
        counter = rows[0]["counter"]
        counter = counter + 1
        db.execute("UPDATE history SET counter=?, timestamp=? WHERE id=?", counter, time.time(), id)

    print("##[[%s]]##" % text)
    return text


@app.route("/stats")
@login_required
def stats():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute("SELECT SUM(correct) AS correct, SUM(incorrect) AS incorrect, SUM(unanswered) \
                      AS unanswered FROM stats WHERE user_id=?", user_id)
    if len(rows) != 1:
        print("[error] invalid param_correct %s" % param_correct)
        return apology("Multiple users detected %d", user_id)
    correct = rows[0]["correct"]
    incorrect = rows[0]["incorrect"]
    unanswered = rows[0]["unanswered"]

    start = EPOCH
    dur = request.args.get("dur")
    if dur == "24h":
        start = int(time.time()) - 86400
    elif dur == "hour":
        start = int(time.time()) - 3600

    rows = db.execute("SELECT b.username AS aa, SUM(correct) AS bb, SUM(incorrect) AS cc, \
                      SUM(unanswered) AS dd FROM stats a, users b WHERE a.user_id=b.id \
                      AND timestamp >= ? GROUP BY aa ORDER BY bb DESC LIMIT ?", start, HIGH_SCORE_COUNT)
    values = []
    for row in rows:
        aa = row["aa"]
        bb = row["bb"]
        cc = row["cc"]
        dd = row["dd"]
        values.append((aa, bb, cc, dd))

    return render_template("stats.html", values=values, correct=correct, incorrect=incorrect, unanswered=unanswered)


@app.route("/grading", methods=["GET", "POST"])
@login_required
def grading():
    if request.method == "GET":
        print("[error] grading GET, do nothing")
        return ['ok']

    batchid = request.form.get("batchid")
    if not batchid:
        print("[error] batchid not provided, skipping..")
        return ['ok']

    param_correct = request.form.get("correct")
    if param_correct != "1" and param_correct != "0":
        print("[error] invalid param_correct %s" % param_correct)
        return ['ok']

    user_id = session["user_id"]
    print("batchid %s, param_correct = %s" % (batchid, param_correct))

    rows = db.execute(
        "SELECT correct, incorrect, unanswered FROM stats WHERE user_id=? AND batchid=?",
            user_id, batchid)
    if len(rows) != 1:
        print("[error] stats not found for user %d" % user_id)
        return ['ok']

    correct = rows[0]["correct"]
    incorrect = rows[0]["incorrect"]
    unanswered = rows[0]["unanswered"]
    if param_correct == "1":
        correct = correct + 1
    else:
        incorrect = incorrect + 1
    unanswered = unanswered - 1

    db.execute("UPDATE stats SET correct=?, incorrect=?, unanswered=? WHERE user_id=? AND batchid=?",
               correct, incorrect, unanswered, user_id, batchid)
    return ['ok']


def parseQuestionAnswer(text):
    """Parse list of questions ans answers from GenAI"""

    tokenQQ = "**QQ**"
    tokenAA = "**AA**"
    qqaas = []
    items = text.split(tokenQQ)
    for item in items:
        parts = item.split(tokenAA)
        if len(parts) <= 1: # skip any chars before first QQ
            continue
        question = parts[0].strip()
        answer = parts[1].strip()
        qqaas.append((markdown(question), markdown(answer)))

        # print("QQ: [%s]" % question)
        # print("AA: [%s]" % answer)

    return qqaas


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Login successful")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        confirmation = request.form.get("confirmation").strip()
        passwordHash = generate_password_hash(password)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        if confirmation != password:
            return apology("password confirmation doesn't match", 400)

        try:
          db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, passwordHash)
        except ValueError:
            return apology("Username already exists, please log in instead")
        except Exception as error:
            return apology("Error %s in registration" % error, 400)

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/chgpwd", methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password"""
    if request.method == "POST":
        user_id = session["user_id"]

        currpwd = request.form.get("currpwd").strip()
        newpwd1 = request.form.get("newpwd1").strip()
        newpwd2 = request.form.get("newpwd2").strip()
        if newpwd1 == "" or newpwd2 == "":
            return apology("New password is empty", 400)
        elif newpwd1 != newpwd2:
            return apology("New password confirmation does not match", 400)

        # Query database for username
        rows = db.execute("SELECT hash FROM users WHERE id=?", user_id)
        if len(rows) != 1:
            return apology("Internal error", 500)
        if not check_password_hash(rows[0]["hash"], currpwd):
            return apology("Current password is wrong")

        try:
          db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(newpwd1), user_id)
        except Exception as error:
            return apology("Error %s in password change" % error, 500)

        flash("Password changed successfully")
        return redirect("/")

    else:
        return render_template("chgpwd.html")



# CREATE TABLE sqlite_sequence(name,seq);

# CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     username TEXT NOT NULL,
#     hash TEXT NOT NULL
# );
# CREATE INDEX idx_username ON users(username);

# CREATE TABLE history (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     user_id INTEGER NOT NULL,
#     question TEXT NOT NULL,
#     counter INTEGER NOT NULL DEFAULT 1,
#     timestamp TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# CREATE INDEX idx_history_user ON history(user_id, timestamp);

# CREATE TABLE stats (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     user_id INTEGER NOT NULL,
#     timestamp TIMESTAMP,
#     batchid VARCHAR(10) NOT NULL,
#     correct INTEGER NOT NULL DEFAULT 0,
#     incorrect INTEGER NOT NULL DEFAULT 0,
#     unanswered INTEGER NOT NULL DEFAULT 0,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# CREATE INDEX idx_stats_user ON stats(user_id, timestamp);
