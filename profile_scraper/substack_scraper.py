from playwright.sync_api import sync_playwright

def search_profiles(search_query):
    """
    
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        page.goto("https://substack.com/home")

        page.get_by_placeholder("Search...").fill(search_query)
        page.get_by_placeholder("Search...").press("Enter")
        page.get_by_role("button", name="People").click()

        profiles = page.query_selector_all("div.pencraft.pc-display-flex.pc-flexDirection-column.pc-paddingBottom-16.pc-reset")

        profiles[0].click()
        page.go_back()
        profiles[1].click()


    

test_query = "blockchain"
search_profiles(test_query)
