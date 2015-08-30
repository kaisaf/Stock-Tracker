# Stock-Tracker

This is a Stock Tracker application that allows users to create an account, sign in and
track short term stock price changes based on percentage or dollar change. Once signed in,
the user is directed to their home page that displays all the trackers she/he set. If any of the
percentage/dollar change thresholds are met, that particular tracker is highlighted with red
background. User can set new trackers on top of the view by typing in the symbol/ticker of
the stock, selecting percentage or dollar from the dropdown menu and finally typing in the
desired change without percentage/dollar signs.

# How to use Step-by-Step:

* Inside Stock-Tracker create virtual environment:
  - $virtualenv -p python3 env
  - $source env/bin/activate
  - $pip3 install -r requirements.txt
    - Installs django 1.8.4, requests 2.7.0 and matplotlib 1.4.3
  - $cd tracker_project
* Create sqlite3 database:
  - $python3 manage.py makemigrations
  - $python3 manage.py migrate
  - $python3 manage.py runserver
  - Go to your browser and start playing around!


### Developers:
* Kaisa Filppula
* Victor Menezes
