from app.prompt import prompt_main
from app.cli import main_cli

def main():
    cli_data = main_cli()
    prompt_main(cli_data)

if __name__ == "__main__":
    main()