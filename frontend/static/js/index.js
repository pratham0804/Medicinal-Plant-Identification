// Debug logging utility
function debugLog(message) {
  console.log(message);
  const debugElement = document.getElementById('debug');
  if (debugElement) {
      debugElement.innerHTML += `<p class="debug-message">${new Date().toLocaleTimeString()}: ${message}</p>`;
  }
}

// Handle file upload and prediction
function handleFileUpload(file) {
  if (!file) {
      debugLog('No file selected');
      return;
  }

  debugLog(`File selected: ${file.name}`);
  
  // Validate file type
  const validTypes = ['image/jpg','image/jpeg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
      debugLog('Invalid file type');
      alert('Please select a valid image file (JPG, PNG, or WebP)');
      return;
  }

  const formData = new FormData();
  formData.append('file', file);
  debugLog('Preparing to send request to server...');

  // Show loading state
  const loadingElement = document.getElementById('loading');
  if (loadingElement) loadingElement.style.display = 'block';

  fetch('/predict', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      debugLog(`Server response status: ${response.status}`);
      if (!response.ok) {
          throw new Error(`Server returned ${response.status}: ${response.statusText}`);
      }
      return response.json();
  })
  .then(data => {
      debugLog(`Prediction received: ${JSON.stringify(data)}`);
      
      if (data.error) {
          throw new Error(data.error);
      }

      // Store both prediction and plant info
      try {
          localStorage.setItem('plantPrediction', data.prediction);
          localStorage.setItem('plantInfo', JSON.stringify(data.plant_info));
          debugLog('Data stored successfully');

          // Redirect to results page
          window.location.href = `/predict.html?prediction=${encodeURIComponent(data.prediction)}`;
      } catch (e) {
          debugLog(`Storage error: ${e.message}`);
          alert('Error saving prediction. Please try again.');
      }
  })
  .catch(error => {
      debugLog(`Error occurred: ${error.message}`);
      alert(`Error: ${error.message}`);
  })
  .finally(() => {
      if (loadingElement) loadingElement.style.display = 'none';
  });
}

// Initialize file input handler
document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            handleFileUpload(file);
        });
        debugLog('File input handler initialized');
    } else {
        debugLog('Warning: imageInput element not found');
    }
});

// Function to store the uploaded image and navigate to prediction page
function goToPlantInfo() {
    const imageInput = document.getElementById('imageInput').files[0];
    const loadingAnimation = document.getElementById('loadingAnimation');
    
    if (imageInput) {
        loadingAnimation.classList.add('show');
        const reader = new FileReader();
        reader.onload = function() {
            localStorage.setItem('uploadedImage', reader.result);
            window.location.href = '/predict';
        };
        reader.readAsDataURL(imageInput);
    } else {
        alert('Please upload an image first.');
    }
}