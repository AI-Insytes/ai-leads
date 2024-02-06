from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def search_profiles(search_query):
    """
    
    """

    profiles_markup = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://substack.com/home")

        page.get_by_placeholder("Search...").fill(search_query)
        page.get_by_placeholder("Search...").press("Enter")
        page.get_by_role("button", name="People").click()

        profiles_count = len(page.query_selector_all("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-paddingBottom-16.pc-reset"))
        
        for index in range(0, 6):

            profiles_links = page.query_selector_all("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-paddingBottom-16.pc-reset")

            profiles_links[index].click()

            if page.query_selector("#trigger5"):
                page.click("//*[@id='trigger5']")
                markup = page.content()
                profiles_markup.append(markup)

            page.go_back()

        browser.close()
    
    return profiles_markup

def extract_profiles(profiles_markup):
    """
    
    """


test_query = "blockchain"
search_profiles(test_query)
