#!/usr/bin/env python

"""
Simple application that logs on to the APIC and displays all
of the events on all the Tenants.
If a particular tenant is given, shows all the events of that tenant
and cotinuously keeps logging the events.
"""
import requests
import acitoolkit as ACI

from credentials import *
import argparse

# cli_args = argparse.ArgumentParser("Post to Spark", "Collects an Access Token to connect to Spark Chatroom")
# cli_args.add_argument('-t', '--token', required=True,
#                       help="The Access Token provided by https://developer.ciscospark.com/ after login.")
# cli_args.add_argument('-r', '--roomid', required=True,
#                       help="The Room ID associated with the chatroom used for messages")

# args = cli_args.parse_args()
# TOKEN = "Bearer {}".format(vars(args)["token"])
# ROOM_ID = vars(args)["roomid"]

def main():
    """
    Main execution routine
    """
    description = ('Simple application that logs on to the APIC'
                   ' and displays all the events. If tenant name is given, '
                   ' shows the events associated with that tenant')




    # Login to APIC
    session = ACI.Session(URL, LOGIN, PASSWORD)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        return
    # if args.tenant_name is not None:
    #     tenant_name = args.tenant_name
    # else:
    #     tenant_name = None

    #events_obj = ACI.Interface()
    events_obj = ACI.Interface.subscribe(session)
    while ACI.Interface.has_events(session):
        if ACI.Interface.has_events(session):
            events = ACI.Interface.get_event(session)
            if events is not None:
                for event in events:
                    if event is not None:
                        print("****************")
                        if event.descr is not None:
                            print("     descr     : " + event.descr)
                        else:
                            
                            print("     descr     : " + "  ")
                        print("     code      : " + event.dn.split('event-',1)[1])
                        print("     dn        : " + event.dn)
                        print("     rule      : " + event.rule)
                        print("     severity  : " + event.severity)
                        print("     type      : " + event.type)
                        print("     domain    : " + event.domain)
                        fault_code = event.dn.split('event-',1)[1]
                        #post_message_to_spark("{}\n {}".format(fault_code, event.descr))


def post_message_to_spark(message):
    header = {"Authorization": TOKEN, "Content-Type": "application/json"}
    message_url = "https://api.ciscospark.com/v1/messages"

    request_body = {"roomId": ROOM_ID, "text": message}
    response = requests.post(message_url, json=request_body, headers=header)

    if not response.ok:
        print("FAILED TO SEND {} TO SPARK".format(message))

if __name__ == '__main__':
    main()
