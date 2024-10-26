from flask import Blueprint, request, redirect, url_for, render_template
import mysql.connector
from dotenv import load_dotenv
import os

create_bp = Blueprint('create_bp', __name__)

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database')
}

@create_bp.route('/add_full_record', methods=['POST'])
def add_full_record():
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    class_id = request.form.get('class_id')
    fav_subject = request.form.get('fav_subject')
    
    if student_id and name and gender and class_id and fav_subject:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        try:
            # Insert into the `students` table
            insert_student = "INSERT INTO students (student_id, name, gender) VALUES (%s, %s, %s)"
            cursor.execute(insert_student, (student_id, name, gender))
            
            # Insert into the `class` table using the same `student_id`
            insert_class = "INSERT INTO class (class_id, student_id) VALUES (%s, %s)"
            cursor.execute(insert_class, (class_id, student_id))
            
            # Insert into the `subject` table using the same `student_id`
            insert_subject = "INSERT INTO subject (fav_subject, student_id) VALUES (%s, %s)"
            cursor.execute(insert_subject, (fav_subject, student_id))
            
            # Commit the transaction
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()  # Rollback in case of an error
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('read_bp.index'))