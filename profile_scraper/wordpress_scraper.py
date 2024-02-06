from playwright.sync_api import sync_playwright

author_urls = []
commenters = []

def main(keyword=None):
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    if keyword:
      page.goto(f'https://wordpress.com/read/search?q={keyword}&sort=relevance')
    else:
      page.goto('https://wordpress.com/discover')
    articles = page.query_selector_all('article')
    length = len(articles)
    print("length: " + str(length))
    for article in articles:
      print('new article')
      url = article.query_selector('div.reader-avatar.is-compact.has-gravatar a')
      if url:
        print('new url')
        author_urls.append("https://wordpress.com" + url.get_attribute('href'))
        print("https://wordpress.com/" + url.get_attribute('href'))
      # article.click()
      # # search_articles(page, keyword)
      # page.wait_for_timeout(2000)
      # all_pages = page.context.pages
      # if len(all_pages) > 1:
      #   all_pages[1].close()
    browser.close()

def search_articles(page, keyword):
  # page.wait_for_selector('*.comments')
  # print('1')
  # comment_list_items = page.query_selector_all('ol:is(.comment-list, .commentlist)')
  # print('2')
  # for comment in comment_list_items:
  #   print('3')
  #   comment.scroll_into_view()
  #   avatar = comment.query_selector('img.avatar.avatar-42.wp-hovercard-attachment.grav-hashed.grav-hijack')

  #   if avatar:
  #     avatar.hover()
  #     page.wait_for_selector('div.gravatar-hovercard.wp-hovercard')
  #     link = page.query_selector('a[class=gravatar-hovercard__profile-link]').get_attribute('href')
  #     print(link)
  #     commenters.append(link)
  pass

if __name__ == "__main__":
    main('Blockchain') # keyword can be inputted
