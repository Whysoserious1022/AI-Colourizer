"""
Flask Web Application for Image Colorization
"""
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

from colorizer import ImageColorizer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = Path(__file__).parent / 'uploads'
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'}

# Initialize colorizer
try:
    colorizer = ImageColorizer()
    print("✓ Colorizer initialized successfully!")
except Exception as e:
    print(f"✗ Error initializing colorizer: {e}")
    print("Please run 'python download_models.py' to download the required models.")
    colorizer = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_array):
    """Convert numpy array to base64 string"""
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/colorize', methods=['POST'])
def colorize_image():
    """Handle image colorization request"""
    if colorizer is None:
        return jsonify({
            'error': 'Colorizer not initialized. Please download the models first.'
        }), 500
    
    # Check if file was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    # Check if file is valid
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, BMP, TIFF, WEBP'}), 400
    
    try:
        # Read image file
        file_bytes = np.frombuffer(file.read(), np.uint8)
        original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if original_image is None:
            return jsonify({'error': 'Could not decode image'}), 400
        
        # Colorize the image
        colorized_image = colorizer.colorize_from_array(original_image)
        
        # Convert images to base64 for JSON response
        original_b64 = image_to_base64(original_image)
        colorized_b64 = image_to_base64(colorized_image)
        
        return jsonify({
            'success': True,
            'original': original_b64,
            'colorized': colorized_b64
        })
    
    except Exception as e:
        print(f"Error during colorization: {e}")
        return jsonify({'error': f'Colorization failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'colorizer_ready': colorizer is not None
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎨 Image Colorization Web Application")
    print("=" * 60)
    
    if colorizer is None:
        print("\n⚠ WARNING: Models not loaded!")
        print("Please run: python download_models.py")
        print("=" * 60 + "\n")
    else:
        print("\n✓ Ready to colorize images!")
        print("=" * 60 + "\n")
    
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
