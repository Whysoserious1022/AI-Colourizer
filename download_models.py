"""
Download pre-trained colorization model files
"""
import os
import requests
from pathlib import Path

# Create models directory
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Model file URLs
MODEL_FILES = {
    "colorization_deploy_v2.prototxt": "https://raw.githubusercontent.com/richzhang/colorization/master/colorization/models/colorization_deploy_v2.prototxt",
    "colorization_release_v2.caffemodel": "https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1",
    "pts_in_hull.npy": "https://github.com/richzhang/colorization/raw/master/colorization/resources/pts_in_hull.npy"
}

def download_file(url, destination):
    """Download a file from URL to destination"""
    print(f"Downloading {destination.name}...")
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"Progress: {progress:.1f}%", end='\r')
        
        print(f"\n✓ Downloaded {destination.name} ({downloaded / 1024 / 1024:.2f} MB)")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {destination.name}: {e}")
        return False

def main():
    """Download all required model files"""
    print("=" * 60)
    print("Image Colorization Model Downloader")
    print("=" * 60)
    
    all_exist = all((MODELS_DIR / filename).exists() for filename in MODEL_FILES.keys())
    
    if all_exist:
        print("\n✓ All model files already exist!")
        print(f"Location: {MODELS_DIR.absolute()}")
        return
    
    print(f"\nDownloading models to: {MODELS_DIR.absolute()}\n")
    
    success_count = 0
    for filename, url in MODEL_FILES.items():
        destination = MODELS_DIR / filename
        
        if destination.exists():
            print(f"✓ {filename} already exists, skipping...")
            success_count += 1
        else:
            if download_file(url, destination):
                success_count += 1
    
    print("\n" + "=" * 60)
    if success_count == len(MODEL_FILES):
        print("✓ All model files downloaded successfully!")
    else:
        print(f"⚠ Downloaded {success_count}/{len(MODEL_FILES)} files")
    print("=" * 60)

if __name__ == "__main__":
    main()
