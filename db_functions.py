import psycopg2
import datetime
import pytz
import os
from dotenv import load_dotenv
import dateutil.parser
import timeago

load_dotenv()

#connect using psycopg2 with a connection string
conn = psycopg2.connect(
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT")
)


#add article to database
def insert_article(article_title: str, article_url: str, source: str):
    
    #get current date and time in IST timezone and save in time_now
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.datetime.now(tz)    

    cursor = conn.cursor()
    cursor.execute("INSERT INTO scrapped_articles (article_title, article_url, source, time_of_insertion) VALUES (%s, %s, %s, %s)", (article_title, article_url, source, time_now))
    conn.commit()
    cursor.close()
    
    print(source +  ": Inserting: " + article_title)
    return {"article_title": article_title, "article_url": article_url}

#check if article is already in database, use url as unique identifier, return 0 if no record found
def check_article(article_url):
    cursor = conn.cursor()
    cursor.execute("SELECT article_url FROM scrapped_articles WHERE article_url = %s", (article_url,))
    article = cursor.fetchone()
    cursor.close()
    if article == None:
        return 0
    else:
        return 1

#get parameter about which source and return 15 latest articles
def get_articles(source_option):
   
    cursor = conn.cursor()
    cursor.execute("SELECT article_title, article_url, time_of_insertion, source, id FROM scrapped_articles WHERE source = %s ORDER BY time_of_insertion DESC LIMIT 25", (source_option,))
    articles = cursor.fetchall()
    cursor.close()
    #parse articles into a json
  
    articles_json = []
    for article in articles:
        
        #get time lapsed between now and article[2] in days, minutes, hours format
        #convert article[2] to datetime object
        tz = pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(tz) 
        time_now = dateutil.parser.parse(time_now.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
        orig_time = dateutil.parser.parse(str(article[2]))   
        #calculate time difference between time_now and orig time in mins
        time_lapsed = timeago.format(time_now, orig_time,'en_short')
        time_lapsed = str(time_lapsed)[3:len(time_lapsed)]

        articles_json.append({"article_title": article[0], "article_url": article[1], "time_of_insertion": article[2], "time_lapsed": time_lapsed, "source_name": article[3], "id": article[4]})
    
    return articles_json

