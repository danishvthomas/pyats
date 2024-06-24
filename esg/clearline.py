#!/ws/danthoma-bgl/automation/pyats_venvs/pyats_venv_04_2023/bin/python
import pexpect
import time
import sys
import re
import logging
from pyats.async_ import pcall 


 

def clearConsole(line):
    switch = pexpect.spawn('telnet 10.197.127.12')
    switch.logfile = sys.stdout
    switch.expect("Username:")
    switch.sendline("lab")
    switch.expect("Password:")
    switch.sendline("lab")
    switch.expect("#") 
    for i in range(1,30):
        switch.sendline("clear line {line}".format(line=line))
        switch.expect('[confirm]')
        switch.sendline("\r\n")
        switch.expect("#")

pcall(clearConsole, line=(47,31,17,33,29,30,24,44,41,37,38))

#def ClearLineSwitch(switch,newImage):

# switch = pexpect.spawn('telnet 10.197.127.12')
# switch.logfile = sys.stdout
# switch.expect("Username:")
# switch.sendline("lab")
# switch.expect("Password:")
# switch.sendline("lab")
# switch.expect("#")
# for line in sorted([26,27,28,29,30,31,24,47,37,44,41,44,37]):
#     for i in range(1,30):
#         switch.sendline("clear line {line}".format(line=line))
#         switch.expect('[confirm]')
#         switch.sendline("\r\n")
#         switch.expect("#")
# ~                           