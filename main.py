from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request
import getfcmtoken
import requests

app = FastAPI()

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root(request: Request):
    request_body = await request.json()
    story = request_body.get("story") 

    headline = story.get("headline")
    story_id = story.get("story-content-id")
    author = story.get("authors")[0]['name']


    # Replace with your authorization token
    auth_token = getfcmtoken.get_fcm_token()

    amar_iid = 'c-rJYjU1RPuq1pSE_cb57F:APA91bGD7oHGev7tm8i5DrueFKu9CjPU1ufCX-tM4r4P94jBJ4lFjJyplatMHjal0UVYWFK5hC0j-4sjBWTKTVhnYsm3I9MFjuHOLd9yTDIgtCoSqLW8O2UAPT3ygNI617zqOFXUO3mO'
    
    # Replace with your notification payload
    payload = {
        "message": {
            "notification": {
                "title": "New Article!",
                "body": headline 
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
    
    return {"R_B": request_body}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}