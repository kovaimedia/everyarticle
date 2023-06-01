import sitescripts
import db_functions
from json import dumps
from httplib2 import Http
import pytz
from datetime import datetime
import asyncio


    
Nitin_Gadkari_alert = "https://www.google.com/alerts/feeds/10475738491546675429/9073726971275308502"
MORTH_alert = "https://www.google.com/alerts/feeds/10475738491546675429/14736463604676785656"
RRTS_alert = "https://www.google.com/alerts/feeds/10475738491546675429/5870660820628805083"
vande_bharat = "https://www.google.com/alerts/feeds/10475738491546675429/7073915936907604684"
MAHSR = "https://www.google.com/alerts/feeds/10475738491546675429/3692549460662323318"
NHSRC = "https://www.google.com/alerts/feeds/10475738491546675429/10590118476679497064"

async def redirect_function(every_pib):
    return await sitescripts.getFrom_PBI(every_pib['option'], every_pib['day'], every_pib['source_txt'])


async def check_sites_now():

    pib_list = [{"option": "Ministry of Road Transport & Highways", "day": "All", "source_txt": "PIB-MORTH"},
                {"option": "Ministry of Railways", "day": "All", "source_txt": "PIB-Railways"}]
   
    # set the timezone to IST
    ist = pytz.timezone('Asia/Kolkata')
    # get the current time in IST
    now = datetime.now(ist)

    print("Starting site check process -> " + str(now))
    
    articles_list = sitescripts.get_from_ETInfra_and_Mint()
    process_articles_list(articles_list)

    articles_list = sitescripts.fetch_rss(
        Nitin_Gadkari_alert, "Nitin Gadkari Alert")
    process_articles_list(articles_list)

    articles_list = sitescripts.fetch_rss(
        MORTH_alert, "MORTH Alert")
    process_articles_list(articles_list)

    articles_list = sitescripts.fetch_rss(
        RRTS_alert, "RRTS Alert")
    process_articles_list(articles_list)
    
    articles_list = sitescripts.fetch_rss(
        vande_bharat, "Vande Bharat Alert")
    process_articles_list(articles_list)

    articles_list = sitescripts.fetch_rss(
        MAHSR, "MAHSR Alert")
    process_articles_list(articles_list)

    articles_list = sitescripts.fetch_rss(
        NHSRC, "NHSRCL Alert")
    process_articles_list(articles_list)

    for every_pib in pib_list:
        #use asyncio to run the function in parallel
        articles_list = await redirect_function(every_pib)
        process_articles_list(articles_list)
        # articles_list = sitescripts.getFrom_PBI(every_pib['option'], every_pib['day'], every_pib['source_txt'])
        # process_articles_list(articles_list)


def process_articles_list(articles_list):
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

