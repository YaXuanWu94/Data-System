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

            # Redirect to the main submissions page after submission
            return redirect(url_for('submissions'))

    # Render the form for GET request
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
        # 從 GridFS 中取得檔案
        file = fs.get(ObjectId(file_id))
        response = app.response_class(file, content_type=file.content_type)
        response.headers['Content-Disposition'] = f'attachment; filename={file.filename}'
        return response
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
