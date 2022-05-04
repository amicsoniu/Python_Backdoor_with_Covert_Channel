ATTACKER:

In a terminal, navigate to the directory containing source code.

Start the ATTACKER with ./attacker.sh

Four options will be provided:
	- 1. Execute Command
		-- INPUT   = Linux command
		-- OUTPUT  = Results of the Linux command from the BACKDOOR's device
		-- EXAMPLE = pwd 
	- 2. Watch Directory
		-- INPUT   = Directory on the BACKDOOR
		-- OUTPUT  = All events occuring inside the specified director
		-- EXAMPLE = /root/Desktop/Final
	- 3. Download File
		-- INPUT 1 = Directory on the BACKDOOR
		-- INPUT 2 = File within the directory spcified
		-- OUTPUT  = File from the BACKDOOR
		-- EXAMPLE = /root/Desktop/Final
		-- EXAMPLE = keylogs.txt
	- 4. Quit
		-- INPUT   = 4
		-- OUTPUT  = Exits ./attacker.sh
		-- EXAMPLE = 4

To force quit, press Ctrl + C as many times as needed, or Ctrl + Z once.

##############################################################################################################
BACKDOOR:

In a terminal, navigate to the directory containing source code.

Start the BACKDOOR with python2 backdoor.py

Start the keylogger with python2 app.py

From here, the BACKDOOR will operate on its own.

To force quit, press Ctrl + C once.

###############################################################################################################
CONFIG:

There is a config file called config.txt

It is responsible for telling the ATTACKER and BACKDOOR which ports to use and where the devices are

Line by line, the configuration is as follows:


Line 1: ATTACKER IP Address
Line 2: BACKDOOR IP Address
Line 3: TCP Port for sending packets
Line 4: Protocol for packet crafting
Line 5: Timeout (in seceonds) between packets

All other lines are not called by the programs.

###############################################################################################################
DEPENDENCIES:

These programs require Python 2 to function along with all necessary modules.

They are as follows:

Get Pip2 for Python 2 with:
	curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
	python2 get-pip.py

Then use Pip2 to install the following modules:
	pip2 install inotify
	pip2 install pycryptodome
	pip2 install scapy
	pip2 install procname
	pip2 install pynput















