import os,sys,thread,socket
 
#### CONSTANT VARIABLES ####
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = False          # debug variable
 
####  MAIN PROGRAM ###
def main():
 
    # check the length of command running
    if (len(sys.argv) < 2):
        print "usage: proxy <port>"
        return sys.stdout
 
   
    #host and port info : 
    host = ''       # blank for localhost
    port = int(sys.argv[1]) # port from argument

    try:
        #create a socket 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #association of the socket with the host and the port
        s.bind(host,port);

        #listening to the socket
        s.listen(BACKLOG);

    except socket.error,(value,message):
        if s:
            s.close()
        print "Could not open socket : " message
        sys.exit(1)

    #get the connection from client
    while 1:
        conn, client_addr = s.accept()

        # create a thread to handle request for the proxy server
        thread.start_new_thread(proxy_thread,(conn,client_addr))

    s.close()

if __name__ == '__main__' : 
    main()

