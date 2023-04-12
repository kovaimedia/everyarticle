import requests
from bs4 import BeautifulSoup

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

