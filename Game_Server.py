from socket import *
import threading
import random
import time


semdict = dict()

def func_auth(conn_socket,tmpmsg,auth_dict):
    acc = tmpmsg[1]
    pwd = tmpmsg[2]
    if acc in auth_dict.keys():
        if auth_dict[acc] == pwd:
            conn_socket.send("1001 Authentication successful".encode())
            return True
        else:
            conn_socket.send("1002 Authentication fail".encode())
    else:
        conn_socket.send("1002 Authentication fail".encode())
    return False


# This function is for game logic
def func_enter_game(conn_socket,room,room_dict,sem):
    conn_socket.send("3012 Game started. Please guess true or false".encode())
    tmpbool = ""
    while True:
        recv_msg = conn_socket.recv(1024).decode().split(" ")
        tmpstr = ""
        if len(recv_msg) != 2:
            tmpstr = "4002 Unrecognized message"
        else:
            if recv_msg[0] != "/guess" or(recv_msg[1] != "true" and recv_msg[1] != "false"):
                tmpstr = "4002 Unrecognized message"
            else:
                tmpbool = recv_msg[1]
                break
        conn_socket.send(tmpstr.encode())
        
    room_dict[room][conn_socket] = tmpbool.strip().lower()
    
    sem.acquire() # semaphore to avoid deadlock
    if "result" not in room_dict[room].keys():
        if random.random() <= 0.5:
            room_dict[room]["result"] = "false"
        else:
            room_dict[room]["result"] = "true"
    sem.release() # semaphore to avoid deadlock

    msgToBeSent = ""
    #print(room_dict[room].keys())
    for k in room_dict[room].keys():
        if k != conn_socket: #check if another player fill up the answer

            while room_dict[room][k] == "Non":
                time.sleep(0.5) # Waiting for another thread to finished

            sem.acquire() # semaphore to avoid deadlock
            if room_dict[room][k] == room_dict[room][conn_socket]:
                msgToBeSent = "3023 The result is a tie"
            else:
                if room_dict[room][conn_socket] != room_dict[room]["result"]:
                    msgToBeSent = "3022 You lost this game"
                else:
                    msgToBeSent = "3021 You are the winner"
            sem.release() # semaphore to avoid deadlock
            break;
                
    time.sleep(1) # To avoid another client didn't finish the game, otherwise BUG occurs, cuz the "room_dict[room]" is lose
    sem.acquire() # semaphore to avoid deadlock
    if room in room_dict.keys():
        del room_dict[room]
    sem.release() # semaphore to avoid deadlock
    conn_socket.send(msgToBeSent.encode())


def func_enter(conn_socket,client_port,room,room_dict): # param: client_port could discard
    if room in room_dict.keys(): # if room exist
        if len(room_dict[room]) >= 2: # if full
            conn_socket.send("3013 The room is full".encode())
        else:
            room_dict[room][conn_socket] = "Non"
            for k in semdict.keys():
                if semdict[k] == room:
                    kk = k;
            func_enter_game(conn_socket,room,room_dict,kk)
    else:
        socket_to_bool = dict() #store the connection socket of specific user and his/her choice, key:socket obj, value:String
        room_dict[room] = dict()
        room_dict[room][conn_socket] = "Non"
        
        
        for kk in semdict.keys(): #choose semaphore in list
            if semdict[kk] == "nil":
                semdict[kk] = room
                break;

        
        print("Room info:" + str(room_dict[room]))
        conn_socket.send("3011 Wait".encode())
        while True:
            if len(room_dict[room]) == 2:
                func_enter_game(conn_socket,room,room_dict,kk)
                semdict[kk] = "nil"
                break
            continue

    

def thrfunc(arg,auth_dict,room_dict):
    conn_socket,addr = arg
    client_port = str(addr[1])
    # Error checking
    while(True):
        try:
            msg = conn_socket.recv(1024).decode()
        except error as err:
            print("Recv error: ",err)
        if msg:
            tmpmsg = msg.split(" ")
            instruction = tmpmsg[0]
            
            if instruction == "/login":
                res = func_auth(conn_socket,tmpmsg,auth_dict)
                while res == False:
                    msg = conn_socket.recv(1024).decode()
                    tmpmsg = msg.split(" ")
                    res = func_auth(conn_socket,tmpmsg,auth_dict)
            elif instruction == "/list":
                #room_num = len(room_dict)
                room_num = 10 #<--- 10 rooms
                tmpstr = "3001 "+str(room_num)+" "

                tmplist = list() # for sorting key
                for k in room_dict.keys():
                    tmplist.append(int(k))
                    
                tmplist.sort()
                tmplist2 = list()
                for tmpi in range(1,11,1):
                    if str(tmpi) in room_dict.keys():
                        tmplist2.append(str(len(room_dict[str(tmpi)])))
                    else:
                        tmplist2.append("0")
                    
                for tmpi in tmplist2:
                    tmpstr += tmpi + " "
                    
                print(tmpstr)
                
                conn_socket.send(tmpstr.encode())
            elif instruction == "/enter" and len(tmpmsg)==2:
                room = tmpmsg[1]
                func_enter(conn_socket,client_port,room,room_dict)           
            elif instruction == "/exit":
                conn_socket.send("4001 Bye bye".encode())
                conn_socket.close()
                break;
            else:
                conn_socket.send("4002 Unrecognized message".encode())
            

if __name__ == "__main__":
    for i in range(1,101,1): #semaphore dictionary size = max. # of room concurrently run
        sem =threading.Semaphore(1) 
        semdict[sem] = "nil" #Key:semaphore object, value:room #
        
        
    acc_dict = dict() #A dictionary for authentication - key:username,value:password
    room_dict = dict() #A dictionary for room number - key:Room #,value: dictionary - {socket:boolean} -- Detail in "readme.md" file

    port = 20000
    filename="UserInfo.txt"
    f = open(filename,"r")
    tmpstr = f.readlines()
    for i in tmpstr:
        tmp = i.strip("\n").split(":")
        acc = tmp[0]
        pwd = tmp[1]
        acc_dict[acc] = pwd
    f.close()

    socket = socket(AF_INET,SOCK_STREAM)
    socket.bind(("",20000))
    socket.listen(5)
    seq = 0
    
    while True:
        arg = socket.accept()
        newthr = threading.Thread(target=thrfunc,args=(arg,acc_dict,room_dict,))
        newthr.start()
        
    socket.close()

