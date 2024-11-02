import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

# Flask app initialization
app = Flask(__name__)

# Configure paths for uploaded and enhanced images
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Load the pre-trained ESRGAN model
model_path = 'models/RRDB_ESRGAN_x4.pth'
device = torch.device('cpu')  # Use CPU if no GPU available

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
model.eval()
model = model.to(device)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and enhancement
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Save the uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the image with ESRGAN
        enhanced_filename = "enhanced_" + filename
        enhanced_filepath = os.path.join(app.config['RESULT_FOLDER'], enhanced_filename)
        enhance_image(filepath, enhanced_filepath)
        
        # Return JSON response with filenames for displaying images
        return jsonify({
            'original_filename': filename,
            'enhanced_filename': enhanced_filename
        })

# Function to enhance image using the model
def enhance_image(img_path, enhanced_path):
    # Load and preprocess the image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    
    # Post-process and save the enhanced image
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round().astype(np.uint8)
    cv2.imwrite(enhanced_path, output)

# Route to serve enhanced images for download
@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
