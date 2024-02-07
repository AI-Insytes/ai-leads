from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
#from 

console = Console()

def get_search_query():
    question = "What category of professional are you aiming to connect with? Specify the industry or area of expertise you're interested in for leads."
    
    console.print(question, style="bold bright_magenta")  
    
    user_response = Prompt.ask(">", show_default=False)  
    
    return user_response

def get_message_length():
    question = "Does your message to leads have any length constraints?\n" \
               "[1] No limit\n" \
               "[2] 280 characters - Twitter/X post\n" \
               "[3] 300 characters - LinkedIn connection request message\n"
    console.print(question, style="bold bright_magenta")
    choices = ['1', '2', '3']
    user_choice = Prompt.ask(">", choices=choices, show_default=False)
    
    length_mapping = {
        '1': "no length limit", # add code when inputting length_mapping: if message_length is None
        '2': "280",
        '3': "300"
    }
    return length_mapping[user_choice]

def get_user_context():
    question = "Provide additional context about yourself and or your request (e.g., is there an event or product they may be interested in?)"
    console.print(question, style="bold bright_magenta")
    user_response = Prompt.ask(">", show_default=False)  # Use '>' as a simple prompt
    
    return user_response


def get_message_purpose():
    question = "What is the objective of your outreach message?"
    console.print(question, style="bold bright_magenta")
    user_response = Prompt.ask(">", show_default=False)  # Use '>' as a simple prompt
    
    return user_response


def get_message_tone():
    question = "Choose the tone for your outreach message:\n" \
               "[1] Professional\n" \
               "[2] Chill\n" \
               "[3] Persuasive\n" \
               "[4] Warm\n"
    console.print(question, style="bold bright_magenta")  # Print the question with style
    choices = ['1', '2', '3', '4']
    user_choice = Prompt.ask(">", choices=choices, show_default=False)  # Use '>' as a simple prompt
    
    tone_mapping = {
        '1': 'Professional',
        '2': 'Chill',
        '3': 'Persuasive',
        '4': 'Warm'
    }
    return tone_mapping[user_choice]

def main_cli():
    lead_category = get_search_query()
    #run scrape_leads(user_response)
    message_length = get_message_length()
    message_purpose = get_message_purpose()
    user_context = get_user_context()
    message_tone = get_message_tone()
    
    console.print(f"Lead category: [bold green]{lead_category}[/bold green]")
    console.print(f"Selected length: [bold green]{message_length if message_length is not None else 'No limit'}[/bold green]")
    console.print(f"Message purpose: [bold green]{message_purpose}[/bold green]")
    console.print(f"Message context: [bold green]{user_context}[/bold green]")
    console.print(f"Selected tone: [bold green]{message_tone}[/bold green]")
    
    cli_data = {
        "query": lead_category,
        "length": message_length,
        "purpose": message_purpose,
        "context": user_context,
        "tone": message_tone,
    }

    return cli_data

if __name__ == "__main__":
    main_cli()