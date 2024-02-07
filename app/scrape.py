from profile_scraper.wordpress_scraper import main as wordpress_scraper
from profile_scraper.substack_scraper import main as substack_scraper
# from pseudobase.pseudobase import add_to_leads


def scrape_leads(keyword, wordpress=True, substack=True):
    """
    
    """

    if wordpress:
        wordpress_results = wordpress_scraper(keyword)
        print(wordpress_results)
        # add_to_leads(wordpress_results, "wordpress")
    if substack:
        substack_results = substack_scraper(keyword)
        print(substack_results)
        # add_to_leads(substack_results, "substack")


test_keyword = "blockchain"
scrape_leads()
