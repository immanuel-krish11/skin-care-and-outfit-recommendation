from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf


from outfit_recommendation import generate_luxury_recommendations, COLOR_DB
from tonehexadecimal import get_skin_tone_hex
from hug_outfit import outfit_response
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# Alternative to "from tensorflow.keras.models import load_model"
load_model = tf.keras.models.load_model

# Alternative to "from tensorflow.keras.preprocessing import image"
image = tf.keras.utils.image_dataset_from_directory  # If loading from a directory


app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Models (Update with your actual model paths)
MODELS = {
    #'skin_tone': load_model('models/skin_tone.h5'),
    #'skin_type': load_model('models/skin_type.h5'),
    #'acne': load_model('models/acne.h5')
}

# Class Labels (Update with your actual classes)
CLASS_LABELS = {
    'skin_tone': ['MST-1', 'MST-2', 'MST-3', 'MST-4', 'MST-5', 
                 'MST-6', 'MST-7', 'MST-8', 'MST-9', 'MST-10'],
    'skin_type': ['Dry', 'Normal', 'Oily', 'Combination'],
    'acne': ['None', 'Mild', 'Moderate', 'Severe']
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/explore/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Preprocess image
            processed_img = preprocess_image(filepath)
            
            # Get predictions
            predictions = {
                'skin_tone': MODELS['skin_tone'].predict(processed_img),
                'skin_type': MODELS['skin_type'].predict(processed_img),
                'acne': MODELS['acne'].predict(processed_img)
            }
            
            # Get class labels
            results = {
                'skin_tone': CLASS_LABELS['skin_tone'][np.argmax(predictions['skin_tone'])],
                'skin_type': CLASS_LABELS['skin_type'][np.argmax(predictions['skin_type'])],
                'acne': CLASS_LABELS['acne'][np.argmax(predictions['acne'])],
                'filename': filename
            }
            
            return render_template('analysis.html', results=results)
    
    return render_template('analysis.html', url_for_explore = "/explore")

@app.route('/explore/outfit', methods=['GET', 'POST'])
def outfit():
    
    # Add your outfit recommendation logic here
    '''
    if request.method == 'POST':
        action = request.form.get('action')
        # Check if the post request has the file part
        if 'photo' not in request.files:
            return redirect(request.url)
        
        file = request.files['photo']
        
        # If user does not select file, browser submits empty file
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['custom-images'], filename)
            file.save(filepath)
        '''
    if request.method == 'POST':
        action = request.form.get('action')
        fname = [f for f in os.listdir("custom-images/")]
        img_path = os.path.join("custom-images/", fname[0])
        hex_tone = get_skin_tone_hex(img_path)
        print(hex_tone)
                
    # Step 2: Get outfit recommendations based on the skin tone
        combinations, brightness,undertone = generate_luxury_recommendations(hex_tone)
    # print(combinations)


    # if request.method == 'POST':
    #     hex_color = request.form.get('hex_color', '').strip()
    #     if len(hex_color) == 7 and hex_color.startswith('#'):
    #         combinations, brightness, undertone = generate_luxury_recommendations(hex_color)
    #         print(hex_color)

        response = outfit_response(skin_tone= hex_tone)
        return render_template('outfit.html',
                            hex_color = hex_tone,
                            combinations= combinations,
                                color_db=COLOR_DB,
                                response = response)
    return render_template('outfit.html')


@app.route('/explore/products')
def product():
    # Add your product recommendation logic here
    return render_template('products.html')

@app.route('/explore/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)