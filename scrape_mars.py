# Dependencies
import os
from splinter import Browser, browser
from bs4 import BeautifulSoup 
import requests
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
from webdriver_manager.chrome import ChromeDriverManager

 

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title,paragraph=scrape_mars_news(browser)

    mars_info = {
        'news_title':title,
        'news_paragraph': paragraph,
        'featured_image_url': scrape_mars_image(browser),
        'facts':scrape_mars_facts(),
        'hemispheres':scrape_mars_hemispheres(browser)
    }
    browser.quit()
    return mars_info

def scrape_mars_news(browser):

    

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)  

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_title = soup.find('li', class_='slide').find('div', class_='content_title').text
        news_paragraph = soup.find('li', class_='slide').find('div', class_='article_teaser_body').text
    except:
        return None,None
    return news_title, news_paragraph

def scrape_mars_image(browser):

    # Visit Mars Space Images url through splinter module
    main_url = 'https://spaceimages-mars.com/'
    browser.visit(main_url) 
    browser.links.find_by_partial_text('FULL IMAGE').click()    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:    
        featured_image_url = soup.find('img', class_='fancybox-image')['src']
    except:
        return None

    featured_image_url = main_url + featured_image_url
    return featured_image_url 
        

def scrape_mars_facts():
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about Mars
    facts_url = 'https://space-facts.com/mars/'
    try:
        tables = pd.read_html(facts_url)
    except:
        return None

    mars_df = tables[0]
    # Rename the columns and set Parameter as index
    mars_df.columns = ['Parameter', 'Description']
    mars_df.set_index('Parameter', inplace = True)
    html_table = mars_df.to_html()
    return html_table


def scrape_mars_hemispheres(browser):
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_img_urls = []
    for item in items:
        title = item.find('h3').text
        hemisphere_url = 'https://astrogeology.usgs.gov' + item.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        try:
            hemisphere_img_url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        except: 
            hemisphere_img_url = None
        hemisphere_img_urls.append({'title': title, 'img_url': hemisphere_img_url})
    return hemisphere_img_urls
    