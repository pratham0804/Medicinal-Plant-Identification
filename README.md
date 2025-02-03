# Medicinal Plant Identification

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
