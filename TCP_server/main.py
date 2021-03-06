import socket
import re
import os
import select

IP = "127.0.0.1"  # global variables
PORT = 4000
BUFFER = 255
END = "\a\b"

# server messages
SERVER_MOVE = "102 MOVE" + END
SERVER_TURN_LEFT = "103 TURN LEFT" + END
SERVER_TURN_RIGHT = "104 TURN RIGHT" + END
SERVER_PICK_UP = "105 GET MESSAGE" + END
SERVER_LOGOUT = "106 LOGOUT" + END
SERVER_KEY_REQUEST = "107 KEY REQUEST" + END
SERVER_OK = "200 OK" + END
SERVER_LOGIN_FAILED = "300 LOGIN FAILED" + END
SERVER_SYNTAX_ERROR = "301 SYNTAX ERROR" + END
SERVER_LOGIC_ERROR = "302 LOGIC ERROR" + END
SERVER_KEY_OUT_OF_RANGE_ERROR = "303 KEY OUT OF RANGE" + END

# time constants
TIMEOUT = 1
TIMEOUT_RECHARGING = 5

aut_array_s = [23019, 3203, 18789, 16443, 18189]
aut_array_c = [32037, 29295, 13603, 29533, 21952]


def hash(string):
    sum = 0
    for i in range(0, len(string)):
        sum = sum + ord(string[i])
        # print(ord(string[i]))
    sum = (sum * 1000) % 65536
    return sum


def username_s(conn, username):
    n = len(str(username))
    if (n > 18):
        send(conn, SERVER_SYNTAX_ERROR)
        conn.close()


def client_s(conn, client_c):
    client_c = str(client_c)
    if (' ' in client_c):
        send(conn, SERVER_SYNTAX_ERROR)
        conn.close()


def client_n(conn, client):
    print("jsem v funkci")
    if (client // 10000 > 9):
        print("je vetsi")
        send(conn, SERVER_SYNTAX_ERROR)
        conn.close()

def authentication(conn):
    username = correct_message(conn,20)
    username_s(conn, username)
    hash_1 = hash(username)
    send(conn, SERVER_KEY_REQUEST)
    try:
        message = correct_message(conn)
        key_id = int(message)
        print("dostal jsem se sem")
        if (key_id > 4 or key_id < 0):
            print("jsem v cyklu na range klice")
            send(conn, SERVER_KEY_OUT_OF_RANGE_ERROR)
            conn.close()
            exit()
    except:
        print("KEY_SYNTAX_ERROR")
        send(conn, SERVER_SYNTAX_ERROR)
        conn.close()
    has_2 = (hash_1 + aut_array_s[key_id]) % (2 ** 16)
    send(conn, str(has_2) + END)
    CLIENT_CONFIRMATION = correct_message(conn)
    client_s(conn, CLIENT_CONFIRMATION)
    CLIENT_CONFIRMATION = int(CLIENT_CONFIRMATION)
    client_n(conn, CLIENT_CONFIRMATION)
    client_hash = (CLIENT_CONFIRMATION - aut_array_c[key_id]) % 2 ** 16

    if (client_hash == hash_1):
        send(conn, SERVER_OK)
    else:
        send(conn, SERVER_LOGIN_FAILED)
        conn.close()

global_str = ""

def extract_message():
    global global_str
    just_END = global_str.find(END)
    return_val = global_str[0:just_END]
    global_str = global_str[just_END + 2:]
    return return_val

CLIENT_FULL_POWER = "FULL POWER"
CLIENT_RECHARGING = "RECHARGING"
RECHARGING = False

def correct_message(conn,lencheck=12):
    global global_str
    global RECHARGING
    while global_str.find(END) == -1:
        if (RECHARGING):
            tmp = TIMEOUT_RECHARGING
        else:
            tmp = TIMEOUT
        if not (conn in select.select([conn], [], [], tmp)[0]):
            conn.close()
            exit()
        data = conn.recv(BUFFER)
        global_str = global_str + (data.decode('ascii'))

        if (len(data) == 0):
            exit()

        elif (lencheck <= len(data) and data.decode('ascii').find(END) == -1 and CLIENT_RECHARGING.find(global_str) == -1):
            send(conn, SERVER_SYNTAX_ERROR)
            conn.close()
            exit()
        print("recieved:", data)
    message = extract_message()

    if (message == CLIENT_RECHARGING and RECHARGING==False):
        RECHARGING  = True
        return correct_message(conn,lencheck)
    elif (RECHARGING == True):
        if (message == CLIENT_FULL_POWER):
            RECHARGING = False
            return correct_message(conn,lencheck)
        else:
            send(conn, SERVER_LOGIC_ERROR)
            conn.close()
            exit()
            return correct_message(conn,lencheck)
    return message

def send(conn, msg):
    conn.send(bytes(msg, 'ascii'))
    print("send messagge", msg)

def msg_to_cordinates(msg):
    fp(msg)
    return list(map(int, re.findall(r'-?\d+', msg)))  # fcking smart regex

def fp(msg):
    msg = str(msg)
    if ('.' in msg):
        print("JEFLOATING")
        send(msg, msg)
        msg.close()
    else:
        print("NENIFLOATING")
    space_C = msg.count(" ")
    if (space_C > 2):
        # print("vice mezer")
        send(msg, msg)
        msg.close()

def turn_right(conn):
    send(conn, SERVER_TURN_RIGHT)
    return msg_to_cordinates(correct_message(conn))

def turn_left(conn):
    send(conn, SERVER_TURN_LEFT)
    return msg_to_cordinates(correct_message(conn))

def move(conn):
    send(conn, SERVER_MOVE)
    return msg_to_cordinates(correct_message(conn))


def horse_move(conn):
    turn_right(conn)
    move(conn)

    turn_left(conn)
    move(conn)
    move(conn)
    # right move left move move


def robot(conn):  # chess bitch
    current_position = [2, 2]  # garbage

    last_position = [3, 3]  # garbage

    while current_position != [0, 0]:
        last_position, current_position = current_position, move(conn)
        if (last_position == current_position):
            horse_move(conn)
        else:
            rotate(last_position, current_position, conn)
    send(conn, SERVER_PICK_UP)
    correct_message(conn,100)
    send(conn, SERVER_LOGOUT)
    conn.close()


def rotate(last, current, conn):
    deltaX, deltaY = current[0] - last[0], current[1] - last[1]
    if (deltaX > 0):
        rot_1 = "right"
    elif (deltaX < 0):
        rot_1 = "left"
    elif (deltaY > 0):
        rot_1 = "up"
    else:
        rot_1 = "down"

    if (current[0] > 0):
        rot_2 = "left"
    elif (current[1] < 0):
        rot_2 = "up"
    elif (current[0] < 0):
        rot_2 = "right"
    else:
        rot_2 = "down"

    print(current, last, deltaX, deltaY)
    print(rot_1, rot_2)
    if (rot_1 == "right" and rot_2 == "right"):
        return
    elif (rot_1 == "right" and rot_2 == "left"):
        turn_right(conn)
        turn_right(conn)
    elif (rot_1 == "right" and rot_2 == "up"):
        turn_left(conn)
    elif (rot_1 == "right" and rot_2 == "down"):
        turn_right(conn)

    elif (rot_1 == "left" and rot_2 == "right"):
        turn_right(conn)
        turn_right(conn)
    elif (rot_1 == "left" and rot_2 == "left"):
        return
    elif (rot_1 == "left" and rot_2 == "up"):
        turn_right(conn)
    elif (rot_1 == "left" and rot_2 == "down"):
        turn_left(conn)

    elif (rot_1 == "up" and rot_2 == "right"):
        turn_right(conn)
    elif (rot_1 == "up" and rot_2 == "left"):
        turn_left(conn)
    elif (rot_1 == "up" and rot_2 == "up"):
        return
    elif (rot_1 == "up" and rot_2 == "down"):
        turn_right(conn)
        turn_right(conn)

    elif (rot_1 == "down" and rot_2 == "right"):
        turn_left(conn)
    elif (rot_1 == "down" and rot_2 == "left"):
        turn_right(conn)
    elif (rot_1 == "down" and rot_2 == "up"):
        turn_right(conn)
        turn_right(conn)
    elif (rot_1 == "down" and rot_2 == "down"):
        return

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    s.listen(1)
    while True:
        print("listening")
        conn, addr = s.accept()
        pid = os.fork()
        if (pid > 0):
            conn.close()
            continue
        s.close()
        try:
            authentication(conn)
            robot(conn)
        except:
            send(conn, SERVER_SYNTAX_ERROR)
        conn.close()

if __name__ == '__main__':
    main()
