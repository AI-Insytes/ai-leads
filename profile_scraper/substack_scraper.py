from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio


async def get_profiles_from_publication(publication_link):
    """
    
    """

    about_markup = None
    profile_links = []
    profiles_markup = []
    publication_description = ""

    # go to the publication about page for blog and extract markup
    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=1000)
        page = await browser.new_page()
        await page.goto(publication_link)

        # skip subscription prompt
        skip_button = page.get_by_role("button", name="No thanks")
        if skip_button:
            await skip_button.click()

        # extract about page markup
        about_button = page.get_by_role("button", name="About")
        await about_button.click()
        about_markup = await page.content()

        await browser.close()

    # extract content from publication about page
    soup = BeautifulSoup(about_markup, "html.parser")
    # extract author profile links
    profile_links_markup = soup.select("div.content-person")
    for profile_link in profile_links_markup:
        link_markup = profile_link.select("a")[0]
        link = link_markup.get("href")
        profile_links.append(link)
    # extract publication description
    description_markup = soup.select_one("div.body.markup")
    if description_markup:
        for element in description_markup:
            publication_description += element.get_text()

    # go to each profile page and extract the markup
    for link in profile_links:
        async with async_playwright() as p:
            browser = await p.chromium.launch(slow_mo=1000)
            page = await browser.new_page()
            await page.goto(link)

            markup = await page.content()

            await browser.close()

        profiles_markup.append(markup)

    return profiles_markup, publication_description

async def publication_search_profiles(search_query):
    """
    
    """

    publication_links = []
    publications_markup = None
    profiles_data = []

    # go to the publications page and search matching newsletters
    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=1000)
        page = await browser.new_page(java_script_enabled=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        await page.goto("https://substack.com/home")

        # search
        await page.get_by_placeholder("Search...").fill(search_query)
        await page.get_by_placeholder("Search...").press("Enter")
        await page.get_by_role("button", name="Publications").click()

        # get publications links
        publications_markup = await page.content()

        await browser.close()

    # extract publication links
    soup = BeautifulSoup(publications_markup, "html.parser")
    publication_links_markup = soup.select("div.reader2-page-body div div a.pencraft")
    for link in publication_links_markup:
        publication_link = link.get("href")
        publication_links.append(publication_link)

    # get profiles markup
    for publication_link in publication_links[:2]:  # Adjusted for testing
        profile_data = await get_profiles_from_publication(publication_link)
        profiles_data.append(profile_data)

    return profiles_data

def extract_profiles_data(profiles_data):
    """
    
    """

    profile_objects = []

    for profile_data in profiles_data:
        profiles_markup, publication_description = profile_data

        for markup in profiles_markup:
            profile = {}
            profile["context"] = ""

            soup = BeautifulSoup(markup, "html.parser")

            # extract lead name
            name_markup = soup.select_one("h1")
            if name_markup:
                user_name = name_markup.get_text().replace("\u00a0", "")
                profile["lead-name"] = user_name

            # extract blog name
            blog_name_markup = soup.select_one("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a h4")
            if blog_name_markup:
                blog_name = blog_name_markup.get_text()
                profile["blog-name"] = blog_name
                profile["context"] += f"Newsletter Name: {blog_name}"

            # extract blog link
            blog_link_markup = soup.select_one("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a")
            if blog_link_markup:
                blog_link = blog_link_markup.get("href")
                blog_link = "/".join(blog_link.split("/", 3)[:3])
                profile["blog-link"] = blog_link

            # extract profile links
            profile_links_markup = soup.select("#dialog6 div div a")
            for link in profile_links_markup:
                link_name = link.select_one("div").get_text() if link.select_one("div") else "Profile Link"
                profile[link_name] = link.get("href")

            # add newsletter description to lead context
            profile["context"] += f" Newsletter Description: {publication_description}"

            profile_objects.append(profile)

    return profile_objects

async def main(search_query):
    """
    
    """

    profiles_data = await publication_search_profiles(search_query)
    profile_objects = extract_profiles_data(profiles_data)

    return profile_objects


### Test #################
if __name__ == "__main__":
    search_query = "blockchain"
    result = asyncio.run(main(search_query))
    print(result)
