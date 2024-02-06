import time
import openai
import os
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key from the OPENAI_API_KEY environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file or environment variables.")

# Instantiate the OpenAI client with the API key
client = openai.OpenAI(api_key=api_key)

# Define the context and objective
client_name = "Oluchi Enebeli"
client_context = "Oluchi Enebeli, a highly sought-after blockchain engineer in Africa, has been instrumental in developing innovative blockchain solutions."
user_context = "I'm reaching out to invite Oluchi to speak at our upcoming web3 conference."
objective = "Send a personalized invitation to Oluchi Enebeli."

try:
    # Create an assistant
    assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    name="Custom Message Creator",
    description=f"Assistant to craft personalized messages for {client_name}."
    )

    # Create a thread for the conversation
    thread = client.beta.threads.create()

    # Send a message in the thread with context
    message_content = f"Objective: {objective}\nClient Name: {client_name}\nClient Context: {client_context}\nUser Context: {user_context}\nPlease craft a personalized message for {client_name}, incorporating the given background and objective."
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content,
    )
    
    start_time = datetime.now()  # Start timing the response generation
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    def wait_on_run_retrieve(run, thread):
        while run.status == 'queued' or run.status == 'in_progress':
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            
            time.sleep(0.5)

        return run
    
    run = wait_on_run_retrieve(run=run, thread=thread)
    end_time = datetime.now()  # End timing after the run is complete
    duration = (end_time - start_time).total_seconds()  # Calculate the duration
    
    # Fetch and print the generated messages
    messages_response = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages_response.data:
        print(f"{message.role.title()}: {message.content}")

    print(f"\nAI response time: {duration} seconds")
    
    
    # Fetch and print the messages after the run completes
    # messages_response = client.beta.threads.messages.list(thread_id=thread.id)
    # print("\nMessages:")
    # for message in messages_response.data:
    #     print(f"{message.role.title()}: {message.content}")



except Exception as e:
    print(f'An error occurred: {e}')



