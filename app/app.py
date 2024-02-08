from app.prompt import prompt_main
from app.cli import main_cli, get_search_query
from app.prompt import get_lead_context, get_lead_name
from app.report import main_report
import asyncio
from app.search import search_main

async def main():
    keyword = await get_search_query()
    scraper_task = asyncio.create_task(search_main(keyword))
    cli_data = await main_cli(keyword)
    await scraper_task
    
    lead_name = await get_lead_name(keyword)
    lead_context = await get_lead_context(keyword)
    
    if lead_name is None or lead_context is None:
        print("Failed to fetch lead name or context. Exiting.")
        return
    
    prompt_main(cli_data, lead_context, lead_name)
    main_report(keyword)


if __name__ == "__main__":
    asyncio.run(main())