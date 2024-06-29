# **BLACKJ@CK.COM**

This is blackj@ck. My final project for CS50x, CS50's Introduction to Computer Science. As you can probably tell by the title, this is basically a website for blackjack. It contains features such as separate users, history, adding money/funds and the game itself. I took lots of inspiration from the finance problem set and the main code for this website is written using flask.

## VIDEO
https://youtu.be/XSfJeFS25Us

## Languages Used
1. HTML
2. CSS
3. JavaScript
4. Python
5. SQLite

> pip install -r requirements.txt

## App.py
This is where all of the action takes place. Using flask and sql, I managed to create a full stack web application. It handles all of the routes and contains all of the code for the actions that the user can do on the website. Now I will go over all the functions and features in the script.

### Default
This isnt an actual function but I would like to mention that some of the functions in this file are imported from finance, just to get rid of the redundant repetitive work. Stuff that I have imported are Register(), Login() and Logout. Along with the code to setup flask and sql. I also imported Money() and History() Which do the same things as in finance. Money() allows the user to add money to thier account and History displays all the things that the user has done on that account. Lastly I want to mention index() because it plays a pretty important role. Whenever the user redirects to "/", Index() will render the home screen.

### Buyin()
This is hte first part of the blackjack game. You need to buyin or in other words bet money before the game starts. It supports both methods GET and POST. When the method is get, it means that the user just pressed play. Thus it simply renders the buyin page where the user can type in however much they want to bet. However when the method is POST, It means that the user has submitted the amount of money they want to bet. Thus this is where the error checking commences. Firstly would be to check if the user inputed a number that is greater than the cash they have, in which case the error will flash and they will be redirected back to /buyin. Same with if the user passes in 0 or a negative integer. Then I used session as a global variable and stored the values of the buy in and the cash remaining.

### Start()
Firstly when the function is called, it needs to check if the buyin value exists in session. If it doesnt, then it will redirect to /buyin. Next up it sets up the game. It deals cards for the player and the dealer, utilising deal_initial_cards from blackjacklogic.py. It also calculates the value for each person's hand along with storing what card was delt to the players in the session. With session["player_hand"], session["dealer_hand"],session["player_value"] and session["dealer_value"] respectively. After setting up, it redirects with the POST method to /game

### Game()
This is the main page for the game, where all of the user action takes place. Firstly it checks for how the user accessed the page. If it was through GET, then they used the url to break in. In that case we will simply redirect them back to the main page. However if they used POST, which is only possible if the entered the buyin and the setup part of the game, the main page will be displayed to them. It just takes the user cards and values along with the dealer card and values. It also has two buttons for the user, Hit and Stand. Just like the heart of a blackjack game. If you made it this far, I will assume you already know how to play blackjack and I will not waste time explaining how to play the game.

### Hit()
Once again, I check to make sure that the only way the user accessed this page is through the POST route. Because if it was through GET, the whole game could break. For hit, it is as simple as just adding a card to the player's deck. Then the value of the player's deck is calculated. If it is above 21, then it is a bust and is redirected to /game-result. Same with if it is equal to 21, where it will also be redirected to /game-result. However if none of these conditions are met, the game keeps going and the user is redirected back to the main game page.

### Stand()
When you stand, you no longer make any moves, so when you press stand, I code the dealer's hand. Firstly, it checks for the value of the dealer's hand. If it is 21, redirect to game result. If it isnt, then it passes a loop. The loop has the dealer constantly deal cards while the value is less than 17. I also added an element of unpredictibility. So if it is greater than 17, the dealer has a 1 in 4 chance of hitting again. If the dealer busts, it is once again sent to /game-result.

### Game_Result
This is the final part of the game. This is where all the calculations are done. By being sent to /game-result, it means that the player is done playing and all the hands are final. So it simply looks at the values of each of the hand and compares them. If the player has 21, they win etc. After comparing everything, the cash is added back to the cash value in the database along with the bet amount, depending if they won or lost.

## Other Files In Project

these are the files used in this project that are not app.py

### Blackjacklogic.py
This is where I wrote and definiend things that would be helpful for when I was writing up the code for blackjack. It consists of two objects and a function. The two objects are Deck() and Hand(). Both of theses store the values that are required duing a blackjack game. Both players, the dealer and the user will have a hand. All of that data is stored within the Hand class. The main feature in the hand class is the add_card method. This adds a card to the player's hand and adjusts the value accordingly. Especially when working with the Ace as it is worth either 11 or 1. The other class is the Deck class. Its constructer creates a deck (52) of cards. Then it will shuffle the cards. The method to deal a card from the deck simply returns pop(), on the shuffed list. Returning a random card and then adding it to the hand. Lastly is the deal initial cards function which deals two cards to the dealer and the player, setting up the game

### Project.db
This database stores all of the backend data. Using sql, I can add or remove data sent from the client side to the server side. It currently has two tables. Users and History. The users table contains the user id, username, password(hashed) and current cash. Pretty much a direct copy off of finance. It also has a history table which contains all of the activities that hte user does. Counting Win/Loss, money gained or lost and adding money. History contains id, activity, cash, date_time and total_cash. The id in this table is the same id of a user in users. So that way when a user accesses the history feature in the website, they will only see the data that correlates to thier userid.

### Templates
Templates is a folder which contains the html for different parts of the website. However all of the templates are extentions of layout.html. Layout is the main html which shows the header bar with the links to different parts of the website. The body is edited differently according to each page of the website, however the header remains the same. The most important file here would be post_redirect.html. It allows me to recreate a funciton in app.py that will allow me to redirect with the post method to another page of the website. For the html, it was pretty trivial. However for the CSS it was way too difficult for me and way to time consuming. So I utilised chatgpt to make it look pretty for me and write the css for each file.

### Static
Static just contains pictures that I will use throughout the website along with styles.css which was used to decorate and manipulate the main file layout.html.

### Requirements.txt
These are libraries requried to run this program. Use pip install -r requirements.txt



