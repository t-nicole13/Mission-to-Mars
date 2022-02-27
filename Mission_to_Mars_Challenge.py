#!/usr/bin/env python
# coding: utf-8

# # Scrape Mars Data: The News

# In[1]:


# Imprt Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


import pandas as pd


# In[12]:


# Set Executable Path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless = False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time = 1)


# In[5]:


# Set up the html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[9]:


# Let's begin scraping
slide_elem.find('div', class_ = 'content_title')


# In[10]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_ = 'content_title').get_text()
news_title


# In[11]:


# Use parent elements to find the paragraph text
news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
news_p


# # Scrape Mars Data: Featured Image


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# Find the relative image url
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel



# Use the base url to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Scrape Mars Data: Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace = True)
df



df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


html = browser.html
hemis_soup = soup(html, 'html.parser')


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
results = hemis_soup.find_all('div', class_ = 'item')

for r in range(len(results)):
    hemispheres = {}
    browser.find_by_css('a.itemLink h3')[r].click()
    img_url = browser.find_by_text('Sample')['href']
    title = browser.find_by_css('h2.title').text
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    browser.back()
    


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()





