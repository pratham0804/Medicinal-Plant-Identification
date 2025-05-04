# Medicinal Plant Identification

This project uses machine learning to identify medicinal plants from images. It supports both JPEG/JPG formats (using a TensorFlow model) and other image formats.

## Prerequisites

- Python 3.8 or higher
- Git with LFS support
- Sufficient disk space (approximately 300MB for dependencies)

## Setup Instructions

### 1. Create and Activate Virtual Environment

For GitHub Codespaces:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

For Local Windows System:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 2. Install Git LFS

For GitHub Codespaces:
```bash
# Install Git LFS
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash && sudo apt-get install git-lfs
```

For Local Windows System:
1. Download Git LFS from https://git-lfs.github.com/
2. Install it on your system
3. Run `git lfs install` in your terminal

### 3. Verify Model File Setup

Run these commands to verify the model file is properly tracked:
```bash
# Check if model is tracked by Git LFS
git lfs ls-files | grep model_avg_25.h5
# Expected output: a4cb17df70 - backend/models/model_avg_25.h5

# Check model file status
ls -lh backend/models/model_avg_25.h5
# Expected output: -rw-rw-rw- 1 vscode root 133 Feb 3 23:52 backend/models/model_avg_25.h5
```

### 4. Pull Model and Install Dependencies

```bash
# Pull the model file
git lfs pull

# Install required packages
pip install -r backend/requirements.txt
```

### 5. Run the Application

```bash
# Navigate to backend directory
cd backend

# Start the Flask server
python app.py
```

The server will start on `http://localhost:5000` or `http://0.0.0.0:5000`

## Features

- Supports multiple image formats (JPG, JPEG, PNG, WEBP)
- Uses TensorFlow model for JPG/JPEG files
- Uses Vision API for other image formats
- Provides detailed plant information and uses
- Interactive web interface

## Troubleshooting

1. If you see "git: 'lfs' is not a git command", make sure Git LFS is properly installed
2. If model file is only 133 bytes, run `git lfs pull` to download the actual model
3. For package installation errors, try upgrading pip: `python -m pip install --upgrade pip`

## Note

- For JPG/JPEG files, the system uses a local TensorFlow model
- For other formats, you need to set up the Vision API key in `backend/.env`

## License

[Add your license information here]

## Contributors

[Add contributor information here]

## Recent Updates
- Improved error handling in both frontend and backend
- Fixed plant information retrieval using info_api.py
- Included pre-configured virtual environment for easier setup
- Enhanced model initialization and error logging
- Updated project structure for better organization

## Project Structure
```
├── backend/
│   ├── models/          # Model files
│   ├── app.py          # Main Flask application
│   ├── info_api.py     # Plant information data
│   └── requirements.txt # Backend dependencies
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
├── venv/               # Pre-configured virtual environment
└── requirements.txt    # Global dependencies
```

## Quick Setup
1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd Medicinal-Plant-Identification
   ```

2. Activate the pre-configured virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. Start the application:
   ```bash
   cd backend
   python app.py
   ```

4. Access the application at `http://localhost:5000`

## Features
- Plant identification from images
- Detailed plant information and uses
- Support for multiple image formats (JPG, PNG, WebP)
- AI-powered plant analysis
- Mobile-responsive design

## Environment Variables
Create a `.env` file in the backend directory with:
```
VISION_API_KEY=your_api_key_here
```

## Notes
- The virtual environment is included for easier setup
- Model files are stored in backend/models/
- Supports both TensorFlow and Gemini Vision API for predictions

## Troubleshooting
If you encounter any issues:
1. Ensure you're using the included virtual environment
2. Check if the model file exists in backend/models/
3. Verify the .env file is properly configured
4. Check the server logs for detailed error messages
