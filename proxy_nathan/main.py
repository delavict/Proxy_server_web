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
 
   