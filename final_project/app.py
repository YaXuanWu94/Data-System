import os
import gridfs
import base64
from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client['tourist_spots']
collection = db['tourist_spots_records']
fs = gridfs.GridFS(db)

@app.route('/')
def index():
    records = list(collection.find())
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    date = request.form.get('date')
    location = request.form.get('location')
    notes = request.form.get('notes')
    files = request.files.getlist('photos')

    photo_ids = []
    for file in files:
        if file:
            file_id = fs.put(file, filename=file.filename, content_type=file.content_type)
            photo_ids.append(file_id)

    record = {
        "name": name,
        "date": datetime.strptime(date, '%Y-%m-%d'),
        "location": location,
        "notes": notes,
        "photos": photo_ids
    }

    collection.insert_one(record)
    return jsonify({"message": "Record added successfully!"})

@app.template_filter('b64encode')
def b64encode_filter(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    return ''

app.jinja_env.filters['b64encode'] = b64encode_filter

@app.route('/view/<record_id>')
def view(record_id):
    record = collection.find_one({"_id": ObjectId(record_id)})
    if record:
        photos = [fs.get(photo_id).read() for photo_id in record.get('photos', [])]
        return render_template('view.html', record=record, photos=photos)
    return "Record not found", 404

@app.route('/edit/<record_id>', methods=['GET', 'POST'])
def edit(record_id):
    record = collection.find_one({"_id": ObjectId(record_id)})
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        notes = request.form.get('notes')

        updated_record = {
            "name": name,
            "date": datetime.strptime(date, '%Y-%m-%d'),
            "location": location,
            "notes": notes
        }

        collection.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
        return redirect(url_for('index'))
    return render_template('edit.html', record=record)

@app.route('/delete/<record_id>', methods=['POST'])
def delete(record_id):
    record = collection.find_one({"_id": ObjectId(record_id)})
    if record:
        for photo_id in record.get('photos', []):
            fs.delete(photo_id)
        collection.delete_one({"_id": ObjectId(record_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)