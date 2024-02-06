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

    profile_objects = []

    for markup in profiles_markup:

        profile = {}

        soup = BeautifulSoup(markup, "html.parser")

        # extract name
        name_markup = soup.select("h1")
        profile["name"] = name_markup.get_text()

        # extract blog link
        if soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset"):
            blog_link_markup = soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a")
            profile["blog"] = blog_link_markup.get("href")

        # extract profile links
        profile_links_markup = soup.select("#dialog6 div div")
        profile_links = {}
        for link in profile_links_markup:
            link_name_markup = link.select("div")
            link_name = link_name_markup.get_text()
            profile_links[link_name] = link.get("href")
        profile["profiles"] = profile_links

        profile_objects.append(profile)

    return profile_objects

def main(search_query):
    """
    
    """


test_query = "blockchain"
search_profiles(test_query)
