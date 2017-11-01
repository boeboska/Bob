# Problem Set 7
# Name: Bob Borsboom
# CS50
#
# Warning: timezone = UTC: https://www.timeanddate.com/time/zones/cest
#
# A website via which users can “buy” and “sell” stocks (including "loan")

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """index shares of stock."""

    # get information from index database where amount is summed and grouped by symbol for current user
    index_info = db.execute("SELECT *, SUM(amount) FROM 'index' WHERE id = :id GROUP BY symbol",
    id = session['user_id'])

    share_amount_user = 0

    for row in range(len(index_info)):

        # retreive all the information from the index database per symbol
        symbol_info = lookup(index_info[row]["symbol"])

        # calculate the total value per sort share
        total = float(symbol_info["price"]) * index_info[row]["SUM(amount)"]

        # add the information for the html page
        index_info[row]["price"] = usd(symbol_info["price"])
        index_info[row]["price2"] = usd(total)

        share_amount_user += total

    # calculate the users' cash
    user_cash = db.execute("SELECT * FROM users WHERE id = :id", id = session['user_id'])
    cash = user_cash[0]["cash"]

    share_amount_user += cash

    # display the index to the user
    return render_template("index.html", index_info = index_info, cash = usd(cash),
    share_amount_user = usd(share_amount_user))

@app.route("/loan", methods=["GET", "POST"])
@login_required
def loan():
    """get extra cash."""

    # get cash from user
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session['user_id'])[0]["cash"]

    if request.method == "POST":

        # check if all the fields are filled in
        if request.form.get("borrow")== "":
            return apology("fill in the amount you want to borrow")

        # check is amount is numeric
        if not request.form.get("borrow").isdigit():
            return apology("Enter only numbers")

        # check is amout is greater than 0
        if int(request.form.get("borrow")) <= 0:
            return apology("Enter only positive numbers")

        # update cash with loan
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id", id = session['user_id'],
        cash = request.form.get("borrow"))

        # display the index to the user
        return redirect(url_for("index"))

    else:
        return render_template("loan.html", cash = usd(cash))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    if request.method == "POST":

        # check if all the fields are filled in
        if request.form.get("symbol")== "" or request.form.get("amount") == "":
            return apology("Fill in all the fields")

        # retreive share info
        share_info = lookup(request.form.get("symbol"))
        if not share_info:
            return apology("Coun't find the share")

        # retreive share name
        share_name = share_info["name"]

        # retreive share price
        share_price = float(share_info["price"])

        # check if amount is numeric
        if not request.form.get("amount").isdigit():
            return apology("Enter only numbers")

        # calculate transaction value
        waarde_transactie = share_price * int((request.form.get("amount")))

        # check if transaction value is positive
        if waarde_transactie <= 0:
            return apology("Enter a number greater than zero")

        # retreive users' info
        user = db.execute("SELECT * FROM users WHERE id = :id", id = session['user_id'])

        # check if user has enough cash for transaction
        if waarde_transactie > user[0]["cash"]:
            return apology("You don't have enough cash for this transaction")

        else:
            # insert transaction in database history
            db.execute("INSERT INTO history (symbol, price, amount, id, name, total) VALUES(:symbol, :price, :amount, :id, :name, :total)",
            symbol = request.form.get("symbol").upper(), price = usd(share_price),
            amount = request.form.get("amount"), id = session['user_id'],
            name = share_name, total = waarde_transactie)

            # decrease users' cash
            db.execute("UPDATE users SET cash = cash - :cash WHERE id = :id",
            id = session['user_id'], cash = waarde_transactie)

            # check if share is already in property
            check_leeg = db.execute("SELECT * FROM 'index' WHERE id = :id AND symbol = :symbol",
            id = session['user_id'], symbol = request.form.get("symbol"))
            if not check_leeg:

                # if share is not in property yet, insert transaction in database index
                db.execute("INSERT INTO 'index' (symbol, price, amount, id, name) VALUES(:symbol, :price, :amount, :id, :name)",
                symbol = request.form.get("symbol").upper(),
                price = share_price, amount = request.form.get("amount"),
                id = session['user_id'], name = share_name)

            else:
                # update index database with transaction
                db.execute("UPDATE 'index' SET amount = amount + :amount WHERE id = :id AND symbol = :symbol",
                id = session['user_id'],
                symbol = request.form.get("symbol"),
                amount = request.form.get("amount"))

        # display the index to the user
        return redirect(url_for("index"))

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    # retreive history information
    history = db.execute("SELECT * FROM history WHERE id = :id", id = session['user_id'])

    # display the history to the user
    return render_template("history.html", history= history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("Invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("quote"))


    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # check if all the fields are filled in
        if request.form.get("symbol")== "":
            return apology("Fill in the quote field")

        # check if share exist
        share_info = lookup(request.form.get("symbol"))
        if not share_info:
            return apology("Couln't find the share")

        # retreiving shares' price
        price = share_info["price"]

        # display the shares' price to the user
        return render_template("quote_weergeven.html", share_info = share_info, price = usd(price))

    else:
        return render_template("quote_zoeken.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":

        # check if all the fields are filled in
        if request.form.get("username")== "" or request.form.get("password") == "" or request.form.get("confirm_password") == "":
            return apology("Fill in all the fields")

        # check if the password is equal to confirm_password
        if not request.form.get("password") == request.form.get("confirm_password"):
             return render_template("apology2.html")

        # check if username is new
        result = db.execute("INSERT INTO users (username, hash)  VALUES(:username, :hash)",
        username=request.form.get("username"),
        hash=pwd_context.hash(request.form.get("password")))
        if not result:
            return apology("Username already exist")

        # logging the user in
        session["user_id"]= result

        # display the index to the user
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == "POST":

        # retreiving shares' symbol
        aandeel_verkoop = request.form.get("symbol").upper()

        # check if share is in property
        share_info = lookup(aandeel_verkoop)
        if not share_info:
            return apology("You don't have this share in property")

        # retreiving shares'price
        share_price = float(share_info["price"])

        # retreiving shares' name
        share_name = share_info["name"]

        # check if all the fields are filled in
        if request.form.get("symbol")== "" or request.form.get("amount") == "":
            return apology("Fill in all the fields")

        # check if amount input is digit
        if not request.form.get("amount").isdigit():
            return apology("Enter only numbers")

        # check if share is in property
        user = db.execute("SELECT * FROM 'index' WHERE id = :id AND symbol = :symbol",
        id = session['user_id'], symbol = aandeel_verkoop)
        if not user:
            return apology("You don't have this share")

        # select sum amount per share sort
        aantal_shares = db.execute("SELECT SUM(amount) FROM 'index' WHERE id = :id AND symbol = :symbol",
        id = session['user_id'], symbol = aandeel_verkoop)

        shares = aantal_shares[0]["SUM(amount)"]

        # check if sell-amount is in property
        if int(request.form.get("amount")) > shares:
            return apology("you don't have enough shares for this transaction")

        # calculate transaction value
        waarde_transactie = share_price * int((request.form.get("amount")))

        # check if transaction is negative
        if waarde_transactie <= 0:
            return apology("Only numbers greater than 0")

        # insert transaction into history database
        db.execute("INSERT INTO history (symbol, price, amount, id, name, total)  VALUES(:symbol, :price, :amount, :id, :name, :total)",
        symbol = request.form.get("symbol").upper(), price = usd(share_price),
        amount = -float(request.form.get("amount")), id = session['user_id'],
        name = share_name, total = waarde_transactie)

        # increase user's cash with transaction value
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :id",
        id = session['user_id'], cash = waarde_transactie)

        # check if user sells all his shares per sort
        if int(request.form.get("amount")) < shares:

            # update index database with transaction
            db.execute("UPDATE 'index' SET amount = amount - :amount WHERE id = :id AND symbol = :symbol",
            id = session['user_id'], symbol = request.form.get("symbol").upper(), amount = request.form.get("amount"))

        else:
            # delete share from index database
            db.execute("DELETE FROM 'index' WHERE id = :id AND symbol = :symbol",
            id = session['user_id'], symbol = request.form.get("symbol").upper())

        # display the index to the user
        return redirect(url_for("index"))

    else:
        return render_template("sell.html")
