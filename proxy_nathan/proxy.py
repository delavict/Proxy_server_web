#!/usr/bin/env python
######
#
# proxy.py
# author : Nathan Delavictoire, Edouardo Vasconcileos
#
#
######

import socket
import thread
import sys


MAX_QUEUE  = 5      
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = False  
PORT= 8081
TIMEOUT = 4
HOST = ''

def main():
	start_proxy()
	return 0

def start_proxy():
	# instantiation of the socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	#bind server
	server.bind((HOST,PORT))



	#listen
	server.listen(MAX_QUEUE)
	print 'Proxy server started at port', PORT

	#infinite loop which waits for connections to handle
	while(1):
		# connection acceptation
		client, address = server.accept()
		#create a thread to handle request for the proxy server
		thread.start_new_thread(proxy_thread,(client,address))


	server.close()


def proxy_thread(client, address):

	#get the request from the browser
	request = client.recv(MAX_DATA_RECV)
	
	#request is stripped and split
	splited_request = [line.strip() for line in request.splitlines()]

	if (len(splited_request)>0):
		# aquire method
		method = splited_request[0].split()[0]
		protocol = splited_request[0].split()[2]
		if method in ['GET','HEAD','POST','PUT','DELETE','TRACE'] and protocol in ['HTTP/1.0','HTTP/1.1']:
			#get the host argument
			for argument in splited_request:
				if argument.startswith('Host:'):
					# the path is the arguement which follows Host:
					path = argument[argument.find(' ') + 1:]
					# case where a port is defined
					if ':' in path:
						host = path[:path.find(':')]
						port = path[:path.find(':')+1]
					# case where is no port defined
					else:
						host = path
						port = 80  # default port value
					break
			# we print the connection data
			print 'Connecting to', host, 'on port', port
			print 'The request is : ', request
			try:
				#this is the socket to handle upstream connection
				proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				# set timeout
				proxy_socket.settimeout(TIMEOUT)
				# connect to upstream
				proxy_socket.connect((host, port))
				# forward request to upstream
				proxy_socket.sendall(request)
				while(1):
					# receive data from upstream
					data = proxy_socket.recv(MAX_DATA_RECV)
					# if the received data is not the end of transmission
					# we send all the data to the client
					if(len(data)>0):
						client.sendall(data) #???
					else:
						break
				#closing of the socket
				proxy_socket.close()
			# exception handler
			except:
				if proxy_socket:
					proxy_socket.close()
			
		elif method in ['OPTION','CONNECT']:
			# no host field
			pass

		else:
			# the request is not valid
			pass

	else:
		# the request is invalid, there is no method to aquire
		pass
	client.close()
	return



if __name__ == "__main__":
	main()