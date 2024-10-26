from flask import Blueprint, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

delete_bp = Blueprint('delete_bp', __name__)

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database')
}

@delete_bp.route('/student', methods=['POST'])
def delete_student():
    student_ids = request.form.getlist('student_ids')
    if student_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        delete_query = "DELETE FROM students WHERE student_id IN (%s)" % ','.join(['%s'] * len(student_ids))
        cursor.execute(delete_query, tuple(student_ids))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('read_bp.index'))

@delete_bp.route('/class', methods=['POST'])
def delete_class():
    class_ids = request.form.getlist('class_ids')
    if class_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        delete_query = "DELETE FROM class WHERE id IN (%s)" % ','.join(['%s'] * len(class_ids))
        cursor.execute(delete_query, tuple(class_ids))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('read_bp.index'))

@delete_bp.route('/subject', methods=['POST'])
def delete_subject():
    subject_ids = request.form.getlist('subject_ids')
    if subject_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        delete_query = "DELETE FROM subject WHERE id IN (%s)" % ','.join(['%s'] * len(subject_ids))
        cursor.execute(delete_query, tuple(subject_ids))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('read_bp.index'))