from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def search_profiles(search_query):
    """
    
    """

    # store profile pages markup
    profiles_markup = []

    with sync_playwright() as p:
        # setup
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://substack.com/home")

        # search
        page.get_by_placeholder("Search...").fill(search_query)
        page.get_by_placeholder("Search...").press("Enter")
        page.get_by_role("button", name="People").click()

        # count of profile results to iterate
        profiles_count = len(page.query_selector_all("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-paddingBottom-16.pc-reset"))
        
        # iterate over each profile result and extract profile markup
        for index in range(0, 6): # TODO testing number, change to profiles_count for production

            profiles_links = page.query_selector_all("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-paddingBottom-16.pc-reset")

            profiles_links[index].click()

            # only store the profile markup if it has profile links
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

    # store profiles data
    profile_objects = []

    # iterate over each profile markup to extract data
    for markup in profiles_markup:

        # store profile data
        profile = {}

        # parse markup
        soup = BeautifulSoup(markup, "html.parser")

        # extract name
        name_markup = soup.select("h1")[0]
        profile["name"] = name_markup.get_text()

        # extract blog link
        if soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset"):
            blog_link_markup = soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a")[0]
            profile["blog"] = blog_link_markup.get("href")

        # extract profile links
        profile_links_markup = soup.select("#dialog6 div div a")
        profile_links = {}
        for link in profile_links_markup:
            link_name_markup = link.select("div")[0]
            link_name = link_name_markup.get_text()
            profile_links[link_name] = link.get("href")
        profile["profiles"] = profile_links

        profile_objects.append(profile)

    return profile_objects

def main(search_query):
    """
    
    """

    profiles_markup = search_profiles(search_query)

    profile_objects = extract_profiles(profiles_markup)

    for profile_object in profile_objects:
        for key, value in profile_object.items():
            print(f"{key}: {value}")


#####################
### Start Scraper ###
#####################

if __name__ == "__main__":
    test_query = "blockchain"
    main(test_query)
