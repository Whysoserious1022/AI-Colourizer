// ===================================
// DOM Elements
// ===================================
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const processingIndicator = document.getElementById('processingIndicator');
const resultsSection = document.getElementById('resultsSection');
const originalImage = document.getElementById('originalImage');
const colorizedImage = document.getElementById('colorizedImage');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');

// ===================================
// State Management
// ===================================
let currentColorizedImage = null;

// ===================================
// File Upload Handlers
// ===================================
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('click', (e) => {
    if (e.target !== browseBtn) {
        fileInput.click();
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

// ===================================
// Drag and Drop Handlers
// ===================================
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleImageUpload(file);
    } else {
        showError('Please upload a valid image file');
    }
});

// ===================================
// Image Upload & Processing
// ===================================
async function handleImageUpload(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, BMP, TIFF, or WEBP');
        return;
    }
    
    // Validate file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size too large. Maximum size is 16MB');
        return;
    }
    
    // Show processing indicator
    showProcessing();
    
    // Create FormData
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        // Send to server
        const response = await fetch('/colorize', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Colorization failed');
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Display results
            displayResults(data.original, data.colorized);
            currentColorizedImage = data.colorized;
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to colorize image. Please try again.');
        hideProcessing();
    }
}

// ===================================
// UI State Management
// ===================================
function showProcessing() {
    resultsSection.classList.remove('active');
    processingIndicator.classList.add('active');
}

function hideProcessing() {
    processingIndicator.classList.remove('active');
}

function displayResults(originalSrc, colorizedSrc) {
    // Set image sources
    originalImage.src = originalSrc;
    colorizedImage.src = colorizedSrc;
    
    // Hide processing, show results
    hideProcessing();
    resultsSection.classList.add('active');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    alert(message);
}

// ===================================
// Download Handler
// ===================================
downloadBtn.addEventListener('click', () => {
    if (!currentColorizedImage) {
        showError('No colorized image to download');
        return;
    }
    
    // Create download link
    const link = document.createElement('a');
    link.href = currentColorizedImage;
    link.download = `colorized_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// ===================================
// Reset Handler
// ===================================
resetBtn.addEventListener('click', () => {
    // Reset state
    currentColorizedImage = null;
    fileInput.value = '';
    
    // Hide results
    resultsSection.classList.remove('active');
    
    // Scroll to upload section
    uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// ===================================
// Keyboard Shortcuts
// ===================================
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + O to open file dialog
    if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        fileInput.click();
    }
    
    // Ctrl/Cmd + S to download (if image is colorized)
    if ((e.ctrlKey || e.metaKey) && e.key === 's' && currentColorizedImage) {
        e.preventDefault();
        downloadBtn.click();
    }
    
    // Escape to reset
    if (e.key === 'Escape' && resultsSection.classList.contains('active')) {
        resetBtn.click();
    }
});

// ===================================
// Page Load Animation
// ===================================
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// ===================================
// Console Welcome Message
// ===================================
console.log('%c🎨 AI Image Colorization', 'font-size: 24px; font-weight: bold; color: #667eea;');
console.log('%cPowered by OpenCV Deep Learning', 'font-size: 14px; color: #a0aec0;');
console.log('%c\nKeyboard Shortcuts:', 'font-size: 12px; font-weight: bold; margin-top: 10px;');
console.log('%cCtrl/Cmd + O: Open file\nCtrl/Cmd + S: Download colorized image\nEsc: Reset', 'font-size: 11px; color: #a0aec0;');
