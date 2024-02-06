from playwright.sync_api import sync_playwright
# import pyperclip
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
        
        # Initialize a set to track unique URLs and a variable for the top profile URL
        unique_urls = set()
        top_profile_url = ""

        # Locator for all profile links that include the specified name
        profile_links = page.locator(f'a.app-aware-link:has-text("{name}")')

        # Check and process the top profile URL separately
        if profile_links.count() > 0:
            top_profile_url = profile_links.first.get_attribute('href').split('?')[0]
            unique_urls.add(top_profile_url)  # Ensure the top profile is also considered unique

        # Process the remaining profiles
        for i in range(1, profile_links.count()):
            profile_url = profile_links.nth(i).get_attribute('href').split('?')[0]
            if profile_url not in unique_urls:
                unique_urls.add(profile_url)

        # Print or process the top profile URL distinctly
        if top_profile_url:
            print(f"Top Profile URL: {top_profile_url}")

        # Print or process the rest of the unique profile URLs
        for url in unique_urls:
            if url != top_profile_url:  # Avoid repeating the top profile
                print(f"Profile URL: {url}")
                
        # Ensure the directory exists
        output_dir = os.path.join(os.path.dirname(__file__), 'scraper_outputs')
        os.makedirs(output_dir, exist_ok=True)

        # Specify the output file path within the new directory
        output_file_path = os.path.join(output_dir, "profile_urls.txt")

        # Write the unique profile URLs to the text file within the specified directory
        with open(output_file_path, "w") as file:
            file.write("Top Profile URL: " + top_profile_url + "\n\n")
            for url in unique_urls:
                if url != top_profile_url:  # Avoid repeating the top profile
                    file.write(url + "\n")

        # Close the browser
        browser.close()


if __name__ == '__main__':
    get_profile()