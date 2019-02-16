#!/usr/bin/env python

"""
Simple application that logs on to the APIC and displays all
of the faults on all the Tenants.
If a particular tenant is given, shows all the faults of that tenant
and cotinuously keeps logging the faults.
"""
import requests
import acitoolkit as ACI
from acitoolkit import Faults
from credentials import *
import argparse

cli_args = argparse.ArgumentParser("Post to Spark", "Collects an Access Token to connect to Spark Chatroom")
cli_args.add_argument('-t', '--token', required=True,
                      help="The Access Token provided by https://developer.ciscospark.com/ after login.")
cli_args.add_argument('-r', '--roomid', required=True,
                      help="The Room ID associated with the chatroom used for messages")

args = cli_args.parse_args()
TOKEN = "Bearer {}".format(vars(args)["token"])
ROOM_ID = vars(args)["roomid"]

def main():
    """
    Main execution routine
    """
    description = ('Simple application that logs on to the APIC'
                   ' and displays all the faults. If tenant name is given, '
                   ' shows the faults associated with that tenant')




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

    faults_obj = Faults()
    faults_obj.subscribe_faults(session)
    while faults_obj.has_faults(session):
        if faults_obj.has_faults(session):
            faults = faults_obj.get_faults(session)
            if faults is not None:
                for fault in faults:
                    if fault is not None:
                        print("****************")
                        if fault.descr is not None:
                            print("     descr     : " + fault.descr)
                        else:
                            
                            print("     descr     : " + "  ")
                        print("     code      : " + fault.dn.split('fault-',1)[1])
                        print("     dn        : " + fault.dn)
                        print("     rule      : " + fault.rule)
                        print("     severity  : " + fault.severity)
                        print("     type      : " + fault.type)
                        print("     domain    : " + fault.domain)
                        fault_code = fault.dn.split('fault-',1)[1]
                        post_message_to_spark("{}\n {}".format(fault_code, fault.descr))


def post_message_to_spark(message):
    header = {"Authorization": TOKEN, "Content-Type": "application/json"}
    message_url = "https://api.ciscospark.com/v1/messages"

    request_body = {"roomId": ROOM_ID, "text": message}
    response = requests.post(message_url, json=request_body, headers=header)

    if not response.ok:
        print("FAILED TO SEND {} TO SPARK".format(message))

if __name__ == '__main__':
    main()
