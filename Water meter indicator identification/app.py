from flask import Flask, request, render_template
import pickle
import os
from werkzeug.utils import secure_filename
from run_yolo import run
from read_number import run_read_number

# Initialize the flask class and specify the templates directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'image')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
print(os.getcwd())

# Default route set as 'home'
@app.route('/')

def home():
    # Render home.html

    return render_template('home.html') 
@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      latestfile = request.files['file']
      latestfile.filename = "upload.jpg"
      full_filename = os.path.join(app.config['UPLOAD_FOLDER'], latestfile.filename)
      latestfile.save(full_filename)
      run("static/image/"+latestfile.filename) 
      data = run_read_number()
      return render_template("home.html", user_image ="static/image/"+latestfile.filename  ,predict_plate ="static/predict/object-detection.jpg"
        ,value1=data['string_digit'],value2=data['Execution_time'])
      



if __name__=='__main__':
    app.run(debug=True)