import os
import twilio
import twilio.rest
import twilio.twiml
import requests
import praw
from flask import request

from flask import Flask
application = Flask(__name__)

# twilio credentials, phone numbers, etc.
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_TOKEN")
DAN_NUMBER = os.environ.get("DAN_NUMBER")
RENS_NUMBER = os.environ.get("RENS_NUMBER")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")

@application.route('/')
def home():
    return 'Welcome'

@application.route('/call_dan')
def call_dan():

  _make_call("Dan", DAN_NUMBER)
  return "success"


@application.route('/call_rens')
def call_rens():

  _make_call("Rens", RENS_NUMBER)
  return "success"


@application.route('/message', methods=['GET', 'POST'])
def get_twiml_message():

  first_name = request.args.get('first_name')
  reddit_post_title = _top_reddit_post()

  message_to_send = "Hi {}.  This is Rens.  The top headline on reddit is, {}.  Goodbye.".format(first_name, reddit_post_title)
  r = twilio.twiml.Response()
  r.say(message_to_send)

  return str(r)


def _make_call(name, to_phone_number):
  client = twilio.rest.TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
 
  call = client.calls.create(to=to_phone_number,
                      from_=DAN_NUMBER,
                      url="http://" + SITE_DOMAIN + "/message?first_name="+name)    


def _top_reddit_post():
  title = ""

  try:
    r = praw.Reddit(user_agent='tile_reader')
    posts = list(r.get_front_page(limit=1))  
    title = posts[0].title
  except:
    # to-do error handling
    title = "unknown"

  return title


if __name__ == '__main__':
  application.run(debug=True)


