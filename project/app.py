
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from blackjacklogic import Deck, Hand, deal_initial_cards
import random

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

RESULTVALUE = ""

#database
db = SQL("sqlite:///project.db")

#imported function from finance
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def redirect_post(url, params={}):
    return render_template('post_redirect.html', url=url, params=params)

@app.route("/add-money", methods=["GET", "POST"])
def money():
    if request.method == "POST":
        if not request.form.get("Cash-Added"):
            flash("Cant add zero cash")
            return redirect("/add-money")
        if int(request.form.get("Cash-Added")) <= 0:
            flash("Cant add negative or zero cash")
            return redirect("/add-money")
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"]
        cash += int(request.form.get("Cash-Added"))
        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, session["user_id"])
        db.execute("INSERT INTO history (id,activity,cash,date_time,total_cash) VALUES (?,'addCash',?,datetime('now'),?)",session["user_id"],int(request.form.get("Cash-Added")),cash)
        return redirect("/add-money")
    else:
        return render_template("moneyadd.html", cash=db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"])

@app.route('/')
@login_required
def index():
    return render_template('home.html', user=db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"])

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username is submitted
        if not request.form.get("username"):
            flash("Must Provide Username")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Provide Password")
            return redirect("/register")

        # Ensure password is confirmed
        elif not request.form.get("confirmation"):
            flash("Must Confirm Password")
            return redirect("/register")

        # Ensure password is confirmed correctly
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password and Confirm Password Must Match")
            return redirect("/register")

        username = request.form.get("username")
        hash = request.form.get("password")

        hashed = generate_password_hash(hash)

        try:
            db.execute("INSERT INTO users (username, hash, cash) VALUES (?,?,10000);", username, hashed)
        except ValueError:
            flash("Username already exists")
            return redirect("/register")
        flash("You are Logged In!")
        return redirect("/")

    elif request.method == "GET":
        return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return redirect("/login")

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


# Buy-in route
@app.route('/buyin', methods=["GET", "POST"])
@login_required
def buyin():
    if request.method == "POST":
        buyin_amount = int(request.form.get("buyin_amount"))
        if buyin_amount <= 0:
            flash("Buy-in amount must be greater than zero.")
            return redirect("/buyin")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if buyin_amount > cash:
            flash("You do not have enough cash for this buy-in amount.")
            return redirect("/buyin")

        session["buyin_amount"] = buyin_amount
        session["cash"] = cash - buyin_amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?", session["cash"], session["user_id"])

        return redirect_post("/play")
    else:
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        return render_template("buyin.html", cash=cash)

# Start game route
@app.route('/play', methods=["GET", "POST"])
@login_required
def start():
    if "buyin_amount" not in session:
        return redirect("/buyin")

    if request.method == "POST":
        deck = Deck()
        player_hand, dealer_hand = deal_initial_cards(deck)
        session['deck'] = deck.deck
        session['player_hand'] = player_hand.cards
        session['player_value'] = player_hand.value
        session['dealer_hand'] = dealer_hand.cards
        session['dealer_value'] = dealer_hand.value
        return redirect_post("/game")
    else:
        return redirect("/")

# Game route
@app.route('/game', methods=["GET", "POST"])
@login_required
def game():
    if request.method == "POST":
        player_hand = session['player_hand']
        dealer_hand = session['dealer_hand']
        player_value = session['player_value']
        dealer_value = session['dealer_value']
        return render_template('game.html', player_hand=player_hand, dealer_hand=dealer_hand, player_value=player_value, dealer_value=dealer_value)
    else:
        return redirect("/")

# Hit route
@app.route('/hit', methods=["POST"])
@login_required
def hit():
    deck = Deck()
    deck.deck = session['deck']
    player_hand = Hand()
    player_hand.cards = session['player_hand']
    player_hand.value = session['player_value']
    player_hand.add_card(deck.deal())
    session['deck'] = deck.deck
    session['player_hand'] = player_hand.cards
    session['player_value'] = player_hand.value
    if player_hand.value > 21:
        return redirect_post("/bust")
    if player_hand.value == 21:
        return redirect_post("/game")
    return redirect_post("/game")

# Stand route
@app.route('/stand', methods=["POST"])
@login_required
def stand():
    deck = Deck()
    deck.deck = session['deck']
    dealer_hand = Hand()
    dealer_hand.cards = session['dealer_hand']
    dealer_hand.value = session['dealer_value']
    if dealer_hand.value == 21:
        return redirect_post("/game_result")
    while dealer_hand.value < 17:
        dealer_hand.add_card(deck.deal())
    randomballs = random.randint(1,4)
    if randomballs == 2:
        dealer_hand.add_card(deck.deal())
    session['dealer_hand'] = dealer_hand.cards
    session['dealer_value'] = dealer_hand.value
    if dealer_hand.value > 21:
        return redirect_post("/game_result")
    return redirect_post("/game_result")

# Bust route
@app.route('/bust', methods=["GET", "POST"])
@login_required
def bust():
    return redirect_post("/game_result")

# Game result route
@app.route('/game_result', methods=["GET", "POST"])
@login_required
def game_result():
    if request.method == "POST":
        player_value = session['player_value']
        dealer_value = session['dealer_value']
        buyin_amount = session.get('buyin_amount')
        user_id = session["user_id"]
        cash = session["cash"]

        if player_value > dealer_value and player_value <= 21:
            # Player wins, add the bet amount to their cash
            cash += buyin_amount * 2
            RESULTVALUE = "You win!"

        elif dealer_value > 21:

            cash += buyin_amount * 2
            RESULTVALUE = "Dealer Bust!"

        elif player_value < dealer_value:
            # Dealer wins, subtract the bet amount from the player's cash
            db.execute("SELECT cash FROM users WHERE id = ?",user_id)[0]["cash"] -= buyin_amount
            RESULTVALUE = "Dealer wins!"
        elif player_value > 21:
            RESULTVALUE = "BUST!"
            db.execute("SELECT cash FROM users WHERE id = ?",user_id)[0]["cash"] -= buyin_amount


        else:
            # It's a tie, cash remains unchanged
            RESULTVALUE = "TIE"
            cash += buyin_amount

        # Update the user's cash in the database
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

        # Remove the buy-in amount from the session
        session.pop('buyin_amount', None)

        db.execute("INSERT INTO history (id,activity,cash,date_time,total_cash) VALUES (?,?,?,datetime('now'),?);",session["user_id"],RESULTVALUE, buyin_amount,cash)

        # Render the result page with the updated cash and result message
        return render_template("result.html", result=RESULTVALUE, cash=cash)
    return redirect("/")


@app.route("/history")
def history():
    jamal = db.execute("SELECT * FROM history WHERE id = ?", session["user_id"])
    return render_template("history.html", database = jamal)
