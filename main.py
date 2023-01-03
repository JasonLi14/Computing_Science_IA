"""
Title: Website Portion
Date-Created: 2023-01-02
"""

# Import flask library
from flask import Flask, render_template, request, redirect
# Import file explorer library
from pathlib import Path
# Import algorithms from other files
import algorithms

# FLASK #
app = Flask(__name__)

# GLOBAL VARIABLES #
DATABASE_NAME = "Fashion.db"
FIRST_RUN = True

if (Path.cwd() / DATABASE_NAME).exists():
    FIRST_RUN = False

# SUBROUTINES


@app.route('/', methods=["GET", "POST"])  # the application immediately routes to the index page
def index():
    ALERT = ""
    return render_template("index.html")


# MAIN PROGRAM CODE #
if __name__ == "__main__":
    # Make the database
    if FIRST_RUN:
        algorithms.setup()

    # Run app
    app.run(debug=True)