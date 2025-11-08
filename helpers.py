import os
import requests
from flask import redirect, render_template, session
from functools import wraps
import finnhub


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login."""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    try:
        finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
        quote = finnhub_client.quote(symbol)
        if not quote:
            return None
        return {
            "name": symbol.upper(),
            "price": float(quote["c"]),
            "symbol": symbol.upper()
        }
    except Exception:
        return None

# def lookup(symbol):
    """Look up quote for symbol using Alpha Vantage."""
    api_key = os.environ.get("API_KEY")
    if not api_key:
        return None

    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        print(response.json())
        response.raise_for_status()
        data = response.json()

        if "Global Quote" not in data or "05. price" not in data["Global Quote"]:
            return None

        return {
            "name": symbol.upper(),
            "price": float(data["Global Quote"]["05. price"]),
            "symbol": symbol.upper()
        }
    except Exception:
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
