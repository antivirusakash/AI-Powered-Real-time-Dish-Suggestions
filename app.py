#!/usr/bin/env python3
"""
AI Powered Real-time Dish Suggestions - Python Flask Backend
Converted from Node.js Express server

AI Powered Real-time dish suggestions with portion sizes for accurate calorie tracking.
Uses Azure OpenAI GPT 4.1 Nano for intelligent, format-aware food suggestions.
"""

import os
import re
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
# This keeps our API credentials secure and out of the source code
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for all routes (equivalent to Express cors middleware)
CORS(app)

# Configure Azure OpenAI settings
openai.api_type = "azure"
openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
openai.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2025-01-01-preview')
openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')

# Content-filter compliant prompt that respects user's typing style
# Incorporates user's exact input format while providing food suggestions
SYSTEM_PROMPT = """You are a helpful food logging assistant. Based on user input, suggest 5 food entries that incorporate their typing style and format preferences.

USER PREFERENCES:
Location: Bengaluru, India
Diet: Non-Vegetarian
Goal: Weight Loss

RULES:
- Build upon the user's exact typing format when possible
- If they specify measurements (like "150g"), use similar measurements
- If they use casual terms, match that style
- Provide 5 diverse but related food suggestions
- Format each as: **Food Name (portion info, style)**

EXAMPLES:

Input: "150g chicken breast"
**150g Grilled Chicken Breast (boneless, skinless)**
**150g Baked Chicken Breast (herb seasoned)**
**150g Pan-Seared Chicken Breast (with olive oil)**
**150g Poached Chicken Breast (plain)**
**150g Rotisserie Chicken Breast (skin removed)**

Input: "pizza slice"
**Pizza Slice (cheese, regular crust)**
**Pizza Slice (pepperoni, thin crust)**
**Pizza Slice (margherita, wood-fired)**
**Pizza Slice (veggie, thick crust)**
**Pizza Slice (hawaiian, stuffed crust)**

Input: "1 cup rice"
**1 Cup White Rice (steamed)**
**1 Cup Brown Rice (cooked)**
**1 Cup Basmati Rice (plain)**
**1 Cup Jasmine Rice (fluffy)**
**1 Cup Wild Rice (mixed)**

Adapt to user's format and provide helpful food logging suggestions."""

def parse_ai_response(response_text):
    """
    Parse Azure OpenAI response to extract food suggestions.
    Handles multiple formats for backward compatibility.
    
    Args:
        response_text (str): Raw response from Azure OpenAI
        
    Returns:
        list: List of parsed food suggestions
    """
    suggestions = []
    
    # Parse the new format with bold markdown and line breaks
    # Expected format: **Dish Name (portion, style)**
    if '**' in response_text:
        # Parse bold formatted suggestions
        bold_matches = re.findall(r'\*\*([^*]+)\*\*', response_text)
        if bold_matches:
            suggestions = [match.strip() for match in bold_matches if match.strip()]
            suggestions = suggestions[:5]  # Limit to 5 suggestions
    
    # Fallback parsing for parentheses format (backward compatibility)
    if not suggestions and '(' in response_text and ')' in response_text:
        matches = re.findall(r'([^,\n]+\([^)]+\))', response_text)
        if matches:
            suggestions = [match.strip() for match in matches if match.strip()]
            suggestions = suggestions[:5]
    
    # Final fallback to simple comma/line splitting
    if not suggestions:
        lines = [line.strip() for line in re.split(r'[,\n]', response_text) if line.strip()]
        suggestions = lines[:5]
    
    return suggestions

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/suggest', methods=['POST'])
def suggest():
    """
    API endpoint for getting dish suggestions
    POST /suggest - receives user input and returns AI-generated suggestions
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'inputText' not in data:
            return jsonify({'error': 'inputText is required'}), 400
        
        input_text = data['inputText']
        
        # Don't make API calls for very short inputs (saves costs and improves UX)
        if len(input_text) < 2:
            return jsonify({'suggestions': []})
        
        # Call Azure OpenAI API
        completion = openai.ChatCompletion.create(
            engine=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4.1-nano'),
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f'User typed exactly: "{input_text}"\n\nPlease provide 5 food suggestions that respect and build upon their exact typing format, measurements, and style.'
                }
            ],
            max_tokens=200,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        # Extract and parse the response
        response_text = completion.choices[0].message.content.strip() if completion.choices else ''
        suggestions = parse_ai_response(response_text)
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as error:
        # Log the error for debugging but don't expose details to the client
        print(f"Error calling Azure OpenAI: {error}")
        
        # Provide more specific error messages based on error type
        error_message = 'Failed to fetch suggestions from AI'
        
        if hasattr(error, 'code'):
            if error.code == 'insufficient_quota':
                error_message = 'API quota exceeded. Please try again later.'
            elif error.code == 'invalid_api_key':
                error_message = 'Invalid API credentials.'
            elif error.code == 'model_not_found':
                error_message = 'AI model not available.'
        
        return jsonify({'error': error_message}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to verify server is running"""
    return jsonify({
        'status': 'OK',
        'message': 'Server is running',
        'aiProvider': 'Azure OpenAI',
        'model': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4.1-nano'),
        'framework': 'Flask (Python)'
    })

@app.route('/test-ai', methods=['GET'])
def test_ai():
    """Test endpoint to verify Azure OpenAI connection"""
    try:
        completion = openai.ChatCompletion.create(
            engine=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4.1-nano'),
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Azure OpenAI connection successful' if you can read this."
                }
            ],
            max_tokens=50
        )
        
        response_text = completion.choices[0].message.content.strip() if completion.choices else ''
        
        return jsonify({
            'status': 'SUCCESS',
            'response': response_text,
            'framework': 'Flask (Python)'
        })
        
    except Exception as error:
        print(f"Azure OpenAI test failed: {error}")
        return jsonify({
            'status': 'ERROR',
            'error': str(error),
            'framework': 'Flask (Python)'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    
    print(f"🚀 Server running at http://localhost:{port}")
    print(f"📊 Health check: http://localhost:{port}/health")
    print(f"🤖 Suggestion API: POST http://localhost:{port}/suggest")
    print(f"🔧 AI Test: GET http://localhost:{port}/test-ai")
    print(f"🧠 Using Azure OpenAI GPT 4.1 Nano model")
    print(f"🐍 Framework: Flask (Python)")
    
    # Run the Flask development server
    app.run(host='0.0.0.0', port=port, debug=True) 