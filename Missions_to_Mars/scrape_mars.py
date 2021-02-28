from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import pandas as pd
import time


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url_nasa_mars = "https://mars.nasa.gov/news"
    browser.visit(url_nasa_mars)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_partial_text('FULL')
    time.sleep(1)
    url_jpl2 = 'https://www.jpl.nasa.gov' + soup.find('a', class_='button')['data-link']
    browser.visit(url_jpl2)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = 'https://www.jpl.nasa.gov' + soup.find('figure', class_='lede').a['href']

    url_mars_facts = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url_mars_facts)

    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df.set_index('Description', inplace=True)
    
    mars_facts_html = mars_facts_df.to_html(justify='left')

    url_mars_hemisphere = "http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_mars_hemisphere)
    time.sleep(1)

    hemisphere_image_urls = []
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(hemisphere)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        img_url = 'https://web.archive.org/' + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        browser.back()
        time.sleep(1)
    
    browser.quit()

    mars_scrape_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    return mars_scrape_data