from flask import Flask, render_template
import calendar
from datetime import datetime
from extentions import db

# Create a Flask app and configure sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# attach db to app
db.init_app(app)

#imports models after db is initialized to avoid circular imports
from models import *

with app.app_context():
    db.create_all()

@app.route("/")
def calendar_view():
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)

    sessions = RevisionSession.query.filter(
    db.extract('month', RevisionSession.date) == now.month,
    db.extract('year', RevisionSession.date) == now.year).all()

    return render_template("calendar.html", calendar=cal, month=now.month, year=now.year, sessions=sessions)

# Run the app if this file is executed
if __name__ == "__main__":
    app.run(debug=True)