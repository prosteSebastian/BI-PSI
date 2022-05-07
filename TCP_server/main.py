import socket
import os
import threading


#def hendler():
#def robot_more():





IP = "127.0.0.1" #global variables
PORT = 3999
BUFFER = 255
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

aut_array_s = [23019,3203, 18789, 16443, 18189]
aut_array_c = [32037, 29295, 13603, 29533, 21952]

def hash(string):

    sum = 0
    for i in range(0, len(string) - 1):
        sum=+ord(string[i])

    sum = (sum*1000)%2**16
    return sum


def authentication():
    pass

str = ""

def extract_message():
    global str
    lmao_END = str.find(END)
    return_val = str[0:lmao_END]

    str = str[END+2:]
    return return_val

def correct_message(conn):
    global str
    while str.find(END) ==-1:

        data = conn.recv(BUFFER)
        str = str + (data.decode('ascii'))
        print("recieved:", data)



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))

    s.listen(1)
    print("listening")
    conn, addr = s.accept()
    correct_message(conn)
    # while 420:
    #
    #
    #     conn.send(data)
    conn.close()


if __name__ == '__main__':
    main()
