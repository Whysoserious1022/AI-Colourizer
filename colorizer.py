"""
Image Colorization using Deep Learning
Based on "Colorful Image Colorization" by Zhang et al.
"""
import cv2
import numpy as np
from pathlib import Path

class ImageColorizer:
    def __init__(self, models_dir="models"):
        """Initialize the colorizer with pre-trained models"""
        self.models_dir = Path(models_dir)
        
        # Model file paths
        self.prototxt = self.models_dir / "colorization_deploy_v2.prototxt"
        self.caffemodel = self.models_dir / "colorization_release_v2.caffemodel"
        self.pts_in_hull = self.models_dir / "pts_in_hull.npy"
        
        # Verify model files exist
        if not all([self.prototxt.exists(), self.caffemodel.exists(), self.pts_in_hull.exists()]):
            raise FileNotFoundError(
                "Model files not found. Please run 'python download_models.py' first."
            )
        
        # Load the model
        print("Loading colorization model...")
        self.net = cv2.dnn.readNetFromCaffe(
            str(self.prototxt),
            str(self.caffemodel)
        )
        
        # Load cluster centers for LAB color space
        pts = np.load(str(self.pts_in_hull), allow_pickle=True)
        
        # Add cluster centers as 1x1 convolutions to the model
        class8 = self.net.getLayerId("class8_ab")
        conv8 = self.net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        self.net.getLayer(class8).blobs = [pts.astype("float32")]
        self.net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
        
        print("✓ Model loaded successfully!")
    
    def colorize(self, image_path):
        """
        Colorize a grayscale image
        
        Args:
            image_path: Path to the input image (can be grayscale or color)
        
        Returns:
            colorized_image: BGR image (numpy array)
        """
        # Load the image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to RGB for processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Normalize and convert to LAB color space
        scaled = image_rgb.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
        
        # Resize for the network (224x224)
        resized = cv2.resize(lab, (224, 224))
        
        # Extract L channel
        L = cv2.split(resized)[0]
        L -= 50  # Mean centering
        
        # Predict AB channels
        self.net.setInput(cv2.dnn.blobFromImage(L))
        ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
        
        # Resize predicted AB channels to match original image size
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
        
        # Extract L channel from original image
        L = cv2.split(lab)[0]
        
        # Concatenate L channel with predicted AB channels
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        
        # Convert back to RGB
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
        colorized = np.clip(colorized, 0, 1)
        
        # Convert to BGR for OpenCV
        colorized = (255 * colorized).astype("uint8")
        colorized_bgr = cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR)
        
        return colorized_bgr
    
    def colorize_from_array(self, image_array):
        """
        Colorize an image from numpy array
        
        Args:
            image_array: BGR image as numpy array
        
        Returns:
            colorized_image: BGR image (numpy array)
        """
        # Convert to RGB for processing
        image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        # Normalize and convert to LAB color space
        scaled = image_rgb.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
        
        # Resize for the network (224x224)
        resized = cv2.resize(lab, (224, 224))
        
        # Extract L channel
        L = cv2.split(resized)[0]
        L -= 50  # Mean centering
        
        # Predict AB channels
        self.net.setInput(cv2.dnn.blobFromImage(L))
        ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
        
        # Resize predicted AB channels to match original image size
        ab = cv2.resize(ab, (image_array.shape[1], image_array.shape[0]))
        
        # Extract L channel from original image
        L = cv2.split(lab)[0]
        
        # Concatenate L channel with predicted AB channels
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        
        # Convert back to RGB
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
        colorized = np.clip(colorized, 0, 1)
        
        # Convert to BGR for OpenCV
        colorized = (255 * colorized).astype("uint8")
        colorized_bgr = cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR)
        
        return colorized_bgr

# Test the colorizer
if __name__ == "__main__":
    colorizer = ImageColorizer()
    print("Colorizer initialized successfully!")
