import psycopg2
import datetime
import pytz
import os

#connect using psycopg2 with a connection string
conn = psycopg2.connect(
    dbname="railway",
    user="postgres",
    password= os.getenv("db_password"),
    host= os.getenv("db_host"),
    port="6956"
)


#add article to database
def insert_article(article_title: str, article_url: str, source: str):
    
    #get current date and time in IST timezone and save in time_now
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.datetime.now(tz)    

    cursor = conn.cursor()
    cursor.execute("INSERT INTO scrapped_articles (article_title, article_url, source, time_of_insertion) VALUES (%s, %s, %s)", (article_title, article_url, source, time_now))
    conn.commit()
    cursor.close()
    
    print("Inserting: " + article_title)
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
def get_articles(source):
    cursor = conn.cursor()
    cursor.execute("SELECT article_title, article_url, time_of_insertion FROM scrapped_articles WHERE source = %s ORDER BY id DESC LIMIT 25", (source,))
    articles = cursor.fetchall()
    cursor.close()
    #parse articles into a json
    articles_json = []
    for article in articles:
        articles_json.append({"article_title": article[0], "article_url": article[1], "time_of_insertion": article[2]})
    return articles_json
