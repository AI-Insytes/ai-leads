from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path
import csv

# Specify the name of the environment file
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the specified file
load_dotenv(env_file_path)

async def get_profile(pref, lead_name, keyword):
    if pref:
        async with async_playwright() as p:  # Use async with for async context manager
            try:
                # Launch browser
                browser = await p.chromium.launch(headless=True, slow_mo=1000)
                page = await browser.new_page()

                # Navigate and log in
                await page.goto("https://www.linkedin.com/login")
                str_username = os.getenv('LINKEDIN_USERNAME')
                str_password = os.getenv('LINKEDIN_PASSWORD')
                await page.fill('input[name="session_key"]', str_username)
                await page.fill('input[name="session_password"]', str_password)
                await page.click('button[type="submit"]')
                await page.wait_for_selector('input[aria-label="Search"]')

                # Perform search
                search_parameter = keyword
                name = lead_name
                combined_query = name + " " + search_parameter
                await page.fill('input[aria-label="Search"]', combined_query)
                await page.press('input[aria-label="Search"]', 'Enter')
                await page.wait_for_selector('div.search-results-container')

                # Click on the "People" filter button
                await page.click('button:has-text("People")')

                # Ensure the page has loaded the results after filtering by "People"
                await page.wait_for_selector('div.search-results-container')

                # Initialize a set to track unique URLs and a variable for the top profile URL
                unique_urls = set()
                top_profile_url = ""

                # Locator for all profile links that include the specified name
                profile_links = page.locator(f'a.app-aware-link:has-text("{name}")')

                # Check and process the top profile URL separately
                count = await profile_links.count()
                if count > 0:
                    top_profile_url = await profile_links.first.get_attribute('href')
                    top_profile_url = top_profile_url.split('?')[0]
                    unique_urls.add(top_profile_url)  # Ensure the top profile is also considered unique

                # Process the remaining profiles
                for i in range(1, count):
                    profile_url = await profile_links.nth(i).get_attribute('href')
                    profile_url = profile_url.split('?')[0]
                    if profile_url not in unique_urls:
                        unique_urls.add(profile_url)
                        
                # Condition to check if profiles were found
                if not unique_urls:
                    print(f"No profiles found for {lead_name} with keyword '{keyword}'.")
                    
                else:
                    # Print or process the top profile URL distinctly
                    if top_profile_url:
                        print(f"Top Profile URL: {top_profile_url}")

                    # Print or process the rest of the unique profile URLs
                    for url in unique_urls:
                        if url != top_profile_url:  # Avoid repeating the top profile
                            print(f"Profile URL: {url}")
                            
                    # Ensure the directory exists
                    output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'leads_and_messages'))
                    os.makedirs(output_dir, exist_ok=True)

                    
                    # Specify the output file path within the new directory
                    output_file_path = os.path.join(output_dir, f"{lead_name.replace(' ', '_')}_profiles.txt")

                    # Write the unique profile URLs to the text file within the specified directory
                    with open(output_file_path, "w") as file:
                        file.write("Lead Name: " + lead_name + "\n")
                        file.write("Lead Search Query: " + keyword + "\n" )
                        file.write("Top Profile URL: " + top_profile_url + "\n\n")
                        for url in unique_urls:
                            if url != top_profile_url:  # Avoid repeating the top profile
                                file.write(url + "\n")
            except TimeoutError as e:
                print(f"TimeoutError: The operation timed out. {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                await browser.close()  # Ensure the browser is closed even if an error occurs
    return 


### Test #######################
if __name__ == '__main__':
    pref = True
    test_name = "Kevin Lee"
    test_query = "blockchain"
    asyncio.run(get_profile(test_name, test_query))
################################