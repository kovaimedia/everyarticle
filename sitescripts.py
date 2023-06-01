import requests
from bs4 import BeautifulSoup
import time
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.errors import NetworkError

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


async def select_by_visible_text(page, selector, text):
    script = """
    (selector, text) => {
        const options = Array.from(document.querySelectorAll(selector));
        const selectedOption = options.find(option => option.innerText.trim() === text);
        if (selectedOption) {
            selectedOption.selected = true;
            selectedOption.parentElement.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
    """
    await page.evaluate(script, selector, text)

async def getFrom_PBI(option, day, source_txt):
    try:
        try:
            articles = []

            browser = await launch()
            page = await browser.newPage()
            await stealth(page)  # Apply stealth measures to mimic a human-like interaction

            url = "https://www.pib.gov.in/allRel.aspx"
            await page.goto(url)
            await asyncio.sleep(2)

            # Select ministry option
            await page.waitForSelector('#ContentPlaceHolder1_ddlMinistry')
            await select_by_visible_text(page,'#ContentPlaceHolder1_ddlMinistry option', option)
            await page.waitForNavigation()
            # Select day option
            await page.waitForSelector('#ContentPlaceHolder1_ddlday')
            await select_by_visible_text(page,'#ContentPlaceHolder1_ddlday option', day)
            await page.waitForNavigation()
            
            await page.waitForSelector("#ContentPlaceHolder1_ddlMonth")
            await select_by_visible_text(page,'#ContentPlaceHolder1_ddlMonth option', "May")

            # Wait for the results to load
            await asyncio.sleep(5)

            # Extract the article elements
            articles_elements = await page.querySelectorAll('.leftul li')
            if len(articles_elements) == 0:
                print("No data found")
            else:
                for article_element in articles_elements:
                    title_element = await article_element.querySelector('a')
                    title = await page.evaluate('(element) => element.textContent', title_element)
                    href = await page.evaluate('(element) => element.getAttribute("href")', title_element)
                    href = "https://www.pib.gov.in" + href
                    articles.append({"title": title, "link": href, "source": source_txt})

            await browser.close()
            return articles
        except NetworkError as e:
            await asyncio.sleep(2)
            print("Error in Network:", e)
            await browser.close()
            return articles
    except Exception as e:
        articles = []
        await browser.close()
        print("Error in PIB:", e)
        return articles
        