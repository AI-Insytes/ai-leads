import json 
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup 
import asyncio 

async def main(keyword=None): 
    """
    Scrape author information from WordPress Discover or search pages.

    Args:
        keyword (str, optional): Keyword for search. If provided, the function
            will navigate to the WordPress search page with the specified keyword.
            If not provided, it will navigate to the WordPress Discover page.
            Defaults to None.

    Returns:
        list: A list of dictionaries containing author information. Each dictionary
        has the following keys:
        - 'lead-name': Author's name.
        - 'context': Contextual information related to the author's blog or post.
        - 'blog-name': Author's blog name.
        - 'blog-url': URL of the author's blog.
        - 'wordpress-url': URL of the author's WordPress profile.

    Raises:
        Exception: Any unexpected exception encountered during the scraping process.
    """
    authors = [] 
    async with async_playwright() as p: 
        options = { 
            'args': [ 
                '--disable-blink-features=AutomationControlled', 
            ], 
            'slow_mo': 2000 
        } 
        browser = await p.chromium.launch(**options) 
        try: 
            context = await browser.new_context() 
            page = await context.new_page() 

            if keyword: 
                await page.goto(f'https://wordpress.com/read/search?q={keyword}&sort=relevance') 
            else: 
                await page.goto('https://wordpress.com/discover') 
            await page.wait_for_timeout(2000) 
            prev_scroll_height = await page.evaluate('document.body.scrollHeight') / 2 

            while len(authors) < 20: 
                html_content = await page.content() 

                soup = BeautifulSoup(html_content, 'html.parser') 

                articles = soup.select('article') 
                for article in articles: 
                    author_urls = article.select_one('div.reader-avatar.is-compact.has-gravatar a') 
                    author_img = article.select_one('div.reader-avatar.is-compact.has-gravatar a img') 
                    author_group = article.select_one('div.reader-post-card__byline-details div.reader-post-card__byline-site a.reader-post-card__site.reader-post-card__link') 
                    author_blog_sites = article.select_one('div.reader-post-card__byline-details div.reader-post-card__author-and-timestamp span.reader-post-card__byline-secondary a.reader-post-card__byline-secondary-item:nth-last-of-type(2)') 
                    author_blog_contexts = article.select_one('div.reader-post-card__post div.reader-post-card__post-details div.reader-excerpt__content.reader-excerpt') 

                    author_url = None 
                    author_name = None 
                    author_group_name = None 
                    author_blog_site = None 
                    author_blog_context = None 

                    if author_urls: 
                        author_url = "https://wordpress.com" + author_urls.get('href') 
                    if author_img: 
                        author_name = author_img.get('alt') 
                    if author_group: 
                        author_group_name = author_group.get_text() 
                    if author_blog_sites: 
                        author_blog_site = author_blog_sites.get('href') 
                    if author_blog_contexts: 
                        author_blog_context = author_blog_contexts.get_text() 

                    if author_blog_site != 'null' and author_blog_site is not None: 
                        authors.append({ 
                            "lead-name": author_name,  
                            "context": author_blog_context, 
                            "blog-name": author_group_name,  
                            "blog-url": author_blog_site,  
                            "wordpress-url": author_url 
                        })

                await page.evaluate(f'window.scrollTo(0, {prev_scroll_height} + 100)') 
                await page.wait_for_timeout(500) 
                more_articles = await page.query_selector_all('article') 
                if not more_articles: 
                    # print("No more articles to load.") 
                    break 
                current_scroll_height = await page.evaluate('document.body.scrollHeight') 
                if current_scroll_height == prev_scroll_height: 
                    # print("No more content loaded.") 
                    break 
                prev_scroll_height = current_scroll_height 

            await context.close() 

        except Exception as e: 
            print(e) 
 
    return authors 
 
async def run(): 
    authors_data = await main('Blockchain')  # keyword can be inputted 
    print(authors_data) 

if __name__ == "__main__": 
    asyncio.run(run()) 
