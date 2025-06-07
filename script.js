// script.js
// Frontend JavaScript for AI dish suggestion application
// Handles user input, API communication, and UI updates

// DOM element references
const dishInput = document.getElementById('dish-input');
const suggestionsBox = document.getElementById('suggestions-box');
const loadingIndicator = document.getElementById('loading-indicator');

// Global variables for managing state
let debounceTimer;
let currentSuggestions = [];
let isLoading = false;
let lastSearchTerm = ''; // Track last search to avoid duplicate calls

// Configuration
const DEBOUNCE_DELAY = 150; // Reduced to 150ms for faster response like Google search
const MIN_INPUT_LENGTH = 1; // Start searching after just 1 character
const API_BASE_URL = 'http://localhost:3000'; // Backend server URL

/**
 * Debounce function to limit API calls
 * Prevents making API requests on every keystroke
 * @param {Function} func - The function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
const debounce = (func, delay) => {
    return function(...args) {
        // Clear the previous timer if it exists
        clearTimeout(debounceTimer);
        
        // Set a new timer to call the function after the delay
        debounceTimer = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
};

/**
 * Show loading indicator while fetching suggestions
 */
const showLoading = () => {
    isLoading = true;
    loadingIndicator.style.display = 'block';
};

/**
 * Hide loading indicator
 */
const hideLoading = () => {
    isLoading = false;
    loadingIndicator.style.display = 'none';
};

/**
 * Fetch suggestions from our backend API with optimizations for real-time search
 * @param {string} text - The user input text
 */
const getSuggestions = async (text) => {
    // Trim and normalize input
    const normalizedText = text.trim();
    
    // Don't search for very short inputs or if it's the same as last search
    if (normalizedText.length < MIN_INPUT_LENGTH) {
        hideSuggestions();
        lastSearchTerm = '';
        return;
    }

    // Avoid duplicate searches for the same term
    if (normalizedText === lastSearchTerm) {
        return;
    }

    lastSearchTerm = normalizedText;

    try {
        showLoading();
        
        // Make API request to our backend
        const response = await fetch(`${API_BASE_URL}/suggest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ inputText: normalizedText }),
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();
        
        // Only update if this is still the most recent search
        if (normalizedText === lastSearchTerm) {
            // Store current suggestions for reference
            currentSuggestions = data.suggestions || [];
            
            // Display the suggestions
            displaySuggestions(currentSuggestions);
        }

    } catch (error) {
        console.error("Failed to fetch suggestions:", error);
        
        // Only show error if this is still the current search
        if (normalizedText === lastSearchTerm) {
            showErrorMessage("Unable to fetch suggestions. Please check your connection.");
        }
    } finally {
        hideLoading();
    }
};

/**
 * Display suggestions in the dropdown UI
 * @param {Array} suggestions - Array of suggestion strings
 */
const displaySuggestions = (suggestions) => {
    // If no suggestions, hide the box
    if (!suggestions || suggestions.length === 0) {
        hideSuggestions();
        return;
    }

    // Clear previous suggestions
    suggestionsBox.innerHTML = '';
    
    // Create suggestion items
    suggestions.forEach((suggestion, index) => {
        const div = document.createElement('div');
        div.textContent = suggestion;
        div.classList.add('suggestion-item');
        
        // Add click handler to select suggestion
        div.addEventListener('click', () => {
            selectSuggestion(suggestion);
        });
        
        // Add keyboard navigation support
        div.setAttribute('data-index', index);
        
        suggestionsBox.appendChild(div);
    });

    // Show the suggestions box with animation
    showSuggestions();
};

/**
 * Show the suggestions dropdown
 */
const showSuggestions = () => {
    suggestionsBox.style.display = 'block';
    suggestionsBox.classList.add('show');
};

/**
 * Hide the suggestions dropdown
 */
const hideSuggestions = () => {
    suggestionsBox.style.display = 'none';
    suggestionsBox.classList.remove('show');
};

/**
 * Handle selecting a suggestion
 * @param {string} suggestion - The selected suggestion text
 */
const selectSuggestion = (suggestion) => {
    // Fill the input with the selected suggestion
    dishInput.value = suggestion;
    
    // Hide the suggestions box
    hideSuggestions();
    
    // Focus back on the input for potential further typing
    dishInput.focus();
    
    // Optional: Log selection for analytics
    console.log('Selected suggestion:', suggestion);
};

/**
 * Show error message to user
 * @param {string} message - Error message to display
 */
const showErrorMessage = (message) => {
    // Clear any existing suggestions
    suggestionsBox.innerHTML = '';
    
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.textContent = message;
    errorDiv.classList.add('suggestion-item', 'error-message');
    
    suggestionsBox.appendChild(errorDiv);
    showSuggestions();
    
    // Auto-hide error after 3 seconds
    setTimeout(hideSuggestions, 3000);
};

/**
 * Handle keyboard navigation in suggestions
 * @param {KeyboardEvent} event - The keyboard event
 */
const handleKeyboardNavigation = (event) => {
    const suggestionItems = suggestionsBox.querySelectorAll('.suggestion-item');
    
    if (suggestionItems.length === 0) return;
    
    const currentActive = suggestionsBox.querySelector('.suggestion-item.active');
    let activeIndex = currentActive ? parseInt(currentActive.getAttribute('data-index')) : -1;
    
    switch (event.key) {
        case 'ArrowDown':
            event.preventDefault();
            activeIndex = Math.min(activeIndex + 1, suggestionItems.length - 1);
            updateActiveItem(suggestionItems, activeIndex);
            break;
            
        case 'ArrowUp':
            event.preventDefault();
            activeIndex = Math.max(activeIndex - 1, 0);
            updateActiveItem(suggestionItems, activeIndex);
            break;
            
        case 'Enter':
            event.preventDefault();
            if (currentActive) {
                selectSuggestion(currentActive.textContent);
            }
            break;
            
        case 'Escape':
            hideSuggestions();
            break;
    }
};

/**
 * Update which suggestion item is highlighted
 * @param {NodeList} items - All suggestion items
 * @param {number} activeIndex - Index of item to highlight
 */
const updateActiveItem = (items, activeIndex) => {
    // Remove active class from all items
    items.forEach(item => item.classList.remove('active'));
    
    // Add active class to current item
    if (items[activeIndex]) {
        items[activeIndex].classList.add('active');
    }
};

/**
 * Initialize example text click handlers
 */
const initializeExamples = () => {
    const exampleTexts = document.querySelectorAll('.example-text');
    
    exampleTexts.forEach(example => {
        example.addEventListener('click', () => {
            const text = example.textContent.replace(/"/g, ''); // Remove quotes
            dishInput.value = text;
            dishInput.focus();
            
            // Trigger search for the example
            getSuggestions(text);
        });
    });
};

// Event Listeners

// Main input event listener with real-time search like Google
dishInput.addEventListener('input', (e) => {
    const inputValue = e.target.value;
    
    // For very short inputs, show suggestions immediately
    if (inputValue.length <= 2) {
        getSuggestions(inputValue);
    } else {
        // For longer inputs, use debouncing to avoid too many API calls
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            getSuggestions(inputValue);
        }, DEBOUNCE_DELAY);
    }
});

// Also listen for keyup events for better responsiveness
dishInput.addEventListener('keyup', debounce((e) => {
    // Skip arrow keys and other navigation keys
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Enter', 'Escape', 'Tab'].includes(e.key)) {
        return;
    }
    
    const inputValue = e.target.value;
    getSuggestions(inputValue);
}, DEBOUNCE_DELAY / 2)); // Faster debounce for keyup

// Keyboard navigation
dishInput.addEventListener('keydown', handleKeyboardNavigation);

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.input-container')) {
        hideSuggestions();
    }
});

// Focus input when page loads
window.addEventListener('load', () => {
    dishInput.focus();
    initializeExamples();
});

// Handle browser back/forward navigation
window.addEventListener('popstate', () => {
    hideSuggestions();
});

// Add CSS for active suggestion highlighting
const style = document.createElement('style');
style.textContent = `
    .suggestion-item.active {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
`;
document.head.appendChild(style);

// Log initialization
console.log('🚀 How to Log Food? initialized');
console.log('💡 Start typing to see detailed dish suggestions with portion sizes!'); 