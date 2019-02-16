#!/usr/bin/env python

import requests
import argparse
from acitoolkit.acitoolkit import *
from credentials import *

requests.packages.urllib3.disable_warnings() # Disable warning message

cli_args = argparse.ArgumentParser("Post to Spark", "Collects an Access Token to connect to Spark Chatroom")
cli_args.add_argument('-t', '--token', required=True,
                      help="The Access Token provided by https://developer.ciscospark.com/ after login.")
cli_args.add_argument('-r', '--roomid', required=True,
                      help="The Room ID associated with the chatroom used for messages")

args = cli_args.parse_args()
TOKEN = "Bearer {}".format(vars(args)["token"])
ROOM_ID = vars(args)["roomid"]

def main():
    session = Session(URL, LOGIN, PASSWORD)
    session.login()

    subscribe_to_events(session)


def subscribe_to_events(session):
    Interface.subscribe(session, only_new=True)
  
    while True:
        if Interface.has_events(session):
            print '<<<<><><><><><><><><><><><><><><><><><>'
            event = Interface.get_event(session) 
            if len(event) == 0:
                print 'NNNNOOOO EVENTS'
            else:
                print event
        

            post_message_to_spark("{}".format(event))

    

def post_message_to_spark(message):
    header = {"Authorization": TOKEN, "Content-Type": "application/json"}
    message_url = "https://api.ciscospark.com/v1/messages"

    request_body = {"roomId": ROOM_ID, "text": message}
    response = requests.post(message_url, json=request_body, headers=header)

    if not response.ok:
        print("FAILED TO SEND {} TO SPARK".format(message))


if __name__ == "__main__":
    main()