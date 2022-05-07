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
    for i in range(0, len(string)):
        sum=sum+ord(string[i])
        #print(ord(string[i]))
    sum = (sum*1000) % 65536
    return sum


def authentication(conn):
    username = correct_message(conn)
    hash_1 = hash(username)
    send(conn, SERVER_KEY_REQUEST)

    key_id = int(correct_message(conn))

    has_2 = (hash_1 + aut_array_s[key_id]) % (2**16)

    #conn.send(bytes(str(has_2) + END, 'ascii'))
    send(conn, str(has_2) + END)
    CLIENT_CONFIRMATION = correct_message(conn)

    client_hash = (int(CLIENT_CONFIRMATION) - aut_array_c[key_id])%2**16

    if(client_hash == hash_1 ):
        #conn.send(bytes(SERVER_OK, 'ascii'))
        send(conn, SERVER_OK)
    else:
        #conn.send(bytes(SERVER_LOGIN_FAILED, 'ascii'))
        send(conn, SERVER_LOGIN_FAILED)
        conn.close()

global_str = ""

def extract_message():
    global global_str
    just_END = global_str.find(END)
    return_val = global_str[0:just_END]

    global_str = global_str[just_END + 2:]
    return return_val

def correct_message(conn):
    global global_str
    while global_str.find(END) ==-1:
        data = conn.recv(BUFFER)
        if (len(data) == 0):
            exit()
        global_str = global_str + (data.decode('ascii'))
        print("recieved:", data)
    return extract_message()


def send(conn, msg):
    conn.send(bytes(msg, 'ascii'))
    print("send messagge", msg)

def main():
    #print(hash("Mnau!"))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))

    s.listen(1)
    print("listening")
    conn, addr = s.accept()
    # while 420:
    #
    #
    #     conn.send(data)
    authentication(conn)
    send(conn,SERVER_PICK_UP)
    conn.close()



if __name__ == '__main__':
    main()
