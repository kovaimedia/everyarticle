import requests
from bs4 import BeautifulSoup
import db_functions
from json import dumps
from httplib2 import Http

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

def check_sites_now():
    articles_list = get_from_ETInfra_and_Mint()
    for every_article in articles_list:
        article_title = every_article['title']
        article_url = every_article['link']
        article_source = every_article['source']
        if db_functions.check_article(article_url) == 0:
            db_functions.insert_article(article_title, article_url, article_source)
            trigger_notification(article_title, article_url, article_source)
        
def trigger_notification(article_title, article_url, article_source):
    url = "https://chat.googleapis.com/v1/spaces/AAAARuukzVI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=fhG7J3pAj5PINzAOKQ7wZjQHJrzhOlxvFeSm0cBQ_1o%3D"
  
    message = "\n*New Article from " + article_source + "*\n" + article_title + "\n" + article_url + "\n---\n---\n"

    bot_message = {
        'text': message
    }
    
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
