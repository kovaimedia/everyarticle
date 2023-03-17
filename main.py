from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
import getfcmtoken
import requests, json
import os
import checksites

app = FastAPI()

class Msg(BaseModel):
    msg: str

@app.post("/")
async def root(request: Request):
    request_body = await request.json()
    story = request_body

    headline = story["headline"]
    story_id = story["story-content-id"]
    author = story["authors"][0]['name']

    # Replace with your authorization token
    auth_token = getfcmtoken.get_fcm_token()

    #get environment variable named 'amar_iid'
    amar_iid = os.environ.get('amar_iid')
    
    # Replace with your notification payload
    payload = {
        "message": {
            "notification": {
                "title": author,
                "body":  headline
            },
            "data": {
                "notification_type": "article",
                "id": story_id
            },
            "token": amar_iid
        }
    }


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    try:

        # Make the POST request to the FCM API endpoint
        response = requests.post(
            "https://fcm.googleapis.com/v1/projects/skilful-air-122506/messages:send", 
            json=payload,
            headers=headers
        )  
        #return response.status_code # Should be 200 if the notification was sent successfully
    except:
        #return "Error"
        pass
    return {"message":"function ran!"}


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