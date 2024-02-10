from playwright.sync_api import sync_playwright

def main():
  keyword_search = 'AI'
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://medium.com/m/signin')
    print('1')
    page.click('a[href="//medium.com/m/connect/google?state=google-%7Chttps%3A%2F%2Fmedium.com%2F%3Fsource%3Dlogin-------------------------------------%7Clogin&source=login-------------------------------------"]')
    print('2')

    print('3')
    page.wait_for_selector('input[type="email"]')
    print('4')
    page.click('input[type="email"]')
    page.fill('input[type="email"]', 'Keter.Pim1')
    print('5')
    page.keyboard.press('Enter')
    print('6')
    page.wait_for_selector('input[type="password"]')
    print('7')
    page.click('input[type="password"]')
    print('8')
    page.click('span[jsname="V67aGc"]:has-text("Next")')
    # page.keyboard.press('Enter')
    print('9')

    articles = page.query_selector_all('h2[class="am gn li lj lk ll lm ln lo lp lq lr ls lt lu lv lw lx ly lz ma mb mc md me mf mg gb gd ge gg gi bq"]')
    print('10')
    for article in articles:
       article.click()
       search_articles_for_keyword(page, keyword_search)
       page.goBack()
    browser.close()

def search_articles_for_keyword(page, keyword):
   paragraphs = page.query_selector_all('p')
   for paragraph in paragraphs:
      text_content = paragraph.inner_text()
      if keyword.lower() in text_content.lower():
          author_profile = page.query_selector('a[data-testid="authorName]')
          if author_profile:
              author_profile_url = author_profile.get_attribute('href')
              print(f'keyword: {author_profile_url}')
          break

if __name__ == "__main__":
    main()