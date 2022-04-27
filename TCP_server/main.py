import socket
import os
import threading


#def hendler():
#def robot_more():


IP = "127.0.0.1" #global variables
PORT = 3999
BUFFER = 1
END = "\a\b"

#server messages
SERVER_MOVE = "102 MOVE" + END
SERVER_TURN_LEFT = "103 TURN LEFT"+ END
SERVER_TURN_RIGHT = "104 TURN RIGHT"+ END
SERVER_PICK_UP = "105 GET MESSAGE"+ END
SERVER_LOGOUT = "106 LOGOUT"+ END
SERVER_KEY_REQUEST = "107 KEY REQUEST"+ END
SERVER_OK = "200 OK"+ END
SERVER_LOGIN_FAILED = "300 LOGIN FAILED"+ END
SERVER_SYNTAX_ERROR = "301 SYNTAX ERROR"+ END
SERVER_LOGIC_ERROR = "302 LOGIC ERROR"+ END
SERVER_KEY_OUT_OF_RANGE_ERROR = "303 KEY OUT OF RANGE"+ END

#time constants
TIMEOUT = 1
TIMEOUT_RECHARGING = 5

def autentication():


if __name__ == '__main__':
    s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP,PORT))
    s.listen(1)
    print("listening")
    conn, addr = s.accept()
    while 420:
        data  = conn.recv(BUFFER)
        if not data:
            break
        print("recieved:",data)
        conn.send(data)
    conn.close()
