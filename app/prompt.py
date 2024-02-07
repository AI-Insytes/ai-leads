import llama2
import requests
import time
from datetime import datetime
import json
from app import cli
from app.file_utils import save_to_file, create_directory


def prompt_main(cli_data):
    
    message_purpose = cli_data['purpose']
    lead_category = cli_data['query']
    lead_name = "Oluchi Enebeli"
    lead_context = "Oluchi Enebeli, a highly sought-after blockchain engineer in Africa"
    user_context = cli_data['context']
    user_tone = cli_data['tone']
    message_length = cli_data['length']
    
    # Crafting the prompt
    prompt = f"""
    Objective: {message_purpose}
    Lead Name: {lead_name}
    Lead Context: {lead_context}
    Lead Category: {lead_category}
    User Context: {user_context}
    Message Tone: {user_tone}
    Please craft a personalized message for {lead_name}, incorporating the given objective, background, context, tone, and lead category. The lead category is the industry or area of expertise the user is looking for connections in. Make this message a total of {message_length} characters or less. Create a subject line, address the lead by their first name (assuming the name listed first is their first name) and sign the message.
    """
    
    start_time = datetime.now()
    print("Compiling your leads and messages...")    
    
    # API endpoint URL
    url = "http://localhost:11434/api/generate"
    # url = "https://ol.bohio.me/api/generate" # external endpoint
      

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
    
    
    try:

        # Checking if the request was successful
        # Parsing the JSON response
        response_data = response.json()
        draft_message = response_data.get("response")
        print("Draft Message:", draft_message)
        
        # Define the directory and filename where you want to save the message
        directory_name = "leads_and_messages"
        filename = f"{lead_name.replace(' ', '_')}_message.txt"

        # ensure the directory exists before trying to save
        create_directory(directory_name)
        
        # save the message to the specified file
        save_to_file(draft_message, directory_name, filename)
        
        end_time = datetime.now()  # End timing after the run is complete
        duration = (end_time - start_time).total_seconds()
        print(f"\nAI response time: {duration} seconds")
        
        
    except Exception as e:
        print("Failed to get response from the API. Status code:", response.status_code)
        print(f'An error occurred: {e}')
    
if __name__ == '__main__':
    prompt_main()