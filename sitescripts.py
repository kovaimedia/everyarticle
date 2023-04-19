import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def get_from_ETInfra_and_Mint():

    url = 'https://infra.economictimes.indiatimes.com/news'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []

    for h3 in soup.find_all('h3'):
        a_tag = h3.find('a')
        if a_tag:
            link = a_tag['href'] 
            text = a_tag.text.strip()
            articles.append({"title": text, "link": link,"source":"ET Infra"})

    url = 'https://www.livemint.com/industry/infrastructure'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    for h3 in soup.find_all('h2'):
        a_tag = h3.find('a')
        if a_tag:
            link = a_tag['href']
            text = a_tag.text.strip()
            articles.append({"title": text, "link": "https://www.livemint.com/industry" + link,"source":"Mint Infra"})


    return articles

import feedparser
import json

def fetch_rss(source_url, source_txt):
    # Parse the RSS feed using the feedparser library
    feed = feedparser.parse(source_url)

    # Create an empty list to store the results
    results = []

    # Iterate over each item in the feed and extract the desired fields
    for item in feed.entries:
        results.append({
            "title": item.title,
            "link": item.link,
            "source": source_txt
            }
            )

    return results


def getFrom_PBI(option, day, source_txt):
    #turn off the chorme browser popup when scraping
    articles = []

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    
    url = "https://www.pib.gov.in/allRel.aspx"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    ministry_select = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlMinistry"))
    ministry_select.select_by_visible_text(option)

    day_select = Select(driver.find_element(By.ID, "ContentPlaceHolder1_ddlday"))
    # select the option tag with text "All"
    day_select.select_by_visible_text(day)

    print(driver.page_source)

    content_area = driver.find_element(By.CLASS_NAME, "leftul")
    # leftul = soup.find("ul", {"class": "leftul"})
    time.sleep(5)
    # find all tag li

    content_area = content_area.find_elements(By.TAG_NAME, "li")
    print(len(content_area))

    if len(content_area) == 0:
        print("No data found")
        return 
    else:
        for li in content_area:
            a = li.find_element(By.TAG_NAME, "a")
            title = a.text
            href = a.get_attribute("href")
            articles.append({"title": title, "link": href,"source":source_txt})
    # close the driver
    driver.quit()
    return articles