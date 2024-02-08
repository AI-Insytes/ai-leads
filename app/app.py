from app.prompt import prompt_main
from app.cli import main_cli, get_search_query, get_user_name, profile_search_pref
from app.prompt import get_lead_context, get_lead_name
from app.report import main_report
import asyncio
from app.search import search_main
from app.linked_in_search import get_profile

async def main():
    user_name = await get_user_name()
    keyword = await get_search_query()
    scraper_task = asyncio.create_task(search_main(keyword))
    cli_data = await main_cli(keyword)
    await scraper_task
    
    lead_name = await get_lead_name(keyword)
    lead_context = await get_lead_context(keyword)
    
    prompt_main(cli_data, lead_context, lead_name, user_name)
    main_report(keyword)
    pref = await profile_search_pref()
    await get_profile(pref, lead_name, keyword)


if __name__ == "__main__":
    asyncio.run(main())
    