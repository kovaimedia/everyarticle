import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
def get_fcm_token():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('sharpkeys.json', SCOPES)
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/amar/Desktop/Code Base/serverless/packages/mani_dof/trigger_push/sharpkeys.json', SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token
