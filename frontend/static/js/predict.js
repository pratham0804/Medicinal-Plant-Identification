// Get data from storage
function getStoredData() {
    const prediction = localStorage.getItem('plantPrediction');
    const plantInfo = JSON.parse(localStorage.getItem('plantInfo') || '{}');
    return { prediction, plantInfo };
}

// Update the slider images
function updateSliderImages(plantName) {
    if (!plantName) return;

    const sliderContainer = document.querySelector('.slider');
    if (!sliderContainer) return;

    // Clear existing slides
    sliderContainer.innerHTML = '';

    // Create slides dynamically
    for (let i = 1; i <= 3; i++) {
        const slide = document.createElement('div');
        slide.className = 'slide';
        
        const img = document.createElement('img');
        img.alt = `Plant Image ${i}`;
        
        // Function to try loading image with different extensions
        async function tryLoadImage() {
            const extensions = ['.jpg', '.jpeg', '.png', '.webp'];
            let loaded = false;

            for (const ext of extensions) {
                try {
                    const response = await fetch(`/static/display-images/${plantName}/image${i}${ext}`);
                    if (response.ok) {
                        img.src = response.url;
                        loaded = true;
                        break;
                    }
                } catch (error) {
                    console.log(`Failed to load image with extension ${ext}`);
                }
            }

            if (!loaded) {
                img.src = '/static/images/default.jpg';
            }
        }

        // Try to load the image with any extension
        tryLoadImage();
        
        slide.appendChild(img);
        sliderContainer.appendChild(slide);
    }

    // Initialize the slider with the first slide
    showSlide(0);
}

// Update the page content
function updatePageContent(prediction, plantInfo) {
    // Update plant name in both places
    document.querySelectorAll('.plant-name, #text-section h2').forEach(element => {
        if (element) element.textContent = prediction || 'Plant Name';
    });

    // Update slider images
    updateSliderImages(prediction);

    // Update plant information
    if (plantInfo) {
        const infoSection = document.querySelector('.info-section');
        if (infoSection) {
            // Update description
            const descriptionP = infoSection.querySelector('h3:contains("Description") + p');
            if (descriptionP) descriptionP.textContent = plantInfo.description || 'Information not available.';

            // Update uses
            const usesP = infoSection.querySelector('h3:contains("Uses") + p');
            if (usesP) usesP.textContent = plantInfo.uses || 'Information not available.';

            // Update applications
            const applicationsP = infoSection.querySelector('h3:contains("Applications") + p');
            if (applicationsP) applicationsP.textContent = plantInfo.applications || 'Information not available.';

            // Update precautions
            const consP = infoSection.querySelector('h3:contains("Precautions") + p');
            if (consP) consP.textContent = plantInfo.cons || 'Information not available.';
        }
    }

    // Clear storage after displaying
    localStorage.removeItem('plantPrediction');
    localStorage.removeItem('plantInfo');
}

let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    // Hide all slides
    slides.forEach(slide => slide.style.display = 'none');
    
    // Reset index if out of bounds
    currentSlide = n;
    if (currentSlide >= slides.length) {
        currentSlide = 0;
    }
    if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }
    
    // Show current slide
    if (slides[currentSlide]) {
        slides[currentSlide].style.display = 'block';
    }
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

// Initialize slider
document.addEventListener('DOMContentLoaded', function() {
    // Show first slide
    if (slides.length > 0) {
        showSlide(0);
    }
    
    // Get and display stored data
    const storedData = getStoredData();
    if (storedData) {
        updatePageContent(storedData.prediction, storedData.plantInfo);
    }
});

// Utility function to find elements by text content
Document.prototype.querySelector = Document.prototype.querySelector || function(selector) {
    if (selector.includes(':contains(')) {
        const text = selector.match(/:contains\("(.+)"\)/)[1];
        const elements = document.getElementsByTagName('*');
        for (let element of elements) {
            if (element.textContent.includes(text)) {
                return element;
            }
        }
        return null;
    }
    return document.querySelector(selector);
};