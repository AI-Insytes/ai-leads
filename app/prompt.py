import llama2
import requests
import time
from datetime import datetime
import json
from app import cli
from app.file_utils import save_to_file, create_directory
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio


def prompt_main(cli_data, lead_context, lead_name):
    
    message_purpose = cli_data['purpose']
    lead_category = cli_data['query']
    lead_name = lead_name or "JB"
    lead_context = lead_context or "Blockchain"
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
    Message Length: {message_length}
    Please craft a personalized message for {lead_name}, incorporating the given objective, background, context, tone, and lead category. The lead category is the industry or area of expertise the user is looking for connections in. Make this message a total of {message_length} characters or less. Create a subject line, address the lead by their first name (assuming the name listed first is their first name) and sign the message.
    """
    
    start_time = datetime.now()
    print("Compiling your leads and messages...")    
    
    # API endpoint URL
    url = "http://localhost:11434/api/generate"
    # url = "https://ol.bohio.me/api/generate" # external endpoint
    
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
        # Parsing the JSON response
        response_data = response.json()
        draft_message = response_data.get("response")
        print("Draft Message:", draft_message)
        print(f"Type of draft_message: {type(draft_message)}, Length: {len(draft_message)}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return  # Stop execution if JSON parsing fails
        
    try:
        # File operations
        directory_name = "leads_and_messages"
        filename = f"{lead_name.replace(' ', '_')}_message.txt"
        create_directory(directory_name)
        save_to_file(draft_message, directory_name, filename)
    except Exception as e:
        print(f"Error during file operations: {e}")
        
        
async def get_lead_context(lead_category):
    
    # Dynamically determine the base directory
    base_dir = Path(__file__).resolve().parent.parent / "pseudobase" / "leads_data"

    file_name = f"{lead_category}_leads.json"
    file_path = base_dir / file_name
    
    # Define a synchronous function to read the file
    def read_file_sync(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file {file_name} was not found. Retrying...")
        except json.JSONDecodeError:
            print(f"There was an error decoding the JSON from the file {file_name}.")
        return None

    # Use run_in_executor to run the synchronous file read operation in a thread pool
    loop = asyncio.get_running_loop()
    leads = await loop.run_in_executor(ThreadPoolExecutor(), read_file_sync, file_path)

    if leads:
        for lead in leads:
            context = lead.get("context")
            if context:
                # print(context)
                return context  # Return the first context found

    return None  # Return None if no context is found

async def get_lead_name(lead_category):
    # Dynamically determine the base directory
    base_dir = Path(__file__).resolve().parent.parent / "pseudobase" / "leads_data"

    file_name = f"{lead_category}_leads.json"
    file_path = base_dir / file_name

    # Define a synchronous function to read the file
    def read_file_sync(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
        except json.JSONDecodeError:
            print(f"There was an error decoding the JSON from the file {file_name}.")
        return None

    # Use run_in_executor to run the synchronous file read operation in a thread pool
    loop = asyncio.get_running_loop()
    leads = await loop.run_in_executor(ThreadPoolExecutor(), read_file_sync, file_path)

    if leads:
        # Assuming you want to return the name of the first lead
        for lead in leads:
            lead_name = lead.get("lead-name")  # Use the correct key based on your JSON structure
            if lead_name:
                # print(lead_name)
                return lead_name  # Return the first lead name found

    return None  # Return None if no lead name is found

if __name__ == '__main__':
    prompt_main()