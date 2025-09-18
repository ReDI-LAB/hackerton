from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

# --- 1. Get your API Key ---
# You can get a free API key from OpenRouter after creating an account at:
# https://openrouter.ai/
# Simply click "Create Account" and then find your API key in your account settings.
API_KEY = os.getenv("SECRET_KEY")

# The URL for the OpenRouter API endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_content(messages):
    """
    Sends the entire message history to the Llama 3 model via the OpenRouter API
    and returns the generated text.
    
    Args:
        messages (list): A list of message dictionaries representing the conversation history.

    Returns:
        str: The generated text from the model, or an error message.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # The payload structure for OpenRouter's chat completions API
    payload = {
        # Using a valid model name for the Llama 3 8B Instruct model on OpenRouter.
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": messages
    }

    try:
        # Make the POST request to the API
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        result = response.json()
        
        # Extract the generated text from the structured response
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No content generated from the API."

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (e.g., incorrect API key, invalid request)
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Error details: {e.response.text}")
        return "An HTTP error occurred. Please check your API key and request."
    except Exception as e:
        # Handle other potential errors
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."