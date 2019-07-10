#!/usr/bin/python

import os
import sys
import subprocess
import time


class log_state:
	def __init__(self):
		self.log=[]
		self.conn=[]
		self.sock=[]

	def record(self):
		os.popen("netstat -p > log.txt").read()
		with open("log.txt", "r") as handle:
			line=0
			for i in handle.readlines():
				self.log.append(i.strip("\n"))
		self.log=self.log[2:]
	def seperate(self):
		while self.log:
			line=self.log.pop()
			if 'Active' in line:
				break
			else:
				self.sock.append(line)
		while self.log:
			self.conn.append(self.log.pop())
	def start(self):
		self.record()
		self.seperate()

# connection status
# Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
# socket status
# Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path

def run():
	conn_f=open("connection_log.txt", "w")
	sock_f=open("socket_log.txt", "w")
	initial=log_state()
	initial.start()
	conn=initial.conn
	sock=initial.sock
	conn_f.write("Changed connections:\n")
	conn_f.write("Status   Time      Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name\n")
	sock_f.write("Changed socket usage:\n")
	sock_f.write("Status   Time       Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path\n")
	while 1:
		temp=log_state()
		temp.start()
		new_conn=[]
		new_sock=[]
		closed_conn=[]
		closed_sock=[]
		for i in temp.conn:
			if i not in conn:
				new_conn.append(i)
		for i in conn:
			if i not in temp.conn:
				closed_conn.append(i)
		for i in temp.sock:
			if i not in sock:
				new_sock.append(i)
		for i in sock:
			if i not in temp.sock:
				closed_sock.append(i)	
		for i in new_conn:
			conn_f.write(" [+]     {:10s} {}\n".format(time.strftime("%H:%M:%S"), i))
			# print("[+] {:10s} {}\n".format(time.strftime("%H:%M:%S"), i))
		for i in closed_conn:
			conn_f.write(" [-]     {:10s} {}\n".format(time.strftime("%H:%M:%S"), i))
		for i in new_sock:
			sock_f.write(" [+]     {:10s} {}\n".format(time.strftime("%H:%M:%S"), i))
		for i in closed_sock:
			sock_f.write(" [-]     {:10s} {}\n".format(time.strftime("%H:%M:%S"), i))
		conn=temp.conn
		sock=temp.sock
		time.sleep(30)


run()


