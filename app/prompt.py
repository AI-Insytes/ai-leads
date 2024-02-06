import llama2
import requests
import json
from app import cli


def prompt_main(cli_data):
    
    message_purpose = cli_data['purpose']
    lead_name = "Oluchi Enebeli"
    lead_context = "Oluchi Enebeli, a highly sought-after blockchain engineer in Africa..."
    user_context = "I'm reaching out to invite this person to speak at our upcoming web3 conference."
    user_tone = cli_data['tone']
    message_length = cli_data['length']
    
    # Crafting the prompt
    prompt = f"""
    Objective: {message_purpose}
    Lead Name: {lead_name}
    Lead Context: {lead_context}
    User Context: {user_context}
    Message Tone: {user_tone}
    Please craft a personalized message for {lead_name}, incorporating the given objective, background, context and tone. Make this a total of {message_length} characters or less.
    """    
    
    # API endpoint URL
    url = "http://localhost:11434/api/generate"
      

    # Replace these variables with your own values
    model_name = "llama2"  # The model you wish to use
    prompt_text = prompt  # Your prompt to the model

    # Data payload for POST request
    data = {
        "model": "llama2",
        "prompt": prompt_text,
        "stream": False,  # Adjust based on whether you want streaming responses
        # "max_tokens": 50
    }

    # Headers to indicate JSON content
    headers = {
        "Content-Type": "application/json"
    }

    # Sending post request to the API
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the JSON response
        response_data = response.json()
        print("Response from LLM:", response_data.get("response"))
    else:
        print("Failed to get response from the API. Status code:", response.status_code)
    
if __name__ == '__main__':
    prompt_main()