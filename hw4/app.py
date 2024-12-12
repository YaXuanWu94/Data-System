from flask import Flask, request, redirect, url_for, render_template, jsonify
from pymongo import MongoClient
import gridfs
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['homework_submissions']
collection = db['submissions']
fs = gridfs.GridFS(db)  # GridFS for file storage

# Helper function to check allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit', methods=['GET', 'POST'])
def submit_homework():
    if request.method == 'POST':
        # Get form data
        school = request.form.get('school')
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        file = request.files['file']

        # Validate file
        if file and allowed_file(file.filename):
            # Save file into GridFS
            filename = secure_filename(file.filename)
            file_id = fs.put(file, filename=filename, content_type=file.content_type)

            # Insert submission details into MongoDB
            submission = {
                'school': school,
                'name': name,
                'student_id': student_id,
                'file_id': str(file_id)  # Store GridFS file ID as string
            }
            collection.insert_one(submission)

            return redirect(url_for('submissions'))

    return render_template('submit.html')

@app.route('/')
def submissions():
    # Fetch all submissions from MongoDB
    records = collection.find()
    return render_template('index.html', records=records)

# Route to download files stored in GridFS
@app.route('/download/<file_id>')
def download_file(file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = app.response_class(file, content_type=file.content_type)
        response.headers['Content-Disposition'] = f'attachment; filename={file.filename}'
        return response
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return jsonify({"error": "File not found"}), 404

# Route to update a submission
@app.route('/update/<submission_id>', methods=['GET', 'POST'])
def update_submission(submission_id):
    submission = collection.find_one({'_id': ObjectId(submission_id)})

    if request.method == 'POST':
        # Get updated form data
        school = request.form.get('school')
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        file = request.files.get('file')

        updated_data = {
            'school': school,
            'name': name,
            'student_id': student_id
        }

        # Handle file update
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = fs.put(file, filename=filename, content_type=file.content_type)
            updated_data['file_id'] = str(file_id)

            # Delete the old file if a new file is uploaded
            if 'file_id' in submission:
                fs.delete(ObjectId(submission['file_id']))

        # Update submission details in MongoDB
        collection.update_one({'_id': ObjectId(submission_id)}, {'$set': updated_data})
        return redirect(url_for('submissions'))

    return render_template('update.html', submission=submission)

# Route to delete a submission
@app.route('/delete/<submission_id>', methods=['POST'])
def delete_submission(submission_id):
    submission = collection.find_one({'_id': ObjectId(submission_id)})

    if submission:
        # Delete file from GridFS
        if 'file_id' in submission:
            fs.delete(ObjectId(submission['file_id']))

        # Delete submission record from MongoDB
        collection.delete_one({'_id': ObjectId(submission_id)})

    return redirect(url_for('submissions'))

if __name__ == '__main__':
    app.run(debug=True)
