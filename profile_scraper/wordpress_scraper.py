from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def main(keyword=None):
    authors = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=2000)
        page = browser.new_page()
        if keyword:
            page.goto(f'https://wordpress.com/read/search?q={keyword}&sort=relevance')
        else:
            page.goto('https://wordpress.com/discover')

        prev_scroll_height = page.evaluate('document.body.scrollHeight') / 2
        try:
            while len(authors) < 50:
                html_content = page.content()

                soup = BeautifulSoup(html_content, 'html.parser')

                articles = soup.select('article')
                for article in articles:

                    author_urls = article.select_one('div.reader-avatar.is-compact.has-gravatar a')
                    author_img = article.select_one('div.reader-avatar.is-compact.has-gravatar a img')
                    author_group = article.select_one('div.reader-post-card__byline-details div.reader-post-card__byline-site a.reader-post-card__site.reader-post-card__link')
                    author_blog_sites = article.select_one('div.reader-post-card__byline-details div.reader-post-card__author-and-timestamp span.reader-post-card__byline-secondary a.reader-post-card__byline-secondary-item')
                    author_url = None
                    author_name = None
                    author_group_name = None
                    author_blog_site = None
                    if author_urls:
                        author_url = "https://wordpress.com" + author_urls.get('href')
                    if author_img:
                        author_name = author_img.get('alt')
                    if author_group:
                        author_group_name = author_group.get_text()
                    if author_blog_sites:
                        author_blog_site = author_blog_sites.get('href')
                    authors[author_name] = {"url": author_url, "blog-name": author_group_name, "blog-url": author_blog_site, "name": author_name}
                page.evaluate(f'window.scrollTo(0, {prev_scroll_height} + 100)')
                page.wait_for_timeout(500)
                more_articles = page.query_selector_all('article')
                if not more_articles:
                    print("No more articles to load.")
                    break
                current_scroll_height = page.evaluate('document.body.scrollHeight')
                if current_scroll_height == prev_scroll_height:
                    print("No more content loaded.")
                    break
                prev_scroll_height = current_scroll_height
        except Exception as e:
            print(e)
        browser.close()
    return authors

if __name__ == "__main__":
    authors = main('Blockchain')  # keyword can be inputted
    print(len(authors))
