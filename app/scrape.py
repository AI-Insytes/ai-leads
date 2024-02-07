import os
from profile_scraper.wordpress_scraper import main as wordpress_scraper
from profile_scraper.substack_scraper import main as substack_scraper
from pseudobase.pseudobase import add_to_leads


def scrape_leads(input_keywords, wordpress=True, substack=True, refresh=False):
    """
    
    """

    # parse keywords
    keywords = input_keywords.split(",")
    for keyword in keywords:
        keyword = keyword.lower()


    # run scrapers with keywords
    for keyword in keywords:

        # check if leads data exists for keyword
        leads_data_path = os.path.join("pseudobase", "leads_data")
        leads_data_files = os.listdir(leads_data_path)
        if keyword not in leads_data_files:
            if wordpress:
                wordpress_results = wordpress_scraper(keyword)
                print(wordpress_results)
                # add_to_leads(wordpress_results, "wordpress", keyword, refresh)
            if substack:
                substack_results = substack_scraper(keyword)
                print(substack_results)
                # add_to_leads(substack_results, "substack", keyword, refresh)


test_keywords = "blockchain"
scrape_leads(test_keywords)
