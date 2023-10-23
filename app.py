from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os

# Define the connection string to your MongoDB cluster
connection_string = 'mongodb+srv://test:sparta@cluster0.qrxbmme.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

# Define the upload folder paths
app.config['UPLOAD_FOLDER'] = 'static'
app.config['UPLOAD_PROFILE'] = 'static'  # Create a 'profiles' directory for profile images

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'{mytime}.{extension}'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]  
    profilename = f'{mytime}-profile.{extension}' 
    profile.save(os.path.join(app.config['UPLOAD_PROFILE'], profilename))

    doc = {
        'profile': profilename,
        'file': filename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
