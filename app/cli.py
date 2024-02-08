from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import asyncio
from aioconsole import ainput

console = Console()

async def get_user_name():
    question = "What is your name?"
    console.print(question, style="bold bright_magenta")
    user_response = await ainput("> ")
    return user_response


async def get_search_query():
    question = "What category of professional are you aiming to connect with? Specify the industry or area of expertise you're interested in for leads using a keyword format."
    instruction = "You can search for multiple keywords separated by SPACES. Too many keywords (3+) will greatly limit the amount and/or quality of suggested leads."
    console.print(question, style="bold bright_magenta")
    console.print(instruction, style="dim")
    user_response = await ainput("> ")
    return user_response

async def get_message_length():
    question = "Does your message to leads have any length constraints?\n" \
               "[1] Quick note\n" \
               "[2] 280 characters - Twitter/X post\n" \
               "[3] 300 characters - LinkedIn connection request message\n"
    console.print(question, style="bold bright_magenta")
    choices = ['1', '2', '3']
    while True:
        user_choice = await ainput("> ")  # Await user input asynchronously
        if user_choice in choices:
            break
        console.print("Please select a valid option.", style="bold red")

    length_mapping = {
        '1': "150",
        '2': "280",
        '3': "300"
    }
    return length_mapping[user_choice]

async def get_user_context():
    question = "Provide additional context about yourself and or your request (e.g., is there an event or product they may be interested in?)"
    console.print(question, style="bold bright_magenta")
    user_response = await ainput("> ") 
    return user_response

async def get_message_purpose():
    question = "What is the objective of your outreach message?"
    console.print(question, style="bold bright_magenta")
    user_response = await ainput("> ")
    return user_response


async def get_message_tone():
    question = "Choose the tone for your outreach message:\n" \
               "[1] Professional\n" \
               "[2] Chill\n" \
               "[3] Persuasive\n" \
               "[4] Warm\n"
    console.print(question, style="bold bright_magenta")
    choices = ['1', '2', '3', '4']
    while True:
        user_choice = await ainput("> ")  # Await user input asynchronously
        if user_choice in choices:
            break
        console.print("Please select a valid option.", style="bold red")

    tone_mapping = {
        '1': 'Professional',
        '2': 'Chill',
        '3': 'Persuasive',
        '4': 'Warm'
    }
    return tone_mapping[user_choice]

async def profile_search_pref():
    question = "Would you like to search for this person's LinkedIn profile?\n" \
               "[1] Yes\n" \
               "[2] No\n"
    console.print(question, style="bold bright_magenta")
    choices = ['1', '2']
    while True:
        user_choice = await ainput("> ")  # Await user input asynchronously
        if user_choice in choices:
            break
        console.print("Please select a valid option.", style="bold red")

    profile_mapping = {
        '1': True,
        '2': False,
    }
    return profile_mapping[user_choice]


async def main_cli(lead_category=None):
    message_length = await get_message_length()
    message_purpose = await get_message_purpose()
    user_context = await get_user_context()
    message_tone = await get_message_tone()
    
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
    asyncio.run(main_cli())
