# Identification of Medical Plant using Machine Learning

A web-based application that uses machine learning to identify medicinal plants from images and provide detailed information about their properties and uses.

## Features

- **Image Upload**: Easy-to-use interface for uploading plant images
- **Real-time Classification**: Instant identification of medicinal plants
- **Detailed Information**: Comprehensive details about identified plants including:
  - Scientific name
  - Medicinal properties
  - Traditional uses
  - Growing conditions
- **Interactive UI**: Modern and responsive design with smooth animations
- **Plant Database**: Extensive database of medicinal plants

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3 with modern animations
  - JavaScript (Vanilla)
  - Font Awesome icons
  
- **Backend**:
  - Python
  - Flask web framework
  - Machine Learning model for plant classification
  - SQLite database for plant information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Identification-of-Medical-Plant-using-Machine-Learning.git
cd Identification-of-Medical-Plant-using-Machine-Learning
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
├── backend/
│   ├── __init__.py
│   ├── model/
│   └── info_api.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
├── app.py
├── requirements.txt
└── README.md
```

## Usage

1. Open the application in your web browser
2. Click on the upload button or drag and drop a plant image
3. Wait for the classification result
4. View detailed information about the identified medicinal plant

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who helped in building this project
- Special thanks to the plant database sources
- Image dataset contributors 