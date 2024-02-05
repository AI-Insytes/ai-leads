from playwright.sync_api import sync_playwright
import pyperclip
from dotenv import load_dotenv
import os

# Specify the name of the environment file
env_file_path = os.path.join(os.path.dirname(__file__), '.env')

# Load environment variables from the specified file
load_dotenv(env_file_path)

def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        # Navigate to LinkedIn and wait for the navigation to complete
        page.goto("https://www.linkedin.com/login")

        # Retrieve environment variables for username and password
        str_username = os.getenv('LINKEDIN_USERNAME')
        str_password = os.getenv('LINKEDIN_PASSWORD')

        # Fill in the username and password fields and submit
        page.fill('input[name="session_key"]', str_username)
        page.fill('input[name="session_password"]', str_password)
        page.click('button[type="submit"]')

        # Wait for the home page to load by checking for a specific element that indicates the page has loaded
        page.wait_for_selector('input[aria-label="Search"]')

        search_parameter = "blockchain"
        name = "Adryenn Ashley"
        combined_query = name + " " + search_parameter

        # Use the search bar
        page.fill('input[aria-label="Search"]', combined_query)
        page.press('input[aria-label="Search"]', 'Enter')

        # Wait for the results page to load
        page.wait_for_selector('div.search-results-container')

        # Adjust the selector to specifically target the "View full profile" link of the top result.
        # This might require more specificity based on actual page structure.
        # Example: page.click('text=View full profile')
        page.click('a:has-text("View full profile")')

        # Wait for the profile page to load and copy the URL
        page.wait_for_selector('div.ph5')
        profile_url = page.url
        print(f"Profile URL: {profile_url}")

        # Optionally, copy the URL to the clipboard using pyperclip
        pyperclip.copy(profile_url)

        # Close the browser
        browser.close()


if __name__ == '__main__':
    # str_username = os.getenv('canvas_username')
    # str_password = os.getenv('canvas_password')
    # str_clipboard = str(pyperclip.paste())
    main()