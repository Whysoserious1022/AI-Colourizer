# 🎨 AI Image Colorization

Transform black and white images into vibrant color using deep learning and OpenCV.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-red.svg)

## ✨ Features

- 🤖 **AI-Powered Colorization** - Uses state-of-the-art deep learning models
- 🎨 **High Quality Results** - Based on "Colorful Image Colorization" by Zhang et al.
- ⚡ **Fast Processing** - Optimized neural network inference
- 🌐 **Modern Web Interface** - Beautiful, responsive UI with glassmorphism design
- 🔒 **Privacy First** - All processing happens locally on your machine
- 📥 **Easy Download** - Save colorized images with one click

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd colourizationProject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download pre-trained models** (~125MB)
   ```bash
   python download_models.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to: `http://localhost:5000`

## 🔄 Workflow & Processing Pipeline

### Complete Processing Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER UPLOADS IMAGE                                   │
│    - Drag & drop or file browser                        │
│    - Client-side validation (type, size)                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. JAVASCRIPT PROCESSING (script.js)                    │
│    - Create FormData object                             │
│    - Show processing indicator                          │
│    - Send POST request to /colorize                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. FLASK SERVER RECEIVES REQUEST (app.py)               │
│    - Validate file extension                            │
│    - Check file size (max 16MB)                         │
│    - Decode image bytes to numpy array                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. COLORIZATION PROCESS (colorizer.py)                  │
│    Step 4.1: Convert BGR → RGB → LAB                   │
│    Step 4.2: Extract L channel (lightness)             │
│    Step 4.3: Resize to 224×224                         │
│    Step 4.4: Mean centering (L -= 50)                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. NEURAL NETWORK INFERENCE (OpenCV DNN)                │
│    - Input: L channel (224×224)                         │
│    - Process through CNN layers                         │
│    - Output: Predicted AB channels                      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 6. POST-PROCESSING (colorizer.py)                       │
│    Step 6.1: Resize AB to original image size          │
│    Step 6.2: Concatenate L + AB channels               │
│    Step 6.3: Convert LAB → RGB → BGR                   │
│    Step 6.4: Clip values & convert to uint8            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 7. SERVER RESPONSE (app.py)                             │
│    - Convert both images to base64                      │
│    - Return JSON with original & colorized              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 8. DISPLAY RESULTS (script.js)                          │
│    - Hide processing indicator                          │
│    - Show results section with animation                │
│    - Display side-by-side comparison                    │
│    - Enable download button                             │
└─────────────────────────────────────────────────────────┘
```

## 📖 Usage

1. **Upload an Image**
   - Drag and drop a grayscale image onto the upload area
   - Or click "Browse Files" to select an image
   - Supports: JPG, PNG, BMP, TIFF, WEBP

2. **Wait for Processing**
   - The AI model will automatically colorize your image
   - Processing typically takes 2-5 seconds

3. **View Results**
   - Compare the original and colorized images side-by-side
   - Download the colorized image with the download button

4. **Try Another**
   - Click "Try Another Image" to colorize more photos

## ⌨️ Keyboard Shortcuts

- `Ctrl/Cmd + O` - Open file dialog
- `Ctrl/Cmd + S` - Download colorized image
- `Esc` - Reset and try another image

## 🏗️ Project Structure

```
colourizationProject/
├── app.py                  # Flask web server
├── colorizer.py            # Core colorization logic
├── download_models.py      # Model downloader script
├── requirements.txt        # Python dependencies
├── models/                 # Pre-trained model files
│   ├── colorization_deploy_v2.prototxt
│   ├── colorization_release_v2.caffemodel
│   └── pts_in_hull.npy
├── static/                 # Frontend assets
│   ├── style.css          # Styling
│   └── script.js          # JavaScript
├── templates/             # HTML templates
│   └── index.html         # Main page
└── uploads/               # Temporary upload storage
```

## 🧠 How It Works

This project uses a deep learning approach based on the paper **"Colorful Image Colorization"** by Richard Zhang, Phillip Isola, and Alexei A. Efros.

### Technical Overview

1. **Color Space Conversion**: Images are converted from RGB to LAB color space
2. **L Channel Extraction**: The lightness (L) channel is extracted from the grayscale image
3. **AB Prediction**: A convolutional neural network predicts the A and B color channels
4. **Reconstruction**: The predicted AB channels are combined with the original L channel
5. **Output**: The result is converted back to RGB for display

### Model Details

- **Architecture**: Caffe deep learning framework
- **Training Data**: Over 1 million images from ImageNet
- **Input Size**: 224x224 pixels (automatically resized)
- **Color Space**: LAB (perceptually uniform)

## 🎯 Best Results

For optimal colorization results:

- Use high-quality grayscale images
- Images with clear subjects work best
- Historical photos and portraits produce excellent results
- Landscapes and nature scenes are well-supported

## 🛠️ Troubleshooting

### Models not downloading?

If automatic download fails, manually download the files:

1. [colorization_deploy_v2.prototxt](https://raw.githubusercontent.com/richzhang/colorization/master/colorization/models/colorization_deploy_v2.prototxt)
2. [colorization_release_v2.caffemodel](https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1)
3. [pts_in_hull.npy](https://github.com/richzhang/colorization/raw/master/colorization/resources/pts_in_hull.npy)

Place them in the `models/` directory.

### Port already in use?

Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

## 📚 References

- [Colorful Image Colorization Paper](http://richzhang.github.io/colorization/)
- [Original GitHub Repository](https://github.com/richzhang/colorization)
- [OpenCV DNN Module](https://docs.opencv.org/master/d2/d58/tutorial_table_of_content_dnn.html)

## 📄 License

This project is for educational purposes. The pre-trained models are from the original research by Zhang et al.

## 🙏 Acknowledgments

- Richard Zhang, Phillip Isola, and Alexei A. Efros for their groundbreaking research
- OpenCV team for the excellent DNN module
- Flask team for the web framework

---

**Made by DAYANANDA S G**
