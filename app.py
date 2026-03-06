from flask import Flask, request
from flask_cors import CORS
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
import os

app = Flask(__name__)

# CORS: allow frontend origins (dev + production)
# Set CORS_ORIGINS in Railway for production frontend URL, e.g. https://your-app.vercel.app
origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173").strip().split(",")
CORS(app, origins=[o.strip() for o in origins], supports_credentials=True)

ACCOUNT_SID = os.environ.get('TWIML_ACCOUNT_SID')
API_KEY = os.environ.get('TWIML_API_KEY')
API_SECRET = os.environ.get('TWIML_API_SECRET')
TWIML_APP_SID = os.environ.get('TWIML_APP_SID')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/voice", methods=["POST", "GET"])
def voice():
    to_number = request.values.get("To")

    print(request.values)
    print(request.data)

    response = VoiceResponse()
    dial = Dial(callerId="+19283161568")
    dial.number(to_number)

    response.append(dial)
    return str(response)

@app.route("/token")
def token():

    token = AccessToken(
        ACCOUNT_SID,
        API_KEY,
        API_SECRET,
        identity="browser-user"
    )

    grant = VoiceGrant(
        outgoing_application_sid=TWIML_APP_SID
    )

    token.add_grant(grant)

    return {"token": token.to_jwt()}

if __name__ == '__main__':
    app.run()
