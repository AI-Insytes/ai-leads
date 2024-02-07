import os
import json
from profile_scraper.wordpress_scraper import main as wordpress_search
from profile_scraper.substack_scraper import main as substack_search
from pseudobase.pseudobase import add_to_leads


def check_leads_data(keyword, sources):
    """
    
    """

    return False
    
    # check if leads data exists for keyword
    # leads_data_path = os.path.join("pseudobase", "leads_data")
    # leads_data_files = os.listdir(leads_data_path)
    # if keyword not in leads_data_files:

def search_leads(keyword, sources):
    """
    Main function to search for leads from various sources
    """

    if sources["wordpress"]:
        wordpress_results = wordpress_search(keyword)
        add_to_leads(wordpress_results, "WordPress", keyword)
    if sources["substack"]:
        substack_results = substack_search(keyword)
        add_to_leads(substack_results, "Substack", keyword)

def search_main(input_keyword):
    """
    
    """

    # TODO check for valid/"good" input
    # normalize keyword
    keyword = input_keyword.lower()

    # TODO prompt user which sources to use
    # search sources
    sources = {
        "wordpress": True,
        "substack": True,
    }

    # check is leads data already exists
    leads_data_exists = check_leads_data(keyword, sources)

    # if leads data already exists, inform user and prompt if they want to refresh leads data
    if leads_data_exists: #TODO
        pass
        # inform user: return? console print?
        # prompt for refresh...
        # if refresh then
        # search_leads()

    # new search
    else:
        search_leads(keyword, sources)


### Test #######################
if __name__ == "__main__":
    test_keywords = "blockchain"
    search_main(test_keywords)
################################
