import llama2
import requests
from datetime import datetime
import time
import json
from app.file_utils import save_to_file, create_directory
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
import sys


async def prompt_main(cli_data, lead_context, lead_name, user_name):
    
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
    User Name: {user_name}
    Lead Name: {lead_name}
    Lead Context: {lead_context}
    Lead Category: {lead_category}
    User Context: {user_context}
    Message Tone: {user_tone}
    Message Length: {message_length} characters or less
    
    Please craft a short personalized message for {lead_name}, incorporating the given objective, background, context, tone, lead category, and message length. The lead category is the industry or area of expertise the user is looking for connections in. Create a subject line, address the lead by their first name (assuming the name listed first is their first name) and sign the message with the {user_name}.
    
    Limit the length of the message to {message_length} characters.
    """
    
    start_time = datetime.now()
    print("Compiling your leads and messages...")    
    
    # API endpoint URL
    # url = "http://localhost:11434/api/generate"
    url = "https://ol.bohio.me/api/generate" # external endpoint
    
    model_name = "llama2"
    prompt_text = prompt

    # Data payload for POST request
    data = {
        "model": "llama2",
        "prompt": prompt_text,
        "stream": False,
    }

    # Headers to indicate JSON content
    headers = {
        "Content-Type": "application/json"
    }

    # Sending post request to the API
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    message = ''
    try:
        # Parsing the JSON response
        response_data = response.json()
        draft_message = response_data.get("response")
        for i in range(0, len(draft_message), 1000):  # Example: print 1000 characters at a time
            message = draft_message[i:i+1000]
            print(message)
            time.sleep(0.1)  # Give a short pause to allow the buffer to flush
            sys.stdout.flush()  # Flush stdout buffer

        # print("Draft Message:", draft_message)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return  # Stop execution if JSON parsing fails
        
    try:
        # File operations
        base_dir = Path(__file__).resolve().parent.parent / "leads_and_messages"
        create_directory(base_dir)  # Ensure the directory exists
        file_path = base_dir / f"{lead_name.replace(' ', '_')}_message.txt"
        
        # Save the draft message to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(draft_message)
        
        print(f"Draft lead message saved to {file_path}")
    except Exception as e:
        print(f"Error during file operations: {e}")
    
    return message
        
        
async def get_lead_context(leads_data_file_name):
    
    # Dynamically determine the base directory
    base_dir = Path(__file__).resolve().parent.parent / "pseudobase" / "leads_data"

    file_name = f"{leads_data_file_name}_leads.json"
    file_path = base_dir / file_name
    
    # Wait for file to be available and not empty
    while not file_path.exists() or file_path.stat().st_size == 0:
        print(f"Waiting for file {file_name} to be available...")
        await asyncio.sleep(1)  # Sleep for a bit before retrying
    
    # Define a synchronous function to read the file, wrapped for async execution
    def read_file_sync(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
            return None
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
                return context  # Return the first context found

    return None  # Return None if no context is found

async def get_lead_name(leads_data_file_name):
    
    # Dynamically determine the base directory
    base_dir = Path(__file__).resolve().parent.parent / "pseudobase" / "leads_data"

    file_name = f"{leads_data_file_name}_leads.json"
    file_path = base_dir / file_name

    # Wait for file to be available and not empty
    while not file_path.exists() or file_path.stat().st_size == 0:
        print(f"Waiting for file {file_name} to be available...")
        await asyncio.sleep(1)  # Sleep for a bit before retrying

    # Synchronous function to read the file, wrapped for async execution
    def read_file_sync(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"There was an error decoding the JSON from the file {file_name}.")
            return None

    loop = asyncio.get_running_loop()
    leads = await loop.run_in_executor(ThreadPoolExecutor(), read_file_sync, file_path)

    if leads:
        # Returns the name for the first lead
        for lead in leads:
            lead_name = lead.get("lead-name")
            if not lead_name:
                # If "lead-name" is missing or None, use "blog-name" instead
                blog_name = lead.get("blog-name")
                return blog_name if blog_name else "Unknown Blog"
            else:
                return lead_name  # Return the first valid lead name found

    return None  # Return None if no lead name is found

if __name__ == '__main__':
    prompt_main()
