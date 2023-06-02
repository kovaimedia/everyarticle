import requests
import feedparser
import json
from bs4 import BeautifulSoup
import time
import scrapy
import scrapydo
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from pipelines import PIBPipeline

pib_articles = []

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


class PIBSpider(scrapy.Spider):
    name = 'pib'
    start_urls = ['https://www.pib.gov.in/allRel.aspx']

    def parse(self, response):
        # Select ministry option    
        ministry_option = response.xpath(f'//*[@id="ContentPlaceHolder1_ddlMinistry"]/option[text()="{self.option}"]')
        ministry_option_value = ministry_option.attrib['value']
        ministry_option_text = ministry_option.xpath('string()').get()
        yield scrapy.FormRequest.from_response(
            response,
            formid='ContentPlaceHolder1_ddlMinistry',
            formdata={'ctl00$ContentPlaceHolder1$ddlMinistry': ministry_option_value},
            callback=self.parse_day
        )

    def parse_day(self, response):
        # Select day option
        day_option = response.xpath(f'//*[@id="ContentPlaceHolder1_ddlday"]/option[text()="{self.day}"]')
        day_option_value = day_option.attrib['value']
        day_option_text = day_option.get()
        yield scrapy.FormRequest.from_response(
            response,
            formid='ContentPlaceHolder1_ddlday',  # Replace with the actual form ID
            formdata={'ctl00$ContentPlaceHolder1$ddlday': day_option_value},
            callback=self.parse_articles
        )

    def parse_articles(self, response):
        articles = []
        article_elements = response.xpath('//*[@id="form1"]/section[2]/div/div[7]/div/div/ul/li/ul')

        if not article_elements:
            print("No data found")
        else:
            for article_element in article_elements:
                title_element = article_element.xpath('.//a')
                title = title_element.xpath('string()').get()
                href = title_element.attrib['href']
                href = response.urljoin(href)
                articles.append({"title": title, "link": href, "source": self.source_txt})
                pib_articles.append({"title": title, "link": href, "source": self.source_txt})
            print("Articles:", articles)
            yield {"articles": articles}  # Yield the scraped articles as an item


def getFrom_PIB(option, day, source_txt):
    
    def collect_results(item, spider):
        articles = item['articles']
        results.extend(articles)

    crawler_settings = {
        'ITEM_PIPELINES': {'pipelines.PIBPipeline': 300}
    }

    scrapydo.setup()
    scrapydo.run_spider(
        PIBSpider,
        settings=crawler_settings,
        option=option,
        day=day,
        source_txt=source_txt,
        callbacks=[collect_results]
    )
    
    results = pib_articles
    return results

