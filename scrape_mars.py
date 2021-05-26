# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

def scrape_mars_news():

    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_info["news_title"] = soup.find('li', class_='slide').find('div', class_='content_title').text
    mars_info["news_paragraph"] = soup.find('li', class_='slide').find('div', class_='article_teaser_body').text
        
    return mars_info

def scrape_mars_image():

    browser = init_browser()

    # Visit Mars Space Images url through splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    
    featured_image_url = main_url + featured_image_url
    mars_info["featured_image_url"] = featured_image_url 
        
    return mars_info

def scrape_mars_facts():
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about Mars
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    mars_df = tables[0]
    # Rename the columns and set Parameter as index
    mars_df.columns = ['Parameter', 'Description']
    mars_df.set_index('Parameter', inplace = True)
    html_table = mars_df.to_html()
    mars_info["mars_facts"] = html_table

    return mars_info

def scrape_mars_hemispheres():
    browser = init_browser()
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
        hemisphere_img_url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        hemisphere_img_urls.append({'title': title, 'img_url': hemisphere_img_url})
    mars_info["hemisphere_img_urls"] = hemisphere_img_urls
    
    return mars_info