// Auto-resize textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Format timestamp
function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Add message to chat
function addMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'} animate-message`;
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${content}
        </div>
        <div class="message-time">${formatTime()}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    indicator.style.display = 'block';
}

// Hide typing indicator
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    indicator.style.display = 'none';
}

// Check if message is plant-related
function isPlantRelated(message) {
    const plantKeywords = [
        'plant', 'flower', 'garden', 'grow', 'leaf', 'root', 'seed', 'soil',
        'water', 'sunlight', 'fertilizer', 'prune', 'indoor', 'outdoor',
        'herb', 'tree', 'shrub', 'pest', 'disease', 'bloom', 'care'
    ];
    
    const lowercaseMessage = message.toLowerCase();
    return plantKeywords.some(keyword => lowercaseMessage.includes(keyword));
}

// Handle user message
async function handleUserMessage(message) {
    if (!isPlantRelated(message)) {
        return `I'm specialized in plant-related topics. Could you please ask me something about plants, gardening, or plant care? For example:
        <ul>
            <li>How to care for indoor plants?</li>
            <li>What are common plant diseases?</li>
            <li>Best plants for beginners?</li>
            <li>How to grow herbs at home?</li>
        </ul>`;
    }
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return 'I apologize, but I encountered an error. Please try asking your question again.';
    }
}

// Send message
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (message) {
        // Add user message
        addMessage(message, true);
        
        // Clear input
        input.value = '';
        input.style.height = 'auto';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Get bot response
        const response = await handleUserMessage(message);
        
        // Hide typing indicator and add bot response
        hideTypingIndicator();
        addMessage(response);
    }
}

// Handle suggested questions
function askQuestion(question) {
    const input = document.getElementById('userInput');
    input.value = question;
    sendMessage();
}

// Handle enter key
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Check for pending question from search on page load
document.addEventListener('DOMContentLoaded', function() {
    const pendingQuestion = localStorage.getItem('pendingQuestion');
    if (pendingQuestion) {
        // Clear the pending question
        localStorage.removeItem('pendingQuestion');
        // Set the question in the input
        const input = document.getElementById('userInput');
        input.value = pendingQuestion;
        // Send the message
        setTimeout(sendMessage, 1000); // Small delay for better UX
    }
}); 