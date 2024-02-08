from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio


async def get_profile_from_publication(publication_link):
    about_markup = None
    profile_links = []
    profiles_markup = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=1000, headless=False)
        page = await browser.new_page()
        await page.goto(publication_link)

        skip_button = page.get_by_role("button", name="No thanks")
        if skip_button:
            await skip_button.click()

        about_button = page.get_by_role("button", name="About")
        await about_button.click()
        about_markup = await page.content()

        await browser.close()

    soup = BeautifulSoup(about_markup, "html.parser")
    profile_links_markup = soup.select("div.content-person")
    for profile_link in profile_links_markup:
        link_markup = profile_link.select("a")[0]
        link = link_markup.get("href")
        profile_links.append(link)

    for link in profile_links:
        async with async_playwright() as p:
            browser = await p.chromium.launch(slow_mo=1000, headless=False)
            page = await browser.new_page()
            await page.goto(link)

            markup = await page.content()

            await browser.close()

        profiles_markup.append(markup)

    return profiles_markup

async def publication_search_profiles(search_query):
    publication_links = []
    publications_markup = None
    profiles_markup = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(slow_mo=1000, headless=False)
        page = await browser.new_page()
        await page.goto("https://substack.com/home")

        await page.get_by_placeholder("Search...").fill(search_query)
        await page.get_by_placeholder("Search...").press("Enter")
        await page.get_by_role("button", name="Publications").click()

        publications_markup = await page.content()

        await browser.close()

    soup = BeautifulSoup(publications_markup, "html.parser")
    publication_links_markup = soup.select("div.reader2-page-body div div a.pencraft")
    for link in publication_links_markup:
        publication_link = link.get("href")
        publication_links.append(publication_link)

    for publication_link in publication_links[:2]:  # Adjusted for testing
        markup = await get_profile_from_publication(publication_link)
        profiles_markup += markup

    return profiles_markup

def extract_profiles_data(profiles_markup):
    profile_objects = []

    for markup in profiles_markup:
        profile = {}
        soup = BeautifulSoup(markup, "html.parser")

        name_markup = soup.select_one("h1")
        if name_markup:
            user_name = name_markup.get_text().replace("\u00a0", "")
            profile["lead-name"] = user_name

        blog_name_markup = soup.select_one("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a h4")
        if blog_name_markup:
            profile["blog-name"] = blog_name_markup.get_text()

        blog_link_markup = soup.select_one("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-gap-16.pc-reset a")
        if blog_link_markup:
            blog_link = blog_link_markup.get("href")
            blog_link = "/".join(blog_link.split("/", 3)[:3])
            profile["blog-link"] = blog_link

        profile_links_markup = soup.select("#dialog6 div div a")
        for link in profile_links_markup:
            link_name = link.select_one("div").get_text() if link.select_one("div") else "Profile Link"
            profile[link_name] = link.get("href")

        profile_objects.append(profile)

    return profile_objects

async def main(search_query):

    publication_profiles_markup = await publication_search_profiles(search_query)
    publication_profile_objects = extract_profiles_data(publication_profiles_markup)

    return publication_profile_objects


if __name__ == "__main__":
    search_query = "blockchain"  # Replace with your actual search query
    result = asyncio.run(main(search_query))
    print(result)
