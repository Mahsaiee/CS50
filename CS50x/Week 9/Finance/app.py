import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)
    cash_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    if cash_left and "cash" in cash_left[0]:
        cash_left = float(cash_left[0]["cash"])
    else:
        cash_left = 0.0

    total_amount = cash_left

    try:
        for stock in portfolio:
            symbol = stock["symbol"]
            stock_info = lookup(symbol)

            current_price = float(stock_info["price"])
            stock_value = current_price * stock["shares"]

            stock.update({"current_price": current_price, "stock_value": stock_value})
            total_amount += float(stock["stock_value"])
    except (ValueError, LookupError):
        return apology("Failed to update stock prices!")

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash_left=cash_left,
        total_amount=total_amount,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("Invalid Symbol")

        if not shares.isdigit():
            return apology("Number of shares must be a positive digit!")

        shares = int(shares)

        if shares <= 0:
            return apology("Number of shares must be a positive digit!")

        stock = lookup(symbol)

        if not stock:
            return apology("Invalid symbol.")

        price_per_share = stock["price"]
        total_cost = price_per_share * shares

        cash_result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if not cash_result or "cash" not in cash_result[0]:
            return apology("Failed to retrieve cash balance.")

        cash_balance = cash_result[0]["cash"]

        if total_cost > cash_balance:
            return apology("Insufficient funds for this transaction.")

        new_cash_balance = cash_balance - total_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)

        timestamp = datetime.datetime.now()
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            user_id,
            symbol,
            shares,
            price_per_share,
            timestamp,
        )


        portfolio = db.execute(
            "SELECT * FROM portfolios WHERE user_id = ? AND symbol = ?", user_id, symbol
        )

        if portfolio:
            updated_shares = portfolio[0]["shares"] + shares
            db.execute(
                "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                updated_shares,
                user_id,
                symbol,
            )
        else:
            db.execute(
                "INSERT INTO portfolios (user_id, symbol, shares) VALUES (?, ?, ?)",
                user_id,
                symbol,
                shares,
            )

        flash("Stock purchased successfully!")

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price NUMERIC NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
"""
    )
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id,
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        """Get stock quote."""
        if not symbol:
            return apology("Symbol is required.")

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol.")
        stock["price"] = usd(stock["price"])
        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        """Register user"""
        if not username or not password or not confirmation:
            return apology("All fields must be filled.")

        if password != confirmation:
            return apology("Passwords do not match.")

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists.")

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        """Sell shares of stock"""
        if not symbol or shares <= 0:
            return apology("Invalid symbol or shares value.")

        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid symbol.")

        user_id = session["user_id"]

        portfolio = db.execute(
            "SELECT * FROM portfolios WHERE user_id = ? AND symbol = ?", user_id, symbol
        )

        if not portfolio or portfolio[0]["shares"] < shares:
            return apology("Insufficient shares for this transaction.")

        updated_shares = portfolio[0]["shares"] - shares

        db.execute(
            "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
            updated_shares,
            user_id,
            symbol,
        )

        price = stock["price"]
        total_sale = price * shares

        cash_result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        if not cash_result or "cash" not in cash_result[0]:
            return apology("Failed to retrieve cash balance.")

        cash_balance = cash_result[0]["cash"]
        new_cash_balance = cash_balance + total_sale

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)

        timestamp = datetime.datetime.now()

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            user_id,
            symbol,
            -shares,
            price,
            timestamp,
        )

        flash("Stock sold successfully!")

        return redirect("/")

    user_id = session["user_id"]

    portfolio = db.execute(
        "SELECT symbol, shares FROM portfolios WHERE user_id = ?", user_id
    )

    return render_template("sell.html", portfolio=portfolio)
