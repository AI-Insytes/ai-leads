import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def people_search_profiles(search_query):
    """
    
    """

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

def get_profile_from_publication(publication_link):
    """
    
    """

    about_markup = None
    profile_links = []
    profiles_markup = []

    # go to the about page for blog and extract markup containing profile link(s)
    with sync_playwright() as p:
        # setup
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto(publication_link)

        # skip subscription prompt
        skip_button = page.get_by_role("button", name="No thanks")
        if skip_button:
            skip_button.click()

        # extract about page markup with profile link(s)
        about_button = page.get_by_role("button", name="About")
        about_button.click()
        about_markup = page.content()

        browser.close()

    # extract the profile link(s)
    soup = BeautifulSoup(about_markup, "html.parser")
    profile_links_markup = soup.select("div.content-person")
    for profile_link in profile_links_markup:
        link_markup = profile_link.select("a")[0]
        link = link_markup.get("href")
        profile_links.append(link)

    # go to each profile page and extract the markup
    for link in profile_links:

        # store profile markup
        markup = None

        # go to profile page
        with sync_playwright() as p:
            # setup
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            page.goto(link)  

            # extract markup
            markup = page.content()

            browser.close()
        
        profiles_markup.append(markup)    

    return profiles_markup

def publication_search_profiles(search_query):
    """
    
    """

    publication_links = []
    publications_markup = None
    profiles_markup = []   

    with sync_playwright() as p:
        # setup
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://substack.com/home")

        # search
        page.get_by_placeholder("Search...").fill(search_query)
        page.get_by_placeholder("Search...").press("Enter")
        page.get_by_role("button", name="Publications").click()

        # get publications links
        publications_markup = page.content()
        
        browser.close()

    # get publication links
    soup = BeautifulSoup(publications_markup, "html.parser")
    publication_links_markup = soup.select("div.reader2-page-body div div a.pencraft")
    for link in publication_links_markup:
        publication_link = link.get("href")
        publication_links.append(publication_link)

    # get profiles markup
    for publication_link in publication_links[:2]: # TODO testing limit, remove slice for production
        markup = get_profile_from_publication(publication_link)
        profiles_markup += markup

    return profiles_markup

def extract_profiles_data(profiles_markup):
    """
    
    """

    profile_objects = []

    # iterate over each profile markup to extract data
    for markup in profiles_markup:

        # store profile data
        profile = {}

        # parse markup
        soup = BeautifulSoup(markup, "html.parser")

        # extract name
        name_markup = soup.select("h1")[0]
        user_name = name_markup.get_text()
        user_name = user_name.replace("\u00a0", "") # removes non-breaking space in name
        profile["lead-name"] = user_name

        # extract blog
        if soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset"):
            # blog name
            blog_name_markup = soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a h4")[0]
            profile["blog-name"] = blog_name_markup.get_text()
            # blog link
            blog_link_markup = soup.select("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a")[0]
            blog_link = blog_link_markup.get("href")
            blog_link = "/".join(blog_link.split("/", 3)[:3]) # truncates url to base domain
            profile["blog-link"] = blog_link

        # extract profile links
        profile_links_markup = soup.select("#dialog6 div div a")
        for link in profile_links_markup:
            link_name_markup = link.select("div")[0]
            link_name = link_name_markup.get_text()
            profile[link_name] = link.get("href")

        profile_objects.append(profile)

    return profile_objects

def main(search_query):
    """
    
    """

    # people search
    profiles_markup = people_search_profiles(search_query)
    people_profile_objects = extract_profiles_data(profiles_markup)

    # publications search
    publication_profiles_markup = publication_search_profiles(search_query)
    publication_profile_objects = extract_profiles_data(publication_profiles_markup)

    # combine profile objects
    combined_profile_objects = people_profile_objects + publication_profile_objects
    # removes duplicates
    # merged_profile_objects = list(set(combined_profile_objects)) # TODO remove duplicates

    # for profile_object in combined_profile_objects:
    #     for key, value in profile_object.items():
    #         print(f"{key}: {value}")

    profile_objects_json = json.dumps(combined_profile_objects, indent=4)

    return profile_objects_json
