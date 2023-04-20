import getfcmtoken
import os

async def push_notif_function(request):
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
        return response.status_code # Should be 200 if the notification was sent successfully
    except:
        return "Error"
        
    
