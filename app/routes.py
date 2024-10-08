from flask import Blueprint, render_template
import sqlite3
import os
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")


@bp.route("/")
def main():
  connection = sqlite3.connect(DB_FILE)
  cursor = connection.cursor()
  res = cursor.execute('''
  SELECT id, name, start_datetime,
  end_datetime
  FROM appointments
  ORDER BY start_datetime
  ''')
  results = res.fetchall()

  rows = []

  for row in results:
    list_row = list(row)
    list_row[2] = datetime.strptime(list_row[2], "%Y-%m-%d %H:%M:%S")
    list_row[3] = datetime.strptime(list_row[3], "%Y-%m-%d %H:%M:%S")
    rows.append(list_row)

  return render_template("main.html", rows=rows)
