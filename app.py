import os
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

import google.generativeai as genai


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
def index(s="", p="", q="", ss="", pp="", qq=""):
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]
    qnty = db.execute(
        "SELECT symbol, SUM(purchase_quantity) AS qty FROM purchases WHERE user_id = ? GROUP BY symbol",
        session["user_id"],
    )
    tv_holding = 0
    for i in qnty:
        quoted = lookup(i["symbol"])
        if quoted is None:
            return apology("Invalid symbol or API unavailable")
        cost = quoted["price"]
        sym = quoted["symbol"]
        quant = i["qty"]
        i["curr_price"] = usd(cost)
        i["total_value"] = cost * quant
        tv_holding += i["total_value"]
        i["total_value"] = usd(cost * quant)

    grand_total = usd(cash + tv_holding)
    cash = usd(cash)

    return render_template(
        "index.html",
        qnty=qnty,
        cash=cash,
        grand_total=grand_total,
        sym=s,
        price=p,
        qty=q,
        s_sym=ss,
        s_price=pp,
        s_qty=qq,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        qty = request.form.get("shares")
        if qty == "":
            return apology("Bruh...")
        try:
            qty = float(qty)
            if qty - int(qty) != 0:
                return apology("Enter a valid number")
        except:
            if not qty.isdigit():
                return apology("Enter a valid number")

        qty = int(qty)
        quoted = lookup(symbol)

        if quoted is None:
            return apology("Stock does not exist")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        username = rows[0]["username"]
        sym = quoted["symbol"]
        price = quoted["price"]
        cash = float(rows[0]["cash"])

        if qty < 1:
            return apology("Enter valid number")
        elif (price * qty) > cash:
            return apology("No sufficient funds")

        db.execute(
            "CREATE TABLE IF NOT EXISTS purchases ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "user_id INTEGER NOT NULL,"
            "symbol TEXT,"
            "purchase_quantity TEXT,"
            "purchase_price REAL,"
            "time TEXT,"
            "FOREIGN KEY (user_id) REFERENCES users (id)"
            ")"
        )
        current_datetime = datetime.today()

        db.execute(
            "INSERT INTO purchases (symbol , purchase_quantity, purchase_price , user_id , time) VALUES (? ,?, ?, ?, ?)",
            sym,
            qty,
            price,
            session["user_id"],
            current_datetime,
        )
        cash = cash - (price * qty)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        return index(sym, usd(price), qty)

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT symbol, purchase_quantity, purchase_price, time FROM purchases WHERE user_id = ?",
        session["user_id"],
    )
    for i in rows:
        i["purchase_quantity"] = int(i["purchase_quantity"])

        if i["purchase_quantity"] < 0:
            i["type"] = "sold"
            i["purchase_quantity"] = -i["purchase_quantity"]
        else:
            i["type"] = "bought"

        i["purchase_price"] = usd(i["purchase_price"])

    rows.reverse()
    return render_template("history.html", transactions=rows)


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
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quoted = lookup(symbol)
        if quoted is None:
            return apology("Stock does not exist")
        else:
            sym = quoted["symbol"]
            price = usd(quoted["price"])
            current_datetime = datetime.today()
            return render_template(
                "quote.html", sym=sym, price=price, date=current_datetime
            )
    else:
        return render_template("quote.html")


def contains_symbol(s):
    for character in s:
        if not character.isalnum():
            return True
    return False


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        rows_u = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if not request.form.get("username"):
            return apology("Please enter username", 400)
        elif len(rows_u) != 0:
            return apology("Username is already taken", 400)
        elif not request.form.get("password"):
            return apology("Please select a password", 400)
        elif not request.form.get("confirmation"):
            return apology("Please re-type the password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        username = request.form.get("username")
        password = request.form.get("password")

        if contains_symbol(password) == False:
            return apology("Password must contain a symbol (@, !, * ...)")

        hashp = generate_password_hash(password, method="pbkdf2", salt_length=16)
        db.execute("INSERT INTO users( username, hash) VALUES(? , ?)", username, hashp)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ? AND hash = ?", username, hashp
        )
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Select stock")
        qty = request.form.get("shares")
        if qty == "":
            return apology("Bruh...")
        if not qty.isdigit():
            return apology("Enter a valid number")
        qty = int(qty)
        current_datetime = datetime.today()
        quoted = lookup(symbol)
        sym = quoted["symbol"]
        price = quoted["price"]
        rows = db.execute(
            "SELECT symbol, SUM(purchase_quantity) AS quant FROM purchases WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            session["user_id"],
            sym,
        )
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        if quoted is None:
            return apology("Stock does not exist")
        elif len(rows) != 1:
            return apology("Not Allowed...")
        elif qty < 1:
            return apology("Enter valid number")
        elif qty > (rows[0]["quant"]):
            return apology("Not enough stocks")
        cash_to_add = price * qty
        new_cash = cash_to_add + cash
        qty = -qty
        db.execute(
            "INSERT INTO purchases (symbol , purchase_quantity, purchase_price , user_id , time) VALUES (? ,?, ?, ?, ?)",
            sym,
            qty,
            price,
            session["user_id"],
            current_datetime,
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"]
        )
        return index(qq=-qty, ss=sym, pp=usd(price))
        return render_template("sell.html", qty=(-qty), symbol=sym, price=usd(price))

    else:
        stocks_dict = db.execute(
            "SELECT symbol FROM purchases WHERE user_id = ? GROUP BY symbol",
            session["user_id"],
        )
        stocks = []
        for i in stocks_dict:
            stocks.append(i["symbol"])

        return render_template("sell.html", stocks=stocks)


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    """Finance chatbot powered by Gemini"""
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not configured. Set GEMINI_API_KEY environment variable."}), 500
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        
        # Create finance-focused prompt
        system_prompt = """You are a helpful financial advisor assistant. Answer questions related to:
- Stock market and investing
- Personal finance
- Trading strategies
- Financial literacy

Keep responses concise (2-3 sentences max). If the question is not finance-related, politely redirect to finance topics."""
        
        full_prompt = f"{system_prompt}\n\nUser Question: {user_message}"
        
        # Get response from Gemini
        response = model.generate_content(full_prompt)
        bot_response = response.text
        
        return jsonify({"response": bot_response}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
