import psycopg2

#Replace the connection parameters with your database details
conn = psycopg2.connect(
    dbname="railway",
    user="postgres",
    password="LbrulJ58CqJxcz6XmpoQ",
    host="containers-us-west-52.railway.app",
    port="7130"
)


#add article to database
async def insert_article(article_title: str, article_url: str, source: str):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articles (article_title, article_url, source) VALUES (%s, %s, %s)", (article_title, article_url, source))
    conn.commit()
    cursor.close()
    return {"article_title": article_title, "article_url": article_url}

#check if article is already in database, use url as unique identifier
async def check_article(article_url: str):
    cursor = conn.cursor()
    cursor.execute("SELECT article_url FROM articles WHERE article_url = %s", (article_url,))
    article = cursor.fetchone()
    cursor.close()
    return article