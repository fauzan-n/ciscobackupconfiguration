### Script untuk membackup konfigurasi perangkat cisco

import telnetlib
import sys
import os
import subprocess
import time
import datetime

now = datetime.datetime.now()
username = "*****"  # the Username
password = "******"  # the Password
buff = ''
resp = ''
with open('Fetch.txt') as f:
    for line in f:
        line = line.strip()
        with open(os.devnull, "wb") as limbo:
            ip = line
            result = subprocess.Popen(["ping", "-n", "2", "-w", "1000", ip],
                                      stdout=limbo, stderr=limbo).wait()
            if result:
                print
                ip, "Link Down - Site unreachable"
                f = open('DownSites.txt', 'a+')
                f.write(line + '\n')
                f.close()
            else:
                try:
                    tn = telnetlib.Telnet(line)
                    tn.read_until("Username:")
                    tn.write(username + "\n")
                    tn.read_until("Password:")
                    tn.write(password + "\n")
                    tn.write("terminal length 0" + "\n")
                    tn.write("sh ver" + "\n")
                    tn.write("sh processes cpu history" + "\n")
                    tn.write("sh run" + "\n")
                    tn.write("exit" + "\n")
                    output = tn.read_all()
                    print
                    ip, "Reachable ~ Command Executed"
                    tn.close()
                    fp = open(line + '.txt', "w")
                    fp.write(output)
                    fp.close()
                except Exception as e:
                    print
                    ip, "ERROR: ", e