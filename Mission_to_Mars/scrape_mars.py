from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium import webdriver
import requests
import time

# Execute browser
def init_browser():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Create scrape function to execute scraping code
def scrape():

    
    browser = init_browser()

    # Create empty dictionary to hold scraped data
    scraped_data = {}

    # Mars News url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')

    # Create soup instance
    ''' html = browser.html

    soup = BeautifulSoup(html, 'html.parser')'''

    # Find all News Headlines

    news_title = soup.find('div', class_= "content_title").find('a').text.strip()
    news_p = soup.find('div', class_= "rollover_description_inner").text.strip()

    # Find the first News Headline Paragraph Teaser
    # paragraph = soup.find('div', class_="article_teaser_body").text

    # Create empty list to hold the Headlines
    '''titles = []
    for quote in quotes:

        # Store the headines as title list in titles        
        titles.append(quote.text)'''

    # Unpack the Headline list
    '''news_title = [title for title in titles]'''

    # Extract the first Headline and save in scraped_data 
    scraped_data['news_title'] = news_title

    # Extract the teaser paragraph corresponding to the first headline
    scraped_data['news_p'] = news_p

    # Scrape url of Featured Image

    # Images url link
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Create soup instance
    img_html = browser.html
    soup = BeautifulSoup(img_html, "html.parser")

    # Visit main page
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)

    # Crawl to reach link with full resolution image url
    browser.click_link_by_partial_text('more info')

    # Create soup instance
    new_img_html = browser.html
    new_img_soup = BeautifulSoup(new_img_html, 'html.parser')

    # Find contents of the landing page img tag
    first_img_url = new_img_soup.find('img', class_='main_image')

    # Extract the src containing the final image url
    final_img_url = first_img_url.get('src')

    # Join the main page url and the final page url
    featured_image_url = "https://www.jpl.nasa.gov" + final_img_url

    # Save final url in scraped_data
    scraped_data['featured_image_url'] = featured_image_url

    # Mars Facts

    # Table url
    table_url = 'https://space-facts.com/mars/'

    # Use pandas to extract table contents
    mars_df = pd.read_html(str(table_url))[0]

    # Rename table headers
    mars_df.rename(columns = {0: 'Fact', 1:'Data'}, inplace=True)

    # Export table in html format
    mars_df_html = mars_df.to_html(index = False)

    # Save table in scraped_data
    scraped_data['mars_facts'] = mars_df_html

    # Mars Hemispheres

    # Mars Hemisphere images url
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_hem_site = browser.visit(mars_hem_url)

    # Create soup instance
    mars_hem_html = browser.html
    soup = BeautifulSoup(mars_hem_html, 'html.parser')

    # Get content of image link
    img_items = soup.find_all('div', class_='item')

    # Create empty list for image urls 
    hemisphere_image_urls = []

    # Store the url of the main page
    mars_hemispheres_main = 'https://astrogeology.usgs.gov'

    # Get contents of each individual image link
    for i in img_items:

        # Find the title
        title = i.find('h3').text
        
        # Find url of full image page
        first_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit image landing page
        browser.visit(mars_hemispheres_main + first_img_url)
        
        # Create soup instance
        first_img_url = browser.html
        
        soup = BeautifulSoup( first_img_url, 'html.parser')
        
        # Extract full image url
        img_url = mars_hemispheres_main + soup.find('img', class_='wide-image')['src']
        
        # Save to dictionary with title as key and img_url as value
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        # Save dictionary to scraped_data
        scraped_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return scraped_data


