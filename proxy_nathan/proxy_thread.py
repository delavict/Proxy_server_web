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

	# find the webserver and proxy_thread