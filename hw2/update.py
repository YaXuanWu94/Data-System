from flask import Blueprint, request, redirect, url_for, render_template
import mysql.connector
from dotenv import load_dotenv
import os

update_bp = Blueprint('update_bp', __name__)

load_dotenv()

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('database')
}


@update_bp.route('/student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    new_student_id = request.form.get(f'student_id_{student_id}')
    name = request.form.get(f'name_{student_id}')
    gender = request.form.get(f'gender_{student_id}')
    
    if new_student_id and name and gender:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Temporarily disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # Update student_id, name, and gender in the students table
            update_student_query = """
                UPDATE students 
                SET student_id = %s, name = %s, gender = %s 
                WHERE student_id = %s
            """
            cursor.execute(update_student_query, (new_student_id, name, gender, student_id))

            # Update references to student_id in the class table
            update_class_query = """
                UPDATE class
                SET student_id = %s
                WHERE student_id = %s
            """
            cursor.execute(update_class_query, (new_student_id, student_id))

            # Update references to student_id in the subject table
            update_subject_query = """
                UPDATE subject
                SET student_id = %s
                WHERE student_id = %s
            """
            cursor.execute(update_subject_query, (new_student_id, student_id))

            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
            conn.commit()
            # flash("Student and related records updated successfully.")
        
        except mysql.connector.Error as e:
            conn.rollback()
            # flash(f"Error: {str(e)}")
        
        finally:
            cursor.close()
            conn.close()
    
    return redirect(url_for('read_bp.index'))

@update_bp.route('/class/<int:class_id>', methods=['POST'])
def update_class(class_id):
    class_id_value = request.form.get(f'class_id_{class_id}')
    student_id = request.form.get(f'student_id_{class_id}')
    
    if class_id_value and student_id:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if student_id exists in students table
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        
        if result[0] == 0:
            # If student_id does not exist, return an error message
            # flash(f"Error: student_id {student_id} does not exist in the students table.")
            return redirect(url_for('read_bp.index'))
        
        # If student_id exists, proceed with the update
        update_query = "UPDATE class SET class_id = %s, student_id = %s WHERE id = %s"
        cursor.execute(update_query, (class_id_value, student_id, class_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    return redirect(url_for('read_bp.index'))

@update_bp.route('/subject/<int:subject_id>', methods=['POST'])
def update_subject(subject_id):
    fav_subject = request.form.get(f'fav_subject_{subject_id}')
    student_id = request.form.get(f'student_id_{subject_id}')
    
    if fav_subject and student_id:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if student_id exists in students table
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()
        
        if result[0] == 0:
            # If student_id does not exist, return an error message
            # flash(f"Error: student_id {student_id} does not exist in the students table.")
            return redirect(url_for('read_bp.index'))
        
        # If student_id exists, proceed with the update
        update_query = "UPDATE subject SET fav_subject = %s, student_id = %s WHERE id = %s"
        cursor.execute(update_query, (fav_subject, student_id, subject_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    return redirect(url_for('read_bp.index'))
