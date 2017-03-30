import os
import time

cmd = 'mpc volume 70'
cmd.split()
os.sys.cmd(cmd)

cmd.split()
cmd = 'mpc play'
os.sys.cmd(cmd)

for i in range(0, 15):
    cmd = 'mpc volume +2'
    cmd.split()
    os.sys.cmd(cmd)
    time.sleep(60)


