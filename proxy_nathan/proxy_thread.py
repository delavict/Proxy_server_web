def proxy_thread(conn, client_addr):

	#get the request from the browser
	request = conn.recv(MAX_DATA_RECV)

	#parse the first line
	first_line = request.split('n')[0]

	#get the url
	url = first_line.split(' ')[1]

	if(DEBUG)
		print first_line
		print
		print "url : ", url
		print

	# find the webserver and port
	http_pos = url.find("://")	# find pos of://
	if(http_pos == 1):
		temp = url
	else
		temp = url[(http_pos+3):]  #get the rest of the url

	port_pos = temp.find(":") 		# find the port

	# let's find end of the web server
	webserver_pos = temp.find("/")
	if webserver_pos == -1 : 
		webserver_pos = len(temp)

	webserver = ""
	port = -1
	if(port_pos == -1 or webserver_pos < port_pos ) : 
		port = 80
		webserver = temp[:webserver_pos]
	else: 		
		port = int((temp[(port_pos+1):])[:webserver_pos - port_pos-1])
		webserver = temp[:port_pos]

	print "Connect to", webserver, port

	try:
		#create a socket to connect to the web server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((webserver,port))
		s.send(request) 		# send request to webserver

		while 1 : 
			# receive the data from the web server
			data = s.recv(MAX_DATA_RECV)

			if(len(data) > 0):
				# send the data to the browser
				conn.send(data)
			else:
				break
		s.close()
		conn.close()

	except socket.error,(value,message):
		if s:
			s.close()
		fi conn 
			conn.close()
		print "Runtime error : ",message
		sys.exit(1)
