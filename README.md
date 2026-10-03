# CS50 Finance

A web-based stock trading application built as part of **Harvard University's CS50x** course.

CS50 Finance simulates a stock brokerage platform where users can register, look up real-time stock prices, buy and sell stocks, and track their portfolio and transaction history.

## Features

* **User Registration & Login**

  * Secure account registration and authentication
  * Passwords stored using hashing

* **Stock Lookup**

  * Search for stocks using their ticker symbols
  * Retrieve current stock prices using an external stock API

* **Buy Stocks**

  * Purchase shares using available cash
  * Automatically updates the user's portfolio and cash balance

* **Sell Stocks**

  * Sell shares owned by the user
  * Prevents users from selling more shares than they own

* **Portfolio Tracking**

  * View current holdings
  * Track available cash and total portfolio value
  * View current stock prices and holding values

* **Transaction History**

  * Records all buy and sell transactions
  * Displays transaction type, stock symbol, number of shares, price, and timestamp

## Tech Stack

* **Python**
* **Flask**
* **SQLite**
* **HTML**
* **CSS**
* **Jinja2**
* **JavaScript**
* **Bootstrap**
* **CS50 Library**
* External stock market API

## Project Structure

```text
finance/
│
├── app.py              # Main Flask application
├── finance.db          # SQLite database
├── helpers.py          # Helper functions
├── requirements.txt    # Python dependencies
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── quote.html
│   ├── quoted.html
│   ├── buy.html
│   ├── sell.html
│   ├── history.html
│   └── apology.html
│
└── static/
    └── styles.css      # Custom styling
```

## How It Works

The application is built using Flask and follows a simple request-response architecture.

1. A user interacts with the web interface.
2. Flask processes the incoming request.
3. The application communicates with the SQLite database when user or transaction data is required.
4. Stock information is retrieved through an external API.
5. The appropriate HTML template is rendered using Jinja2.
6. The updated portfolio or transaction information is displayed to the user.

## Database

The application uses SQLite to store application data.

The database maintains information such as:

* Registered users
* Password hashes
* Cash balances
* Stock holdings
* Buy and sell transactions
* Transaction timestamps

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set the required environment variables

Configure the environment variables required by the CS50 Finance application, including the stock API key if required by the implementation.

### 4. Run the Flask application

```bash
flask run
```

The application will be available at the local address provided by Flask.

## Example Workflow

```text
Register
   ↓
Login
   ↓
Search for a stock
   ↓
View current price
   ↓
Buy shares
   ↓
Portfolio updated
   ↓
Sell shares
   ↓
Transaction recorded
```

## Learning Outcomes

This project provided practical experience with:

* Flask web application development
* Backend development using Python
* SQL and relational databases
* User authentication
* REST/API integration
* Server-side rendering with Jinja2
* Form validation
* Session management
* Financial transaction logic
* Frontend development with HTML, CSS and Bootstrap

## Disclaimer

This project is intended for educational purposes only. It does not execute real stock trades or handle real financial transactions.

## Acknowledgements

This project was developed as part of **CS50x: Introduction to Computer Science** by Harvard University.

Built for learning and experimentation.
