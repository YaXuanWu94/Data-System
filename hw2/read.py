from flask import Blueprint, render_template
import mysql.connector
from dotenv import load_dotenv
import os

read_bp = Blueprint('read_bp', __name__)

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database')
}

@read_bp.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM class")
    classes = cursor.fetchall()

    cursor.execute("SELECT * FROM subject")
    subjects = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('index.html', students=students, classes=classes, subjects=subjects)