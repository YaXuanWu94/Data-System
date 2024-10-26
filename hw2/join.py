from flask import Blueprint, render_template
import mysql.connector
from dotenv import load_dotenv
import os

join_blueprint = Blueprint('join', __name__)

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database')
}

def execute_query(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@join_blueprint.route('/', methods=['GET'])
def show_join():
    query = '''
        SELECT students.student_id, students.name, students.gender, class.class_id, subject.fav_subject
        FROM students
        LEFT JOIN class ON students.student_id = class.student_id
        LEFT JOIN subject ON students.student_id = subject.student_id;
    '''
    results = execute_query(query)
    return render_template('join.html', results=results)