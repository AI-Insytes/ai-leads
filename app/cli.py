from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

console = Console()

def get_message_length():
    choices = ['1', '2', '3'] 
    question = Text("Does your message to leads have any length constraints?\n"
                    "[1] No limit\n"
                    "[2] 280 characters - Twitter/X post\n"
                    "[3] 300 characters - LinkedIn connection request message\n",
                    style="bold blue")

    user_choice = Prompt.ask(question, choices=choices)
    
    length_mapping = {
        '1': "no length limit", # add code when inputting length_mapping: if message_length is None
        '2': 280,
        '3': 300
    }
    return length_mapping[user_choice]

def get_user_context():
    question = Text("Provide additional context about yourself and or your request (e.g., is there an event or product they may be interested in?)")
    
    user_response = Prompt.ask(question)
    
    return user_response


def get_message_purpose():

    question = Text("What is the objective of your outreach message?\n")
                    
    user_response = Prompt.ask(question)
    
    return user_response


def get_message_tone():
    choices = ['1', '2', '3', '4']  # Define the valid choices
    question = Text("Choose the tone for your outreach message:\n"
                    "[1] Professional\n"
                    "[2] Chill\n"
                    "[3] Persuasive\n"
                    "[4] Warm\n",
                    style="bold blue")
    # Ask the user to choose from the predefined options
    user_choice = Prompt.ask(question, choices=choices)
    
    tone_mapping = {
        '1': 'Professional',
        '2': 'Chill',
        '3': 'Persuasive',
        '4': 'Warm'
    }
    return tone_mapping[user_choice]

def main_cli():
    message_length = get_message_length()
    message_purpose = get_message_purpose()
    user_context = get_user_context()
    message_tone = get_message_tone()
    

    console.print(f"Selected length: [bold green]{message_length if message_length is not None else 'No limit'}[/bold green]")
    console.print(f"Message purpose: [bold green]{message_purpose}[/bold green]")
    console.print(f"Message context: [bold green]{user_context}[/bold green]")
    console.print(f"Selected tone: [bold green]{message_tone}[/bold green]")
    
    cli_data = {
        "length": message_length,
        "purpose": message_purpose,
        "context": user_context,
        "tone": message_tone
    }

    return cli_data

if __name__ == "__main__":
    main_cli()