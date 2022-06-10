# What is this ?
will connect to a thermal printer and print when an item is Queued on Vmix Social.

# What printer this use?
It can use any printer. However the best suggestion is a ECS Pos compatable Thermal printer. 

# How to launch the script?
This script will only run on Windows!

This script should be running on the computer connected to the printer. Before launching the script, you will need to set the IP address of VMix Social. You'll also need to set the default printer to the printer you want this script to use (done this on control panel).

# Setup Page Layout
First, print a queue by launch the script and queue a thread. The printer will print something but the margin would be huge. You can now close the script, and open ```nopol.txt``` using windows Notepad. On File -> Page Setup, set all margins to 0, save the file and print once, save the file again. Now reopen the script and print, the printout should look right.