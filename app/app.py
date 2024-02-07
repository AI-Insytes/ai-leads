from app.prompt import prompt_main
from app.cli import main_cli
from app.report import main_report

def main():
    cli_data = main_cli()
    prompt_main(cli_data)
    main_report(cli_data['query'])
    

if __name__ == "__main__":
    main()