# 📈 CS50 Finance

A modern web-based stock trading application with **AI-powered financial chatbot** built as part of **Harvard University's CS50x** course.

CS50 Finance simulates a full-featured stock brokerage platform where users can register, look up real-time stock prices, buy and sell stocks, track their portfolio, and get financial advice from an intelligent AI assistant.

## ✨ Features

### Core Trading Features

- **User Registration & Login** - Secure authentication with password hashing
- **Real-time Stock Lookup** - Search ticker symbols and get current prices via Finnhub API
- **Buy Stocks** - Purchase shares with real-time balance management
- **Sell Stocks** - Liquidate holdings with safeguards against over-selling
- **Portfolio Tracking** - View holdings, cash balance, and total portfolio value
- **Transaction History** - Complete audit trail of all trades with timestamps

### 🤖 AI-Powered Financial Chatbot

- **Intelligent Assistant** - Powered by Google Gemini AI
- **Finance-Focused** - Specialized in stocks, investing, and personal finance
- **Real-time Chat** - Chat bubble interface in bottom-right corner
- **Context-Aware** - Finance-specialized prompts for accurate advice
- **Mobile-Friendly** - Responsive design that works on all devices

## 🛠 Tech Stack

| Category      | Technology                               |
| ------------- | ---------------------------------------- |
| **Backend**   | Python 3.12+, Flask                      |
| **Database**  | SQLite                                   |
| **Frontend**  | HTML5, CSS3, JavaScript, Bootstrap 5.3   |
| **APIs**      | Finnhub (Stock Data), Google Gemini (AI) |
| **Security**  | Werkzeug, Session-based Authentication   |
| **Libraries** | CS50, Flask-Session, Jinja2              |

## 📋 Prerequisites

Before running this project, you'll need:

1. **Python 3.12+**
2. **API Keys** (Free):
   - [Finnhub API Key](https://finnhub.io/) - Real-time stock data
   - [Google Gemini API Key](https://aistudio.google.com/app/apikeys) - AI chatbot

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd finance
```

### 2. Create & Activate Python Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Set Finnhub API Key (for stock data)
export FINNHUB_API_KEY="your_finnhub_api_key_here"

# Set Google Gemini API Key (for AI chatbot)
export GEMINI_API_KEY="your_gemini_api_key_here"
```

**Or create a `.env` file:**

```
FINNHUB_API_KEY=your_finnhub_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` in debug mode.

## 📦 Dependencies

- **cs50** - CS50 library for SQL database operations
- **Flask** - Web framework
- **Flask-Session** - Server-side session management
- **finnhub-python** - Finnhub API client for stock data
- **google-generativeai** - Google Gemini API client for AI chatbot
- **pytz** - Timezone handling
- **requests** - HTTP library
- **Werkzeug** - Security utilities

All dependencies are listed in `requirements.txt`

## 🎯 Getting API Keys

### Finnhub API Key (Free Tier)

1. Visit [finnhub.io](https://finnhub.io/)
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Set as `FINNHUB_API_KEY` environment variable

### Google Gemini API Key (Free Tier)

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click "Create API Key"
3. Copy the generated key
4. Set as `GEMINI_API_KEY` environment variable

## 📂 Project Structure

```
finance/
├── app.py                 # Flask application & route handlers
├── helpers.py            # Utility functions (login_required, lookup, usd)
├── requirements.txt      # Python dependencies
├── finance.db           # SQLite database (created on first run)
├── templates/           # HTML templates
│   ├── layout.html      # Base template with AI chatbot
│   ├── index.html       # Portfolio dashboard
│   ├── buy.html         # Buy stocks form
│   ├── sell.html        # Sell stocks form
│   ├── quote.html       # Stock lookup page
│   ├── history.html     # Transaction history
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── apology.html     # Error page
└── static/
    └── styles.css       # CSS styling
```

## 🔐 How It Works

### User Authentication

- Users register with a username and password
- Passwords are hashed using PBKDF2 with salt
- Sessions are stored server-side for security

### Stock Trading

- Real-time stock prices fetched from Finnhub API
- Buy operation checks sufficient cash balance
- Sell operation prevents over-selling
- All transactions stored in SQLite database

### AI Chatbot

- Accessible to logged-in users only
- Chat bubble appears in bottom-right corner
- Uses Google Gemini model "gemini-pro"
- Custom system prompt focuses on finance topics
- Async request handling via JavaScript
- Real-time message streaming and response

## 📊 Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    cash NUMERIC DEFAULT 10000.00
)
```

### Purchases Table

```sql
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT,
    purchase_quantity TEXT,
    purchase_price REAL,
    time TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

## 🖼 Screenshots

- **Dashboard** - Portfolio overview with holdings and cash balance
- **Quote** - Real-time stock price lookup
- **Buy/Sell** - Transaction forms with balance validation
- **History** - Complete transaction ledger
- **AI Chatbot** - Finance-focused assistant chat bubble

## 🔧 Development

### Running in Debug Mode

The app runs in Flask debug mode by default:

- Automatic reloader on code changes
- Interactive debugger on exceptions
- Debug PIN: Check terminal output

### To Disable Debug Mode

Edit the last line in `app.py`:

```python
if __name__ == "__main__":
    app.run(debug=False)  # Set to False for production
```

## ⚠️ Important Notes

1. **Development Only**: This is a development server. Use a production WSGI server (Gunicorn, uWSGI) for deployment
2. **Database**: SQLite is suitable for development/learning. Use PostgreSQL for production
3. **API Rate Limits**: Be aware of API rate limits on free tiers
4. **Security**: Keep API keys secure. Never commit them to version control

## 📝 License

This project is part of Harvard's CS50 course and follows their academic integrity policies.

## 🙋 Support

For issues or questions about this project:

1. Check the [CS50 Documentation](https://cs50.readthedocs.io/)
2. Review the [Flask Documentation](https://flask.palletsprojects.com/)
3. Consult the [Finnhub API Docs](https://finnhub.io/docs/api)
4. Check [Google Gemini API Docs](https://ai.google.dev/docs)

## 🎓 Learning Outcomes

This project demonstrates:

- Full-stack web development with Python/Flask
- RESTful API integration
- Database design and SQL queries
- Authentication and security best practices
- Real-time API data handling
- AI/ML integration with LLMs
- Responsive UI/UX design
- Frontend-backend communication

---

**Made with ❤️ for CS50 | Enhanced with 🤖 AI Chatbot**

- External stock market API

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

- Registered users
- Password hashes
- Cash balances
- Stock holdings
- Buy and sell transactions
- Transaction timestamps

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

- Flask web application development
- Backend development using Python
- SQL and relational databases
- User authentication
- REST/API integration
- Server-side rendering with Jinja2
- Form validation
- Session management
- Financial transaction logic
- Frontend development with HTML, CSS and Bootstrap

## Disclaimer

This project is intended for educational purposes only. It does not execute real stock trades or handle real financial transactions.

## Acknowledgements

This project was developed as part of **CS50x: Introduction to Computer Science** by Harvard University.

Built for learning and experimentation.
