import os
from flask import Flask, render_template, request, redirect, url_for
from unicodedata import normalize
from upload import upload
from youtube import youtube_download
from transcriber import transcribe

# GLOBALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google_cloud.json"
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav'}
HOST = '0.0.0.0'
PORT = 5000
LOCALES = {"ru": "ru-RU", "kz": "kk-KZ"}

# CONFIG
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# FUNCTIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       locale = request.form.get("locale")
       file = request.files['file']
       if file and allowed_file(file.filename):
           filename = normalize('NFKC',file.filename)
           file_location = f"uploaded.{filename.split('.')[-1]}"
           print(file_location)
           file.save(file_location)
           filename = upload(file_location)
           text, confidence = transcribe(filename, LOCALES[locale])
       elif request.form["youtube"]:
           filename = youtube_download(request.form["youtube"])
           print(filename)
           text, confidence = transcribe(filename, LOCALES[locale])
       else:
           text="Ошибка. Вставьте либо файл, либо ссылку с YouTube"
           confidence = ""
    else:
          text="Запустите приложение для получения транскрипции"
          confidence = ""
    return render_template("index.html", data=text);

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
