import os
import time
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
# app.logger.setLevel(50) #ERROR


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    return render_template("index.html")

@app.route("/trivia")
@login_required
def trivia():
    """Show portfolio of stocks"""
    # dict(sorted(x.items(), key=lambda item: item[1]))

    user_id = session["user_id"]
    rows = db.execute("SELECT cash from users WHERE id=?", user_id)
    if len(rows) != 1:
        return apology("Fatal error, user doesn't exist", 500)
    cash = rows[0]["cash"]
    total = float(cash)

    values = dict()
    rows = db.execute("SELECT * from stock_balance WHERE user_id=?", user_id)
    for row in rows:
        symbol = row["symbol"]
        quantity = row["quantity"]
        value = lookup(symbol)
        if (value is None):
            print("Symbol %s is an invalid symbol, skipping.." % symbol)
            continue
        amount = float(quantity) * value["price"]
        total = total + amount
        values[symbol.upper()] = (quantity, value["price"], amount)

    # sort by Market Value desc
    sorted_values = dict(sorted(values.items(), key=lambda item: item[1][2], reverse=True))

    return render_template("trivia.html", values=sorted_values, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").strip()
        if not symbol:
            return apology("must provide Symbol", 400)
        symbol = symbol.upper()
        try:
          shares = int(request.form.get("shares").strip())
        except ValueError:
            return apology("invalid num of shares", 400)
        if not shares:
            return apology("must provide num of shares", 400)
        if shares <= 0:
            return apology("Invalid num of shares", 400)

        value = lookup(symbol)

        if (value is None):
            return apology("invalid Symbol", 400)

        user_id = session["user_id"]
        price = value['price']
        amount = float(shares) * price

        # ensure there is enough fund
        rows = db.execute("SELECT id, cash FROM users WHERE id=?", user_id)
        if len(rows) != 1:
            return apology("unknown error in updating user's balance, %d" % len(rows), 500)
        available_cash = rows[0]["cash"]
        if amount > available_cash:
            return apology("insufficient fund to buy", 400)

        # record the transaction
        try:
            sql = "INSERT INTO transactions (user_id, type, symbol, quantity, price, amount, timestamp) \
                VALUES(?, ?, ?, ?, ?, ?, ?)"
            db.execute(sql, user_id, "BUY", symbol, shares, price, amount, time.time())
        except:
            return apology("unknown error in recording txn", 500)

        # update the stock_balance
        rows = db.execute("SELECT quantity from stock_balance WHERE user_id=? AND symbol=?", user_id, symbol)
        if len(rows) == 0:
            db.execute("INSERT INTO stock_balance (user_id, symbol, quantity) VALUES (?, ?, ?)", user_id, symbol, shares)
        elif len(rows) == 1:
            shares = shares + rows[0]["quantity"]
            db.execute("UPDATE stock_balance set quantity=? WHERE user_id=? AND symbol=?", shares, user_id, symbol)
        else:
            return apology("unknown error in updating stock balance, %d" % len(rows), 500)

        # update user's balance
        available_cash = available_cash - amount
        db.execute("UPDATE users SET cash=? WHERE id=?", available_cash, user_id)

        flash("Bought")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = []
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC", user_id)
    for row in rows:
        type = row["type"]
        symbol = row["symbol"]
        quantity = row["quantity"]
        value = lookup(symbol)
        if (value is None):
            print("Symbol %s is an invalid symbol, skipping.." % symbol)
            continue
        amount = float(quantity) * value["price"]

        dt = datetime.fromtimestamp(row["timestamp"])
        dtime = "%s-%02d-%02d %02d:%02d:%02d" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        data.append((dtime, type, symbol, quantity, value["price"], amount))

    return render_template("history.html", data=data)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol").strip()
        if not symbol:
            return apology("must provide Stock symbol", 400)
        value = lookup(symbol)
        if (value is None):
            return apology("invalid Stock symbol", 400)
        return render_template("quoted.html", symbol=value['symbol'], price=value['price'])
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol or symbol == "":
            return apology("must choose a symbol", 400)
        symbol = symbol.upper()
        try:
          shares = int(request.form.get("shares").strip())
        except ValueError:
            return apology("invalid num of shares", 400)
        if not shares:
            return apology("must provide num of shares", 400)
        if shares <= 0:
            return apology("Invalid num of shares", 400)

        value = lookup(symbol)
        if (value is None):
            return apology("invalid Symbol", 400)

        price = value['price']
        amount = float(shares) * price

        # validate availability
        rows = db.execute("SELECT quantity from stock_balance WHERE user_id=? AND symbol=?", user_id, symbol)
        if len(rows) > 1:
            return apology("unknown error in updating stock balance, %d" % len(rows), 500)
        elif len(rows) == 0 or rows[0]["quantity"] == 0:
            return apology("can't sell, no %s shares" % symbol, 400)

        curr_shares = rows[0]["quantity"]
        if shares > curr_shares:
            return apology("not enough shares, %s vs %s" % (shares, curr_shares), 400)

        # record the transaction
        try:
            sql = "INSERT INTO transactions (user_id, type, symbol, quantity, price, amount, timestamp) \
                VALUES(?, ?, ?, ?, ?, ?, ?)"
            db.execute(sql, user_id, "SELL", symbol, shares, price, amount, time.time())
        except:
            return apology("unknown error in recording txn", 500)

        # subtract the quantity
        curr_shares = curr_shares - shares
        if curr_shares > 0:
            db.execute("UPDATE stock_balance set quantity=? WHERE user_id=? AND symbol=?", curr_shares, user_id, symbol)
        else:
            db.execute("DELETE FROM stock_balance WHERE user_id=? AND symbol=?", user_id, symbol)

        # update user's balance
        rows = db.execute("SELECT id, cash FROM users WHERE id=?", user_id)
        if len(rows) == 1:
            cash = rows[0]["cash"]
            cash = cash + amount
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, user_id)
        else:
            return apology("unknown error in updating user's balance", 500)

        flash("Sold")
        return redirect("/")

    else:
        stocks = []
        rows = db.execute("SELECT symbol FROM stock_balance WHERE user_id=? ORDER BY symbol ASC", user_id)
        for row in rows:
            stocks.append(row["symbol"])
        return render_template("sell.html", stocks=stocks)


# CREATE TABLE transactions (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     user_id INTEGER NOT NULL,
#     type VARCHAR(4),
#     symbol VARCHAR(12),
#     quantity INTEGER NOT NULL,
#     price NUMERIC NOT NULL,
#     amount NUMERIC NOT NULL,
#     timestamp TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# CREATE INDEX txn_userid ON transactions(user_id);

# CREATE TABLE stock_balance (
#     user_id INTEGER NOT NULL,
#     symbol VARCHAR(12),
#     quantity INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# CREATE INDEX sb_userid_symbol ON stock_balance(user_id, symbol);
