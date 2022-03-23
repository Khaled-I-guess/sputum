from distutils.log import debug
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request 
import os
from numpy import imag
from werkzeug.utils import secure_filename

name = ''
app = Flask(__name__)
 
UPLOAD_FOLDER = 'uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])

def upload_image():
  
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        #cv2.imshow('yeeeeeeeeees',file.filename)
        filename = secure_filename(file.filename)
        #return cv2.imshow('original image',img) 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        import cv2

        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        hsv_img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        height , width, _ = img.shape 
        cx= int(width/2)
        cy= int(height/2)
        pixelcenter= hsv_img[cy, cx]
        hue_value= pixelcenter[0]
        sat_Value= pixelcenter[1]
        val_value= pixelcenter[2]
        color="undefiend"
        if hue_value >0:
            if hue_value <7:
                color = "RED"
            elif hue_value < 18:
                color = "Brown"
            elif hue_value < 37:
                color = "YELLOW"
            elif hue_value < 78:
                color = "GREEN"
            elif hue_value <199:
                color = "RED"
        if hue_value <10 and sat_Value < 10 and val_value <86 :
            color = "BLACK"
        elif hue_value < 10 and sat_Value < 10 and val_value >200:
            color = "WHITE"
        print(pixelcenter)
        print(color)
        cv2.circle(img,(cx,cy), 5 , (255,0,0),3)
        cv2.imshow('original image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        flash(color)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/')
def display_image(filename):
    #print('display_image filename: ' + filename)    
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')