from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key from the OPENAI_API_KEY environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file or environment variables.")

# Instantiate the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Define the context and objective
client_name = "Oluchi Enebeli"
client_context = "Oluchi Enebeli, a highly sought-after blockchain engineer in Africa, has been instrumental in developing innovative blockchain solutions."
user_context = "I'm reaching out to invite Oluchi to speak at our upcoming web3 conference."
user_tone = "chill"
objective = "Send a personalized invitation to connect to Oluchi Enebeli."

# Crafting the prompt
prompt = f"""
Objective: {objective}
Client Name: {client_name}
Client Context: {client_context}
User Context: {user_context}
Message Tone: {user_tone}
Please craft a personalized message for {client_name}, incorporating the given background and objective.
"""

try:
    # Generating a response from the GPT model
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who will help craft a professional message aimed at generating a lead"},
            {"role": "user", "content": prompt}
        ],
         max_tokens=150  # Limit the response length
    )
        
    # Iterate through the choices (although there's typically only one choice in chat completions)
    for choice in response.choices:
        # Each 'choice' contains a 'message' with 'content'
        print(choice.message.content)
        
    # Serialize the response to JSON and write to a file
    response_json = response.model_dump_json(indent=2)
    with open('response.json', 'w') as f:
        f.write(response_json)
    
    print(response_json)

except Exception as e:
    print(f'An error occurred: {e}')
