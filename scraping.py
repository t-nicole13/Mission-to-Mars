# Import Splinter, Beautiful Soup, and Pandas
from dataclasses import dataclass
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Connect to Mongo
def scrape_all():
    # Set Up Splinter
    # Initialize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store the results in a dictionary data
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    # Stop the webdriver and return data
    browser.quit()
    return data


# Scrape Mars Data: The News
def mars_news(browser):

    # Visit the Mars news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:    
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_ = 'content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_ = 'content_title').get_text()
        # Use parent elements to find the paragraph text
        news_paragraph = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_paragraph


# ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
    
    except AttributeError:
        return None


    # Use the base url to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## Mars Facts

def mars_facts():
    try:    
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
        
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace = True)



    return df.to_html()


  

# Tell Flask Our Script is Complete and Ready for Action
if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())







