# OpenRouter Python API Client

A simple and reusable Python function to interact with the Llama 3 model via the OpenRouter API. This client is designed to be easily integrated into any Python project.

### Features

* **Simple Functionality:** A single, clean function (`generate_content`) to handle API calls.

* **Conversation Memory:** Designed to work with a list of messages to maintain conversation history.

* **Error Handling:** Includes robust `try-except` blocks to manage API and HTTP errors gracefully.

### Prerequisites

* Python 3.6 or later

* An API key from [OpenRouter](https://openrouter.ai/)

### Installation

1.  **Clone the repository:**

2.  **Install the necessary Python libraries:**
    This project requires the `requests` library to make HTTP calls.

    ```
    pip install -r requirements.txt
    ```
### Configuration
1.  Open the `generate_content.py` file.
2.  Replace `"YOUR_API_KEY_HERE"` with your actual API key from OpenRouter.
### Usage
To use the function, simply import it into your script and pass a list of message dictionaries.
Here is a full example of how to use the function to have a multi-turn conversation:
```python
# my_app.py
from generate_content import generate_content
# The conversation history starts empty.
conversation_history = []
def chat_with_llama(prompt):
    """
    A simple function to add a new message and get a response.
    """
    # Add the new user message to the history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Get the response from the model
    response_text = generate_content(conversation_history)
    
    # Add the model's response to the history
    conversation_history.append({"role": "assistant", "content": response_text})
    
    return response_text
# --- Example of a conversation turn ---
print("Llama: Hello! How can I help you today?")
user_message_1 = input("You: ")
response_1 = chat_with_llama(user_message_1)
print(f"Llama: {response_1}")
# A follow-up question
user_message_2 = input("You: ")
response_2 = chat_with_llama(user_message_2)
print(f"Llama: {response_2}")
```
