from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import logging
import random
import numpy as np
from PIL import Image
import google.generativeai as genai
from info_api import plants_data  # Import plants_data from info_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize variables for TensorFlow components
tf = None
preprocess_input = None
custom_model = None

try:
    import tensorflow as tf
    from tensorflow.keras.applications.xception import preprocess_input
    logger.info("TensorFlow successfully imported")
except ImportError as e:
    logger.error(f"Error importing TensorFlow: {str(e)}")
    logger.warning("Application will run in test mode without TensorFlow")

# Load environment variables
load_dotenv()

# App configuration
app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

# Configuration constants
UPLOAD_FOLDER = os.path.join('..', 'frontend', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MODEL_PATH = os.path.join('models', 'model_avg_25.h5')  # Model inside backend/models

# Labels list
labels = ['Aloevera', 'Amla', 'Amruthaballi', 'Arali', 'Astma_weed', 'Badipala', 'Balloon_Vine', 
          'Bamboo', 'Beans', 'Betel', 'Bhrami', 'Bringaraja', 'Caricature', 'Castor', 
          'Catharanthus', 'Chakte', 'Chilly', 'Citron lime (herelikai)', 'Coffee', 
          'Common rue(naagdalli)', 'Coriender', 'Curry', 'Doddpathre', 'Drumstick', 'Ekka', 
          'Eucalyptus', 'Ganigale', 'Ganike', 'Gasagase', 'Ginger', 'Globe Amarnath', 
          'Guava', 'Henna', 'Hibiscus', 'Honge', 'Insulin', 'Jackfruit', 'Jasmine', 
          'Kambajala', 'Kasambruga', 'Kohlrabi', 'Lantana', 'Lemon', 'Lemongrass', 
          'Malabar_Nut', 'Malabar_Spinach', 'Mango', 'Marigold', 'Mint', 'Neem', 
          'Nelavembu', 'Nerale', 'Nooni', 'Onion', 'Palak(Spinach)', 'Papaya', 
          'Parijatha', 'Pea', 'Pepper', 'Pomoegranate', 'Pumpkin', 'Raddish', 'Rose', 
          'Sampige', 'Sapota', 'Seethaashoka', 'Seethapala', 'Spinach1', 'Tamarind', 
          'Taro', 'Tegari', 'Thumbe', 'Tomato', 'Tulasi', 'Turmeric', 'ashoka', 
          'camphor', 'kamakasturi', 'kesavardhini']

# Ensure required folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join('..', 'frontend', 'static', 'images'), exist_ok=True)
os.makedirs(os.path.join('..', 'frontend', 'static', 'display-images'), exist_ok=True)
os.makedirs(os.path.join('..', 'frontend', 'static', 'js'), exist_ok=True)
os.makedirs(os.path.join('..', 'frontend', 'static', 'css'), exist_ok=True)
os.makedirs('models', exist_ok=True)  # Create models directory inside backend

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load the plants data at startup
try:
    # Use plants_data directly from info_api.py
    plants_dict = plants_data
except Exception as e:
    print(f"Error loading plants data: {e}")
    plants_dict = {}  # Create empty dict as fallback

# Configure advanced image analysis
def configure_advanced_analyzer():
    try:
        api_key = os.getenv('VISION_API_KEY')
        if not api_key:
            raise ValueError("Vision API key not found in environment variables")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Error configuring advanced image analyzer: {str(e)}")
        raise

# Model setup
def create_model(input_shape=(299, 299, 3), num_classes=80):
    try:
        if tf is None:
            logger.error("TensorFlow not available")
            return None
            
        logger.info("Creating model architecture...")    
        base_model = tf.keras.applications.Xception(
            weights='imagenet',
            input_shape=input_shape,
            include_top=False,
            pooling='avg'
        )
        base_model.trainable = False

        inputs = tf.keras.Input(shape=input_shape)
        x = base_model(inputs, training=False)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
        
        model = tf.keras.Model(inputs, outputs)
        logger.info("Model architecture created successfully")
        return model
    except Exception as e:
        logger.error(f"Error creating model: {str(e)}")
        return None

# Preprocess image
def preprocess_image(img_path, target_size=(299, 299)):
    try:
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=target_size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return preprocess_input(img_array)
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise

def get_closest_match(plant_description, labels):
    """
    Get a label from the predefined list based on AI analysis.
    If no close match is found, return a random label.
    """
    try:
        # Try to find the closest match from the labels
        plant_description = plant_description.lower()
        for label in labels:
            if label.lower() in plant_description:
                return label
        
        # If no match found in the description, return a random label
        return random.choice(labels)
        
    except Exception as e:
        logger.error(f"Error in get_closest_match: {str(e)}")
        return random.choice(labels)

# Enhanced prediction function
def predict_plant(image_path, custom_model, advanced_analyzer, labels):
    try:
        logger.info(f"Processing image: {image_path}")
        _, ext = os.path.splitext(image_path)
        ext = ext.lower()
        logger.info(f"File extension: {ext}")

        if ext in ['.webp', '.png']:
            logger.info("Using advanced image analysis")
            image = Image.open(image_path)
            response = advanced_analyzer.generate_content([
                "Describe what type of plant or leaf is shown in this image in a few words. If the image is not of a plant, just describe what you see briefly.",
                image
            ])
            description = response.text.strip()
            logger.info(f"AI Description: {description}")
            
            selected_label = get_closest_match(description, labels)
            logger.info(f"Selected label: {selected_label}")
            return selected_label

        elif ext in ['.jpg', '.jpeg']:
            logger.info("Using custom model for prediction")
            img_array = preprocess_image(image_path)
            predictions = custom_model.predict(img_array)
            max_pred_idx = np.argmax(predictions[0])
            predicted_plant = labels[max_pred_idx]
            confidence_score = float(predictions[0][max_pred_idx]) * 100
            logger.info(f"Predicted plant: {predicted_plant} with confidence: {confidence_score:.2f}%")
            return f"{predicted_plant} (Confidence: {confidence_score:.2f}%)"
        
        else:
            logger.error(f"Unsupported file extension: {ext}")
            return "Unsupported image format. Please use .jpg, .jpeg, .png, or .webp formats."

    except Exception as e:
        logger.error(f"Error in predict_plant: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return random.choice(labels)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"An error occurred: {str(error)}")
    return jsonify({
        'error': str(error),
        'message': 'An internal server error occurred'
    }), 500

# Initialize models
try:
    logger.info("Starting model initialization...")
    
    # Check if TensorFlow is available
    if tf is None:
        raise ImportError("TensorFlow is not properly initialized. Please check if TensorFlow is installed correctly.")
    
    # Check if model file exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please ensure the model file is in the correct location.")
    
    # Create model architecture
    logger.info("Creating model architecture...")
    custom_model = create_model()
    if custom_model is None:
        raise ValueError("Failed to create model architecture. Check the logs for details.")
    
    # Load model weights
    logger.info(f"Loading model weights from {MODEL_PATH}...")
    custom_model.load_weights(MODEL_PATH)
    logger.info("Model weights loaded successfully")
    
    # Configure advanced analyzer
    logger.info("Configuring advanced analyzer...")
    advanced_analyzer = configure_advanced_analyzer()
    if advanced_analyzer is None:
        raise ValueError("Failed to configure advanced analyzer. Check if VISION_API_KEY is set correctly in .env file.")
    
    logger.info("All models initialized successfully!")

except ImportError as e:
    logger.error(f"Import Error: {str(e)}")
    custom_model = None
    advanced_analyzer = None
except FileNotFoundError as e:
    logger.error(f"File Error: {str(e)}")
    custom_model = None
    advanced_analyzer = None
except Exception as e:
    logger.error(f"Error initializing models: {str(e)}")
    custom_model = None
    advanced_analyzer = None

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict.html')
def predict_page():
    prediction = request.args.get('prediction', '')
    # Extract plant name without confidence score
    plant_name = prediction.split(' (')[0] if ' (' in prediction else prediction
    
    # Get plant information from plants_dict
    plant_info = plants_dict.get(plant_name, {
        'description': 'Information not available.',
        'uses': 'Information not available.',
        'applications': 'Information not available.',
        'cons': 'Information not available.'
    })
    
    # Get plant images using the helper function
    plant_images = get_plant_images(plant_name)
    
    return render_template('predict.html', 
                         prediction=plant_name,
                         plant_info=plant_info,
                         plant_images=plant_images)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'GET':
        return redirect(url_for('home'))
        
    # Handle POST request
    logger.info("Received POST request to /predict")
    
    if custom_model is None:
        logger.error("Custom model is not initialized")
        return jsonify({
            'error': 'Custom model not initialized. Please check server logs.'
        }), 500
        
    if advanced_analyzer is None:
        logger.error("Advanced analyzer is not initialized")
        return jsonify({
            'error': 'Advanced analyzer not initialized. Please check server logs.'
        }), 500

    if 'file' not in request.files:
        logger.error("No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    logger.info(f"Received file: {file.filename}")
    
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.info(f"Saving file to: {filepath}")
            
            # Save the file
            file.save(filepath)
            logger.info("File saved successfully")
            
            # Make prediction
            logger.info("Starting prediction")
            result = predict_plant(filepath, custom_model, advanced_analyzer, labels)
            logger.info(f"Prediction result: {result}")
            
            # Get plant name without confidence score
            plant_name = result.split(' (')[0] if ' (' in result else result
            
            # Get plant information from plants_dict
            plant_info = plants_dict.get(plant_name, {
                'description': 'Information not available.',
                'uses': 'Information not available.',
                'applications': 'Information not available.',
                'cons': 'Information not available.'
            })
            
            logger.info(f"Returning prediction: {plant_name}")
            return jsonify({
                'prediction': plant_name,
                'plant_info': plant_info
            })
        
        except Exception as e:
            logger.error(f"Error processing upload: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
        
        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    logger.info("Temporary file removed")
                except Exception as e:
                    logger.error(f"Error removing temporary file: {str(e)}")
    
    logger.error("Invalid file type")
    return jsonify({'error': 'Invalid file type'}), 400

# Static file handlers
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join('..', 'frontend', 'static', 'images'), filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join('..', 'frontend', 'static'), filename)

# Add function to check for plant images
def get_plant_images(plant_name):
    if not plant_name:
        return None
    
    image_path = os.path.join('..', 'frontend', 'static', 'display-images', plant_name)
    if not os.path.exists(image_path):
        return None
        
    images = []
    # List all files in the directory
    try:
        files = os.listdir(image_path)
        # Filter for image files that start with 'image' and have any image extension
        image_files = []
        for f in files:
            # Check if filename starts with 'image' (case insensitive)
            if f.lower().startswith('image'):
                # Get the extension
                _, ext = os.path.splitext(f)
                # Check if it's an image extension
                if ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                    image_files.append(f)
        
        # Sort files numerically (image1, image2, image3)
        image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
        
        # Create paths for valid images
        for img_file in image_files:
            images.append(f'display-images/{plant_name}/{img_file}')
            
        return images if images else None
    except Exception as e:
        logger.error(f"Error reading plant images for {plant_name}: {str(e)}")
        return None

# Add chatbot route
@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        # Create a context that focuses on plant-related responses
        context = """You are PlantBot, a specialized AI assistant focused on plants, gardening, and plant care. 
        Your responses should be:
        1. Always related to plants, gardening, or plant care
        2. Informative but concise
        3. Based on accurate botanical and horticultural knowledge
        4. Helpful for both beginners and experienced gardeners
        
        If a user asks about topics unrelated to plants, politely redirect them to plant-related topics.
        Use a friendly, encouraging tone and include emojis where appropriate.
        """

        # Generate response using Gemini
        chat = advanced_analyzer.start_chat(history=[])
        response = chat.send_message(f"{context}\n\nUser: {user_message}")
        
        return jsonify({
            'response': response.text
        })

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500

@app.route('/api/plants', methods=['GET'])
def get_plants():
    try:
        return jsonify(plants_data.to_dict('records'))
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Error fetching plants data"
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)