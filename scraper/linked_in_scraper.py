from playwright.sync_api import sync_playwright
import pyperclip
from dotenv import load_dotenv
import os

# Specify the name of the environment file
env_file_path = os.path.join(os.path.dirname(__file__), '.env')

# Load environment variables from the specified file
load_dotenv(env_file_path)

def get_profile():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

         # Navigate and log in
        page.goto("https://www.linkedin.com/login")
        str_username = os.getenv('LINKEDIN_USERNAME')
        str_password = os.getenv('LINKEDIN_PASSWORD')
        page.fill('input[name="session_key"]', str_username)
        page.fill('input[name="session_password"]', str_password)
        page.click('button[type="submit"]')
        page.wait_for_selector('input[aria-label="Search"]')

        # Perform search
        search_parameter = "blockchain"
        name = "Kevin Lee"
        combined_query = name + " " + search_parameter
        page.fill('input[aria-label="Search"]', combined_query)
        page.press('input[aria-label="Search"]', 'Enter')
        page.wait_for_selector('div.search-results-container')

        # Click on the "People" filter button
        page.click('button:has-text("People")')

        # Ensure the page has loaded the results after filtering by "People"
        page.wait_for_selector('div.search-results-container')
        
        # Use a selector to find all profile links that include the name
        profile_links = page.locator(f'a.app-aware-link:has-text("{name}")')

        # Initialize a list to hold all matching profile URLs
        all_profile_urls = []

         # Process the top profile separately
        if profile_links.count() > 0:
            top_profile_url = profile_links.first.get_attribute('href').split('?')[0]
            all_profile_urls.append({"Top Profile URL": top_profile_url})

        # Process the rest of the profiles
        for i in range(1, profile_links.count()):
            profile_url = profile_links.nth(i).get_attribute('href').split('?')[0]
            all_profile_urls.append({"Profile URL": profile_url})

        # Print or process all collected profile URLs
        for item in all_profile_urls:
            print(item)

        # Optionally, write the profile URLs to a text file with identification for the top profile
        with open("profile_urls.txt", "w") as file:
            for item in all_profile_urls:
                if "Top Profile URL" in item:
                    file.write("Top Profile: " + item["Top Profile URL"] + "\n")
                else:
                    file.write(item["Profile URL"] + "\n")

        # Close the browser
        browser.close()


if __name__ == '__main__':
    get_profile()