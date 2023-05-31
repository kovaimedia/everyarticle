from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
import checksites
import db_functions
import push_notif
import os

app = FastAPI()

# try:
#     os.system('sudo apt-get update')
#     os.system('sudo apt-get install -y google-chrome-stable')
# except Exception as e:
#     print("Error in installing chromium-browser: ", e)


#use apscheduler to run check_sites every 10 minutes
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(checksites.check_sites_now, 'interval', minutes=10)
scheduler.print_jobs()
scheduler.start()
checksites.check_sites_now()

class Msg(BaseModel):
    msg: str

@app.post("/")
async def root(request: Request):
    return push_notif.push_notif_function(request)

@app.get("/runcheck")
async def run_check():
    checksites.check_sites_now()
    return {"message": "Ran web checks"}

@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}

#route to call get_articles function from db_functions.py
@app.get("/articles/{source}")
async def get_articles(source: str):
    articles = db_functions.get_articles(source)
    return articles



