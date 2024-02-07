import os
import json
import asyncio
from profile_scraper.wordpress_scraper import main as wordpress_search  # Assume this is now async
from profile_scraper.substack_scraper import main as substack_search  # Assume this is now async
from pseudobase.pseudobase import add_to_leads  # Assume this is now async or wrapped accordingly

async def check_leads_data(keyword, sources):
    """
    Asynchronously check if leads data exists for a given keyword.
    """
    # Assuming this function might perform file IO or other async operations in the future
    return False

async def search_leads(keyword, sources):
    """
    Asynchronously search for leads from various sources.
    """
    if sources["wordpress"]:
        wordpress_results = await wordpress_search(keyword)
        await add_to_leads(wordpress_results, "WordPress", keyword)
    if sources["substack"]:
        substack_results = await substack_search(keyword)
        await add_to_leads(substack_results, "Substack", keyword)

async def search_main(input_keyword):
    """
    Main async function to manage the leads search process.
    """

    print("starting scrape")
    keyword = input_keyword.lower()
    sources = {
        "wordpress": True,
        "substack": True,
    }

    leads_data_exists = await check_leads_data(keyword, sources)

    if not leads_data_exists:
        await search_leads(keyword, sources)

### Test #######################
if __name__ == "__main__":
    test_keyword = "blockchain"
    asyncio.run(search_main(test_keyword))
################################
