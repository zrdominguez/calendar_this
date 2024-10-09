from flask import Blueprint, render_template, redirect, url_for
import sqlite3
import os
from datetime import datetime, timedelta
from .forms import NewAppointment

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

def convert_date(row):
  list_row = list(row)
  list_row[2] = datetime.strptime(list_row[2], "%Y-%m-%d %H:%M:%S")
  list_row[3] = datetime.strptime(list_row[3], "%Y-%m-%d %H:%M:%S")
  return list_row

@bp.route("/<int:year>/<int:month>/<int:day>", methods=["GET", "POST"])
def daily(year, month, day):
    day = datetime(year, month, day)
    next_day = timedelta(days=1) + day
    form = NewAppointment()

    if form.validate_on_submit():
        # Combine start/end date and time into datetime strings for SQLite
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data).strftime("%Y-%m-%d %H:%M:%S"),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data).strftime("%Y-%m-%d %H:%M:%S"),
            'description': form.description.data,
            'private': form.private.data
        }

        # Insert into the database
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO appointments(name, start_datetime, end_datetime, description, private)
                VALUES(:name, :start_datetime, :end_datetime, :description, :private)
            ''', params)
            connection.commit()

        return redirect("/")
    else:
      print(form.errors)

    # Fetch the appointment data
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id, name, start_datetime, end_datetime
            FROM appointments
            WHERE start_datetime BETWEEN :day AND :next_day
            ORDER BY start_datetime
        ''', {'day': day, 'next_day': next_day})
        results = cursor.fetchall()

    # Convert rows to Python-friendly datetime objects
    rows = [convert_date(row) for row in results]

    # Render the page with the form and fetched appointments
    return render_template("main.html", rows=rows, form=form)



@bp.route("/", methods=["GET", "POST"])
def main():
    today = datetime.now()
    return redirect(url_for(".daily", year=today.year, month=today.month, day=today.day))
